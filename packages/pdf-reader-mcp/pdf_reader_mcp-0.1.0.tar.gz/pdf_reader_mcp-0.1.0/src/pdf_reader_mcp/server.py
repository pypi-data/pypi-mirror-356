from mcp.server.fastmcp import FastMCP
import PyPDF2
import os
import base64
from typing import Optional, List, Dict, Any
import pytesseract
from PIL import Image
import io
import fitz  # PyMuPDF
import tempfile
import re
import numpy as np
import pdfkit
import markdown

mcp = FastMCP("pdf_reader")

@mcp.tool()
def get_pdf_metadata(file_path: str) -> Dict[str, Any]:
    """
    Extract metadata from a PDF file i.e. num pages, metadata, is encrypted etc.
    Args:
        file_path: Path to the PDF file
    Returns:
        Dictionary containing metadata information
    """
    if not os.path.exists(file_path):
        return {"error": f"File not found at {file_path}"}
    
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            metadata = {
                "num_pages": len(reader.pages),
                "metadata": reader.metadata or {},
                "is_encrypted": reader.is_encrypted
            }
            return metadata
    except Exception as e:
        return {"error": f"Error reading PDF metadata: {str(e)}"}

@mcp.tool()
def analyze_pdf(file_path: str) -> Dict[str, Any]:
    """
    Analyze a PDF file to determine if it's a scanned image PDF or searchable text PDF
    Args:
        file_path: Path to the PDF file
    Returns:
        Dictionary containing analysis results including PDF type and sample content
    """
    if not os.path.exists(file_path):
        return {"error": f"File not found at {file_path}"}
    
    try:
        result = {
            "file_path": file_path,
            "is_scanned_image": False,
            "has_searchable_text": False,
            "total_pages": 0,
            "first_page_sample": "",
            "last_page_sample": "",
            "text_confidence": 0.0,
            "recommended_extraction_method": "text"
        }
        
        # Get basic metadata
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            result["total_pages"] = len(reader.pages)
            
            # Check first page for text
            first_page_text = reader.pages[0].extract_text().strip()
            result["first_page_sample"] = first_page_text[:500] + "..." if len(first_page_text) > 500 else first_page_text
            
            # Check last page for text
            last_page = reader.pages[-1]
            last_page_text = last_page.extract_text().strip()
            result["last_page_sample"] = last_page_text[:500] + "..." if len(last_page_text) > 500 else last_page_text
            
            # Determine if PDF has searchable text
            result["has_searchable_text"] = len(first_page_text) > 50 or len(last_page_text) > 50
        
        # Use PyMuPDF for more detailed analysis
        doc = fitz.open(file_path)
        
        # Check if pages contain images that might indicate scanned content
        first_page = doc.load_page(0)
        last_page = doc.load_page(-1)
        
        # Count images on first and last pages
        first_page_images = first_page.get_images()
        last_page_images = last_page.get_images()
        
        # If pages have images and little text, likely a scanned document
        result["first_page_image_count"] = len(first_page_images)
        result["last_page_image_count"] = len(last_page_images)
        
        # Perform a quick OCR test on first page to compare with extracted text
        if len(first_page_images) > 0:
            # Render first page to image
            pix = first_page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # Perform OCR
            ocr_text = pytesseract.image_to_string(img)
            
            # Compare OCR text length with extracted text length
            if len(ocr_text.strip()) > len(first_page_text.strip()) * 1.5:
                result["is_scanned_image"] = True
                result["text_confidence"] = min(100, len(first_page_text) / max(1, len(ocr_text)) * 100)
            else:
                result["text_confidence"] = min(100, len(first_page_text) / max(1, len(ocr_text) + 1) * 100)
        
        # Determine recommended extraction method
        if result["is_scanned_image"] or result["text_confidence"] < 50:
            result["recommended_extraction_method"] = "ocr"
        else:
            result["recommended_extraction_method"] = "text"
            
        doc.close()
        return result
    except Exception as e:
        return {"error": f"Error analyzing PDF: {str(e)}"}

@mcp.tool()
def smart_extract_pdf(file_path: str, lang: str = "eng+tha") -> Dict[str, Any]:
    """
    Intelligently extract content from a PDF by first analyzing whether it's a scanned image or searchable text
    Args:
        file_path: Path to the PDF file
        lang: Language code for OCR (default: "eng+tha" for English and Thai)
    Returns:
        Dictionary containing extracted content and analysis information
    """
    if not os.path.exists(file_path):
        return {"error": f"File not found at {file_path}"}
    
    try:
        # First analyze the PDF
        analysis = analyze_pdf(file_path)
        
        # Extract content based on analysis results
        if analysis.get("error"):
            return analysis
        
        result = {
            "analysis": analysis,
            "content": "",
            "extraction_method_used": ""
        }
        
        # Use recommended extraction method
        if analysis["recommended_extraction_method"] == "ocr":
            result["content"] = ocr_pdf(file_path, lang)
            result["extraction_method_used"] = "ocr"
        else:
            result["content"] = read_pdf(file_path)
            result["extraction_method_used"] = "text"
        
        return result
    except Exception as e:
        return {"error": f"Error in smart extraction: {str(e)}"}

