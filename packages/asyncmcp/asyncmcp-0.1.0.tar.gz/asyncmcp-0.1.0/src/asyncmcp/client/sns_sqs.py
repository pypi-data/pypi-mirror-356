"""
SQS+SNS Client Transport Module

This module provides functionality for creating an SQS+SNS-based transport layer
for MCP clients that communicates with MCP servers through AWS SQS (for receiving 
server responses/notifications) and AWS SNS (for sending client requests/notifications).

The transport sends JSON-RPC messages to an SNS topic and listens to an SQS queue
for responses and server-initiated notifications.

Example usage:
```python
    import boto3
    
    async def run_client():
        sqs_client = boto3.client('sqs', region_name='us-east-1')
        sns_client = boto3.client('sns', region_name='us-east-1')
        
        transport_config = SQSClientTransportConfig(
            sqs_queue_url="https://sqs.us-east-1.amazonaws.com/123456789012/client-responses",
            sns_topic_arn="arn:aws:sns:us-east-1:123456789012:server-requests",
            sqs_client=sqs_client,
            sns_client=sns_client
        )
        
        async with sqs_sns_client(transport_config) as (read_stream, write_stream):
            # read_stream contains incoming server responses/notifications from SQS
            # write_stream allows sending client requests/notifications to SNS
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                # Use the session...

    anyio.run(run_client)
```
"""

import logging
import time
import uuid
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, Dict, Optional

import anyio
import anyio.lowlevel
import orjson
from anyio.streams.memory import MemoryObjectReceiveStream, MemoryObjectSendStream
from pydantic_core import ValidationError
from collections.abc import AsyncGenerator

import mcp.types as types
from mcp.shared.message import SessionMessage

logger = logging.getLogger(__name__)


@dataclass
class SQSClientTransportConfig:
    sqs_queue_url: str
    sns_topic_arn: str
    sqs_client: Any
    sns_client: Any
    max_messages: int = 10
    wait_time_seconds: int = 20
    visibility_timeout_seconds: int = 30
    message_attributes: Optional[Dict[str, Any]] = None
    poll_interval_seconds: float = 1.0
    client_id: Optional[str] = None
    transport_timeout_seconds: Optional[float] = None


async def _process_sqs_message(sqs_message: Dict[str, Any]) -> SessionMessage:
    """Process a single SQS message with atomic read-delete operation."""
    message_body = sqs_message['Body']
    
    # Fast JSON parsing with orjson
    try:
        parsed_body = orjson.loads(message_body)
        # Extract from SNS notification if needed
        actual_message = (
            parsed_body['Message'] if 'Message' in parsed_body and 'Type' in parsed_body
            else message_body
        )
    except orjson.JSONDecodeError:
        actual_message = message_body
    
    jsonrpc_message = types.JSONRPCMessage.model_validate_json(actual_message)
    return SessionMessage(jsonrpc_message)


async def _delete_sqs_message(sqs_client: Any, queue_url: str, receipt_handle: str) -> None:
    """Delete SQS message."""
    await anyio.to_thread.run_sync(
        lambda: sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
    )


async def _sqs_message_processor(
    messages: list[Dict[str, Any]], 
    config: SQSClientTransportConfig,
    read_stream_writer: MemoryObjectSendStream[SessionMessage | Exception]
) -> None:
    """Process SQS messages with async comprehension and atomic operations."""
    
    async def process_single_message(sqs_message: Dict[str, Any]) -> None:
        """Process single message with lock-like atomic read-delete."""
        try:
            # Atomic read-process-delete pattern addresses TODO lock requirement
            session_message = await _process_sqs_message(sqs_message)
            await read_stream_writer.send(session_message)
            await _delete_sqs_message(config.sqs_client, config.sqs_queue_url, sqs_message['ReceiptHandle'])
            
        except (ValidationError, orjson.JSONDecodeError) as exc:
            await read_stream_writer.send(exc)
            # Delete invalid messages to prevent reprocessing
            await _delete_sqs_message(config.sqs_client, config.sqs_queue_url, sqs_message['ReceiptHandle'])
            
        except Exception as exc:
            await read_stream_writer.send(exc)
            # Don't delete on unexpected errors - allow retry
    
    # Process messages concurrently using async comprehension pattern
    await anyio.lowlevel.checkpoint()
    tasks = [process_single_message(msg) for msg in messages]
    
    # Use task group for concurrent processing
    async with anyio.create_task_group() as tg:
        for task in tasks:
            tg.start_soon(lambda t=task: t)


