# PDF Reader MCP Server

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/pdf-reader-mcp.svg)](https://badge.fury.io/py/pdf-reader-mcp)

A powerful Model Context Protocol (MCP) server that provides comprehensive PDF processing capabilities, including text extraction, OCR support, and network diagram detection. Designed to work seamlessly with Amazon Q Developer CLI and other MCP-compatible systems.

## 🚀 Features

- **Text Extraction**: Extract text content from PDF files with high accuracy
- **PDF Analysis**: Get comprehensive metadata (pages, document info, encryption status)
- **Page-Specific Processing**: Extract text from specific pages
- **Multi-Language OCR**: Support for Thai and English text recognition
- **Smart Processing**: Automatically chooses between OCR and direct text extraction
- **Markdown Conversion**: Convert PDF content to clean markdown format
- **Document Analysis**: Determine if PDFs are scanned images or searchable text
- **Network Diagram Detection**: Advanced capability to detect and extract network diagrams
- **MCP Integration**: Seamless integration with Amazon Q Developer CLI

## 📦 Installation

### Using uvx (Recommended)

The easiest way to use this MCP server is with `uvx`:

```bash
# Run directly without installation
uvx pdf-reader-mcp # your mcp client can now connect using both sse and stdio transport

# Or install globally
uvx install pdf-reader-mcp
```

### Using pip

```bash
pip install pdf-reader-mcp
```

### From Source

```bash
git clone https://github.com/zixma13/pdf-reader-mcp.git
cd pdf-reader-mcp
pip install -e .
```

## 📋 Prerequisites

1. Install Tesseract OCR (required for OCR functionality):
   ```bash
   # For macOS
   brew install tesseract
   brew install tesseract-lang  # For language support including Thai
   
   # For Ubuntu/Debian
   # sudo apt-get install tesseract-ocr
   # sudo apt-get install tesseract-ocr-tha  # For Thai language support
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure you have the virtual environment activated:
   ```bash
   source .venv/bin/activate
   ```

4. Test the server:
   ```bash
   mcp dev main.py
   ```

## Configuration for Amazon Q Developer CLI

Add the following to your `~/.aws/amazonq/mcp.json` file:

- in case you clone the git repository

```json
{
  "mcpServers": {
    "pdf_reader": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/your/pdf_reader/pdf_reader",
        "run",
        "main.py"
      ]
    }
  }
}
```

- in case you use uvx 
```json
{
  "mcpServers": {
    "pdf_reader": {
      "command": "uvx",
      "timeout": 60000,
      "args": [
        "pdf-reader-mcp"
      ]
    }
  }
}
```


## Usage Examples

Once configured, you can use the PDF reader tools in Amazon Q:

### Basic PDF Processing

- To analyze a PDF and determine if it's a scanned image or searchable text:
  ```
  pdf_reader___analyze_pdf("/path/to/document.pdf")
  ```

- To intelligently extract content from a PDF (automatically choosing between OCR and text extraction):
  ```
  pdf_reader___smart_extract_pdf("/path/to/document.pdf")
  ```

- To intelligently convert a PDF to markdown:
  ```
  pdf_reader___smart_pdf_to_markdown("/path/to/document.pdf")
  ```

- To extract text from a PDF:
  ```
  pdf_reader___read_pdf("/path/to/document.pdf")
  ```

- To get metadata from a PDF:
  ```
  pdf_reader___get_pdf_metadata("/path/to/document.pdf")
  ```

- To extract text from a specific page (0-indexed):
  ```
  pdf_reader___extract_pdf_page("/path/to/document.pdf", 0)
  ```

- To extract text using OCR (supports Thai and English):
  ```
  pdf_reader___ocr_pdf("/path/to/document.pdf")
  ```

- To extract text from a specific page using OCR:
  ```
  pdf_reader___ocr_pdf_page("/path/to/document.pdf", 0)
  ```

- To convert PDF to markdown format:
  ```
  pdf_reader___pdf_to_markdown("/path/to/document.pdf")
  ```

- To convert PDF to markdown format using OCR:
  ```
  pdf_reader___pdf_to_markdown("/path/to/document.pdf", use_ocr=True)
  ```

