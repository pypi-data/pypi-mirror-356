# Async MCP - Async Transport layer for MCP

<div align="center">

**Exploring queue based and other async MCP transport layers**

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)

</div>

---

## Overview

Async MCP explores async transport layer implementations for MCP (Model Context Protocol) clients and servers, beyond the officially supported stdio and HTTP transports. 

The whole idea of an **async MCP server with async transport layer** is that it doesn't have to respond immediately to any requests - it can choose to direct them to internal queues for processing and the client doesn't have to stick around for the response.

## Installation

```bash
# Using uv (recommended)
uv add asyncmcp

# Using pip  
pip install asyncmcp
```

## Quick Start

### Basic Server Setup

```python
import boto3
from asyncmcp.server.sns_sqs import sqs_sns_server, SQSTransportConfig

# Configure transport
config = SQSTransportConfig(
    sqs_queue_url="https://sqs.region.amazonaws.com/account/service-queue",
    sns_topic_arn="arn:aws:sns:region:account:mcp-responses",
    sqs_client=boto3.client('sqs'),
    sns_client=boto3.client('sns')
)

async def main():
    async with sqs_sns_server(config) as (read_stream, write_stream):
        # Your MCP server logic here
        pass
```

### LocalStack Development

```bash
# Start LocalStack
localstack start

# Setup resources
cd tests/localstack && ./localstack.sh

# Set endpoint
export AWS_ENDPOINT_URL=http://localhost:4566
```

## Possible Use Cases

- **Background Data Processing**: Submit analysis jobs and receive results when ready
- **Report Generation**: Queue report requests and get notified on completion
- **API Integrations**: Fire-and-forget integrations with external services
- **Scheduled Operations**: Background task execution without blocking main flows
- **Ambient Agent Processing**: Long-running agents that work independently and notify on completion

## Keep in mind

- **Message Size**: For SQS - message size limits (256KB standard, 2MB extended)
- **Response Handling**: Async nature means responses may not be immediate
- **Session Context**: Storage mechanism handled by server application, not transport
- **Ordering**: Standard SQS doesn't guarantee message ordering

## To-Do List

- [ ] **Manager needed for session handling** - Dedicated session lifecycle management
- [ ] **Server cannot have the SNS configuration** - Rather, client defines what queue it wants to listen to while making the connection.
- [ ] **Initialization pending**

## Testing

### Local Development

```bash
cd tests/local
python mcp_server_cli.py                    # Start server
python quick_test_cli.py --interactive      # Interactive client
```

### Integration Testing

```bash
cd tests/localstack
./localstack.sh                             # Setup AWS resources
python run_direct_test.py                   # Run tests
```

### Unit Tests

```bash
uv run pytest                               # All tests
uv run pytest tests/sns_sqs/                # Transport tests
```

## Contributing

We welcome contributions and discussions around async MCP architectures!

### Development Setup

```bash
git clone https://github.com/bharatgeleda/asyncmcp.git
cd asyncmcp
uv sync
```

### Key Areas

- Transport layer optimizations
- Session management patterns
- Message routing strategies
- Production deployment patterns

---

## License

Apache License 2.0 - see [LICENSE](LICENSE) file for details.

## Links

- **MCP Specification**: [https://spec.modelcontextprotocol.io](https://spec.modelcontextprotocol.io)
- **Model Context Protocol**: [https://modelcontextprotocol.io](https://modelcontextprotocol.io)

