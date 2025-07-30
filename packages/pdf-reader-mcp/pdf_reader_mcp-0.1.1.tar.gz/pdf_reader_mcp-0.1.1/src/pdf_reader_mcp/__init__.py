"""
PDF Reader MCP Server

A powerful Model Context Protocol (MCP) server for comprehensive PDF processing.
"""

__version__ = "0.1.0"
__author__ = "Apisak Musikapan"
__email__ = "apisak13@gmail.com"

from .server import mcp
from .cli import main

__all__ = ["mcp", "main"]
