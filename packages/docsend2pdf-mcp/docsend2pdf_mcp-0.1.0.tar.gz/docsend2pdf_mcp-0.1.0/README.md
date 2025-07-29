# docsend2pdf-mcp

MCP server for converting DocSend documents to PDF via docsend2pdf.com

## Installation

```bash
pip install docsend2pdf-mcp
```

## Configuration

```json
{
    "mcpServers": {
        "docsend2pdf": {
            "command": "python",
            "args": ["-m", "docsend2pdf_mcp"],
            "env": {
                "DOCSEND2PDF_DOWNLOAD_DIR": "~/Downloads/docsend_pdfs"
            }
        }
    }
}
```

## Usage

- Convert: `"Convert this DocSend to PDF: https://docsend.com/view/abc123"`
- With password: `"Convert https://docsend.com/view/xyz789 (password: mypass)"`
- With email: `"Convert https://docsend.com/view/doc456 (email: user@example.com)"`
- Custom filename: `"Save https://docsend.com/view/doc789 as report.pdf"`

## Features

- Password-protected documents
- Email-verification support
- OCR for searchable PDFs
- Custom filenames
- Rate limiting (5 req/sec)

## License

MIT