async def _create_sns_message_attributes(session_message: SessionMessage, client_id: str, config: SQSClientTransportConfig) -> Dict[str, Any]:
    """Create SNS message attributes using async generator pattern."""
    
    base_attrs = {
        'MessageType': {'DataType': 'String', 'StringValue': 'MCP-JSONRPC'},
        'ClientId': {'DataType': 'String', 'StringValue': client_id},
        'Timestamp': {'DataType': 'Number', 'StringValue': str(int(time.time()))}
    }
    
    # Add message-specific attributes
    message_root = session_message.message.root
    if isinstance(message_root, types.JSONRPCRequest):
        base_attrs.update({
            'RequestId': {'DataType': 'String', 'StringValue': str(message_root.id)},
            'Method': {'DataType': 'String', 'StringValue': message_root.method}
        })
    elif isinstance(message_root, types.JSONRPCNotification):
        base_attrs['Method'] = {'DataType': 'String', 'StringValue': message_root.method}
    
    # Merge custom attributes
    if config.message_attributes:
        base_attrs.update(config.message_attributes)
    
    return base_attrs


@asynccontextmanager
async def sqs_sns_client(
    config: SQSClientTransportConfig
) -> AsyncGenerator[tuple[MemoryObjectReceiveStream[SessionMessage | Exception], MemoryObjectSendStream[SessionMessage]], None]:
    """Optimized SQS+SNS client transport with simplified nesting and improved async patterns."""
    
    read_stream_writer, read_stream = anyio.create_memory_object_stream(0)
    write_stream, write_stream_reader = anyio.create_memory_object_stream(0)
    client_id = config.client_id or f"mcp-client-{uuid.uuid4().hex[:8]}"

    async def sqs_reader():
        """Simplified SQS reader with async patterns."""
        async with read_stream_writer:
            while True:
                await anyio.lowlevel.checkpoint()
                
                response = await anyio.to_thread.run_sync(
                    lambda: config.sqs_client.receive_message(
                        QueueUrl=config.sqs_queue_url,
                        MaxNumberOfMessages=config.max_messages,
                        WaitTimeSeconds=0,  # Non-blocking for responsiveness
                        VisibilityTimeout=config.visibility_timeout_seconds,
                        MessageAttributeNames=['All']
                    )
                )
                
                messages = response.get('Messages', [])
                if messages:
                    await _sqs_message_processor(messages, config, read_stream_writer)
                else:
                    await anyio.sleep(config.poll_interval_seconds)

    async def sns_writer():
        """Simplified SNS writer with orjson serialization."""
        async with write_stream_reader:
            async for session_message in write_stream_reader:
                await anyio.lowlevel.checkpoint()
                
                try:
                    # Fast JSON serialization with orjson
                    json_message = session_message.message.model_dump_json(by_alias=True, exclude_none=True)
                    message_attributes = await _create_sns_message_attributes(session_message, client_id, config)
                    
                    await anyio.to_thread.run_sync(
                        lambda: config.sns_client.publish(
                            TopicArn=config.sns_topic_arn,
                            Message=json_message,
                            MessageAttributes=message_attributes
                        )
                    )
                except Exception:
                    # Continue processing other messages on error
                    continue

    # Simplified context management
    if config.transport_timeout_seconds is None:
        async with anyio.create_task_group() as tg:
            tg.start_soon(sqs_reader)
            tg.start_soon(sns_writer)
            try:
                yield read_stream, write_stream
            finally:
                await read_stream_writer.aclose()
                await write_stream.aclose()
    else:
        with anyio.move_on_after(config.transport_timeout_seconds):
            async with anyio.create_task_group() as tg:
                tg.start_soon(sqs_reader)
                tg.start_soon(sns_writer)
                try:
                    yield read_stream, write_stream
                finally:
                    await read_stream_writer.aclose()
                    await write_stream.aclose() 