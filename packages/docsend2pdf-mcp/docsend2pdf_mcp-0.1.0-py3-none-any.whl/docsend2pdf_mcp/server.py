"""MCP server for docsend2pdf.com API - Updated implementation"""

import os
import asyncio
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime
from pathlib import Path

import httpx
from mcp.server.lowlevel import Server
from mcp import types

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Create the server instance
server = Server("docsend2pdf")

# Configuration
API_URL = "https://docsend2pdf.com/api/convert"
DOWNLOAD_DIR = Path(os.environ.get("DOCSEND2PDF_DOWNLOAD_DIR", "~/Downloads/docsend_pdfs")).expanduser()

# Create download directory if it doesn't exist
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

# HTTP client with timeout
http_client = httpx.AsyncClient(
    timeout=httpx.Timeout(300.0),  # 5 minutes for large documents
    follow_redirects=True
)

# Rate limiter instance
rate_limiter = None


class RateLimiter:
    """Simple rate limiter for API calls"""
    
    def __init__(self, max_requests: int, time_window: float):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
        self.lock = asyncio.Lock()
    
    async def acquire(self):
        """Wait if necessary to respect rate limits"""
        async with self.lock:
            while True:
                now = asyncio.get_event_loop().time()
                
                # Remove old requests outside the time window
                self.requests = [req_time for req_time in self.requests 
                               if now - req_time < self.time_window]
                
                # If at limit, wait until oldest request expires
                if len(self.requests) >= self.max_requests:
                    sleep_time = self.time_window - (now - self.requests[0]) + 0.01
                    if sleep_time > 0:
                        logger.info(f"Rate limit reached, waiting {sleep_time:.2f}s")
                        await asyncio.sleep(sleep_time)
                        continue  # Check again after sleeping
                
                # Record this request and exit
                self.requests.append(now)
                break


# Initialize rate limiter
rate_limiter = RateLimiter(max_requests=5, time_window=1.0)

logger.info(f"DocSend2PDF MCP server initialized. PDFs will be saved to: {DOWNLOAD_DIR}")


# Register handlers
@server.list_tools()
async def list_tools_handler() -> List[types.Tool]:
    """Return the list of available tools"""
    return [
        types.Tool(
            name="convert_docsend",
            description="Convert a DocSend document to PDF. Returns the path to the saved PDF file.",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "The DocSend URL to convert"
                    },
                    "email": {
                        "type": "string",
                        "description": "Email for password-protected documents (optional)"
                    },
                    "passcode": {
                        "type": "string",
                        "description": "Password for password-protected documents (optional)"
                    },
                    "searchable": {
                        "type": "boolean",
                        "description": "Whether to make the PDF searchable with OCR (default: false)"
                    },
                    "filename": {
                        "type": "string",
                        "description": "Custom filename for the PDF (optional)"
                    }
                },
                "required": ["url"]
            }
        )
    ]


@server.call_tool()
async def call_tool_handler(name: str, arguments: Any) -> List[types.TextContent]:
    """Handle tool calls"""
    if name == "convert_docsend":
        return await convert_docsend(**arguments)
    else:
        return [types.TextContent(type="text", text=f"Error: Unknown tool '{name}'")]


async def convert_docsend(
    url: str,
    email: Optional[str] = None,
    passcode: Optional[str] = None,
    searchable: bool = False,
    filename: Optional[str] = None
) -> List[types.TextContent]:
    """
    Convert a DocSend document to PDF.
    
    Args:
        url: DocSend URL to convert
        email: Email for password-protected documents
        passcode: Password for password-protected documents
        searchable: Whether to make the PDF searchable with OCR
        filename: Custom filename for the PDF
        
    Returns:
        Success message with file path or error message
    """
    try:
        # Validate URL
        url = url.strip()
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"
        
        if "docsend.com/view/" not in url:
            return [types.TextContent(type="text", text="Error: Invalid DocSend URL. URL must contain 'docsend.com/view/'")]
        
        logger.info(f"Converting DocSend document: {url}")
        
        # Apply rate limiting
        await rate_limiter.acquire()
        
        # Prepare request data
        data = {
            "url": url,
            "email": email or "",
            "passcode": passcode or "",
            "searchable": searchable
        }
        
        # Make API request
        response = await http_client.post(
            API_URL,
            json=data,
            headers={"User-Agent": "DocSend2PDF-MCP/1.0"}
        )
        
        # Handle rate limiting
        if response.status_code == 429:
            retry_after = response.headers.get("Retry-After", "60")
            error_msg = f"Rate limit exceeded. Please retry after {retry_after} seconds."
            logger.warning(error_msg)
            return [types.TextContent(type="text", text=f"Error: {error_msg}")]
        
        # Handle errors
        if not response.is_success:
            try:
                error_data = response.json()
                error_msg = error_data.get("error", f"HTTP {response.status_code}")
            except:
                error_msg = f"HTTP {response.status_code}: {response.text}"
            
            logger.error(f"API error: {error_msg}")
            return [types.TextContent(type="text", text=f"Error: Failed to convert document - {error_msg}")]
        
        # Extract filename from Content-Disposition header
        content_disposition = response.headers.get("Content-Disposition", "")
        if not filename:
            if "filename=" in content_disposition:
                # Extract filename from header
                filename = content_disposition.split("filename=")[-1].strip('"')
            else:
                # Generate filename based on URL and timestamp
                doc_id = url.split("/")[-1].split("?")[0]
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"docsend_{doc_id}_{timestamp}.pdf"
        
        # Ensure .pdf extension
        if not filename.endswith(".pdf"):
            filename += ".pdf"
        
        # Save PDF to disk
        filepath = DOWNLOAD_DIR / filename
        filepath.write_bytes(response.content)
        
        logger.info(f"PDF saved successfully: {filepath}")
        
        # Return success message with file path
        return [types.TextContent(
            type="text",
            text=f"✅ PDF converted successfully!\n\nSaved to: {filepath}\nFile size: {len(response.content) / 1024 / 1024:.1f} MB"
        )]
        
    except Exception as e:
        logger.error(f"Error converting document: {str(e)}")
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]



