# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2025-06-17

### Added
- Initial release of docsend2pdf-mcp
- Convert DocSend documents to PDF via docsend2pdf.com API
- Support for password-protected documents
- Support for email-protected documents
- OCR support for searchable PDFs
- Custom filename support
- Rate limiting (5 requests/second)
- Configurable download directory via DOCSEND2PDF_DOWNLOAD_DIR environment variable
- Full MCP (Model Context Protocol) server implementation for Claude Desktop

### Technical Details
- Built with Python 3.8+ compatibility
- Uses httpx for async HTTP requests
- Implements MCP low-level server API
- Automatic retry handling for rate limits
- Comprehensive error handling with user-friendly messages