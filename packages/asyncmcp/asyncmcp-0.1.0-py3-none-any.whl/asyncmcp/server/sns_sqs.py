"""
SQS+SNS Server Transport Module

Optimized transport layer for MCP servers using AWS SQS/SNS with orjson and async patterns.
"""

import logging
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, Dict, Optional

import anyio
import anyio.lowlevel
import orjson
from anyio.streams.memory import MemoryObjectReceiveStream, MemoryObjectSendStream
from pydantic_core import ValidationError

import mcp.types as types
from mcp.shared.message import SessionMessage

logger = logging.getLogger(__name__)


@dataclass
class SQSTransportConfig:
    """Configuration for SQS+SNS transport"""
    sqs_queue_url: str
    sns_topic_arn: str
    sqs_client: Any
    sns_client: Any
    max_messages: int = 10
    wait_time_seconds: int = 20
    visibility_timeout_seconds: int = 30
    message_attributes: Optional[Dict[str, Any]] = None
    poll_interval_seconds: float = 1.0


async def _process_sqs_message(sqs_message: Dict[str, Any], queue_url: str) -> SessionMessage:
    """
    Process a single SQS message with metadata.
    """
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
    
    return SessionMessage(
        jsonrpc_message,
        metadata={
            'sqs_message_id': sqs_message['MessageId'],
            'sqs_receipt_handle': sqs_message['ReceiptHandle'],
            'sqs_message_attributes': sqs_message.get('MessageAttributes', {}),
            'sqs_queue_url': queue_url
        }
    )


async def _delete_sqs_message(sqs_client: Any, queue_url: str, receipt_handle: str) -> None:
    """Delete SQS message."""
    await anyio.to_thread.run_sync(
        lambda: sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
    )


async def _sqs_message_processor(
    messages: list[Dict[str, Any]], 
    config: SQSTransportConfig,
    read_stream_writer: MemoryObjectSendStream[SessionMessage | Exception]
) -> None:
    """Process SQS messages with async comprehension and atomic operations."""
    
    async def process_single_message(sqs_message: Dict[str, Any]) -> None:
        """Process single message with atomic read-delete pattern."""
        try:
            session_message = await _process_sqs_message(sqs_message, config.sqs_queue_url)
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


async def _create_sns_message_attributes(session_message: SessionMessage, config: SQSTransportConfig) -> Dict[str, Any]:
    """Create SNS message attributes."""
    base_attrs = {
        'MessageType': {'DataType': 'String', 'StringValue': 'MCP-JSONRPC'}
    }
    
    # Add custom attributes from config
    if config.message_attributes:
        base_attrs.update(config.message_attributes)
    
    # Add metadata from original message if available
    if hasattr(session_message, 'metadata') and session_message.metadata:
        if isinstance(session_message.metadata, dict) and 'sqs_message_id' in session_message.metadata:
            base_attrs['OriginalSQSMessageId'] = {
                'DataType': 'String',
                'StringValue': session_message.metadata['sqs_message_id']
            }
    
    return base_attrs


@asynccontextmanager
async def sqs_sns_server(config: SQSTransportConfig):
    """Optimized SQS+SNS server transport with simplified nesting and improved async patterns."""
    
    read_stream_writer, read_stream = anyio.create_memory_object_stream(0)
    write_stream, write_stream_reader = anyio.create_memory_object_stream(0)

    async def sqs_reader():
        """Simplified SQS reader with async patterns."""
        async with read_stream_writer:
            while True:
                response = await anyio.to_thread.run_sync(
                    lambda: config.sqs_client.receive_message(
                        QueueUrl=config.sqs_queue_url,
                        MaxNumberOfMessages=config.max_messages,
                        WaitTimeSeconds=config.wait_time_seconds,
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
                try:
                    # Fast JSON serialization
                    json_message = session_message.message.model_dump_json(by_alias=True, exclude_none=True)
                    message_attributes = await _create_sns_message_attributes(session_message, config)
                    
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

    async with anyio.create_task_group() as tg:
        tg.start_soon(sqs_reader)
        tg.start_soon(sns_writer)
        yield read_stream, write_stream 