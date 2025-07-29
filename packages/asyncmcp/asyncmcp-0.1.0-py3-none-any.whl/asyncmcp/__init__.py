"""
Async MCP - Async Transport layer for MCP

This package provides async transport layer implementations for MCP (Model Context Protocol)
clients and servers, with support for AWS SQS and SNS as transport mechanisms.
"""

__version__ = "0.1.0"

# Import main transport configurations and functions
from .client.sns_sqs import SQSClientTransportConfig, sqs_sns_client
from .server.sns_sqs import SQSTransportConfig, sqs_sns_server

__all__ = [
    "SQSClientTransportConfig",
    "sqs_sns_client", 
    "SQSTransportConfig",
    "sqs_sns_server",
    "__version__",
]