@mcp.tool()
def read_pdf(file_path: str) -> str:
    """
    Extract text content from a PDF file
    Args:
        file_path: Path to the PDF file
    Returns:
        The extracted text content from the PDF
    """
    if not os.path.exists(file_path):
        return f"Error: File not found at {file_path}"
    
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page_num in range(len(reader.pages)):
                text += reader.pages[page_num].extract_text() + "\n\n"
            return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

@mcp.tool()
def smart_pdf_to_markdown(file_path: str, lang: str = "eng+tha") -> Dict[str, Any]:
    """
    Intelligently convert PDF to markdown by first analyzing if it's a scanned image or searchable text
    Args:
        file_path: Path to the PDF file
        lang: Language code for OCR (default: "eng+tha" for English and Thai)
    Returns:
        Dictionary containing markdown content and analysis information
    """
    if not os.path.exists(file_path):
        return {"error": f"File not found at {file_path}"}
    
    try:
        # First analyze the PDF
        analysis = analyze_pdf(file_path)
        
        # Extract content based on analysis results
        if analysis.get("error"):
            return analysis
        
        result = {
            "analysis": analysis,
            "markdown_content": "",
            "extraction_method_used": ""
        }
        
        # Use recommended extraction method
        if analysis["recommended_extraction_method"] == "ocr":
            result["markdown_content"] = pdf_to_markdown(file_path, use_ocr=True, lang=lang)
            result["extraction_method_used"] = "ocr"
        else:
            result["markdown_content"] = pdf_to_markdown(file_path, use_ocr=False)
            result["extraction_method_used"] = "text"
        
        return result
    except Exception as e:
        return {"error": f"Error in smart markdown conversion: {str(e)}"}


@mcp.tool()
def extract_pdf_page(file_path: str, page_number: int) -> str:
    """
    For non-OCR PDF, Extract text from a specific page in a PDF file
    Args:
        file_path: Path to the PDF file
        page_number: Page number to extract (0-indexed)
    Returns:
        The extracted text content from the specified page
    """
    if not os.path.exists(file_path):
        return f"Error: File not found at {file_path}"
    
    try:
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            if page_number < 0 or page_number >= len(reader.pages):
                return f"Error: Page number {page_number} is out of range (0-{len(reader.pages)-1})"
            
            return reader.pages[page_number].extract_text()
    except Exception as e:
        return f"Error extracting page: {str(e)}"

@mcp.tool()
def ocr_pdf(file_path: str, lang: str = "eng+tha") -> str:
    """
    Extract text from a PDF using OCR with support for Thai and English
    Args:
        file_path: Path to the PDF file
        lang: Language code for OCR (default: "eng+tha" for English and Thai)
    Returns:
        The extracted text content from the PDF using OCR
    """
    if not os.path.exists(file_path):
        return f"Error: File not found at {file_path}"
    
    try:
        # Open the PDF with PyMuPDF (fitz)
        doc = fitz.open(file_path)
        text = ""
        
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            
            # Render page to an image
            pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # Perform OCR
            page_text = pytesseract.image_to_string(img, lang=lang)
            text += page_text + "\n\n"
        
        doc.close()
        return text
    except Exception as e:
        return f"Error performing OCR on PDF: {str(e)}"

@mcp.tool()
def ocr_pdf_page(file_path: str, page_number: int, lang: str = "eng+tha") -> str:
    """
    Extract text from a specific page in a PDF file using OCR
    Args:
        file_path: Path to the PDF file
        page_number: Page number to extract (0-indexed)
        lang: Language code for OCR (default: "eng+tha" for English and Thai)
    Returns:
        The extracted text content from the specified page using OCR
    """
    if not os.path.exists(file_path):
        return f"Error: File not found at {file_path}"
    
    try:
        # Open the PDF with PyMuPDF (fitz)
        doc = fitz.open(file_path)
        
        if page_number < 0 or page_number >= len(doc):
            return f"Error: Page number {page_number} is out of range (0-{len(doc)-1})"
        
        # Get the specified page
        page = doc.load_page(page_number)
        
        # Render page to an image
        pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72))
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # Perform OCR
        text = pytesseract.image_to_string(img, lang=lang)
        
        doc.close()
        return text
    except Exception as e:
        return f"Error performing OCR on page: {str(e)}"


@mcp.tool()
def markdown_to_pdf(markdown_file_path: str, pdf_file_path: str) -> str:
    """
    Convert markdown content to PDF format with support for images and tables
    Args:
        markdown_file_path: Path to the markdown file
        pdf_file_path: Path to save the PDF file
    Returns:
        Path to the saved PDF file
    """
    try:
        # Read markdown content
        with open(markdown_file_path, 'r') as file:
            markdown_content = file.read()

        # Convert markdown to HTML with extensions for tables and other features
        html_content = markdown.markdown(
            markdown_content,
            extensions=['tables', 'fenced_code', 'codehilite']
        )
        
        # Get directory of markdown file for image path resolution
        markdown_dir = os.path.dirname(os.path.abspath(markdown_file_path))
        
        # Convert HTML to PDF with options for image handling
        options = {
            'enable-local-file-access': True,
            'encoding': 'UTF-8'
        }
        pdfkit.from_string(html_content, pdf_file_path, options=options, css=None)

        return pdf_file_path
    except Exception as e:
        return f"Error converting markdown to PDF: {str(e)}"
