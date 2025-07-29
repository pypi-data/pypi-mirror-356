# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-01-22

### Added
- Initial release of AsyncMCP
- SQS+SNS transport layer for MCP clients and servers
- LocalStack integration for development and testing
- Background task processing capabilities

### Features
- **Client Transport**: `SQSClientTransportConfig` and `sqs_sns_client` for async client communication
- **Server Transport**: `SQSServerTransportConfig` and `sqs_sns_server` for async server communication  
- **Type Safety**: Full type hint support with `py.typed` marker
- **AWS Integration**: Native boto3 integration for SQS and SNS services

### Documentation
- Comprehensive README with usage examples
- API documentation in docstrings
- LocalStack development setup guide
- Testing documentation and examples

### Testing
- Unit tests for client and server transports
- Integration tests for full message flow
- LocalStack-based testing environment

[Unreleased]: https://github.com/bh-rat/asyncmcp/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/bh-rat/asyncmcp/releases/tag/v0.1.0 