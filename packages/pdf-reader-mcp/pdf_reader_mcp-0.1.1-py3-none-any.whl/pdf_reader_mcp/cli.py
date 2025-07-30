#!/usr/bin/env python3
"""
Command-line interface for PDF Reader MCP Server
"""

import sys
import argparse
from .server import mcp


def main():
    """Main entry point for the PDF Reader MCP Server CLI."""
    parser = argparse.ArgumentParser(
        description="PDF Reader MCP Server - A powerful MCP server for PDF processing"
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="stdio",
        help="Transport method to use (default: stdio)"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )
    
    args = parser.parse_args()
    
    try:
        # Run the MCP server
        mcp.run(transport=args.transport)
    except KeyboardInterrupt:
        print("\nShutting down PDF Reader MCP Server...")
        sys.exit(0)
    except Exception as e:
        print(f"Error running PDF Reader MCP Server: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
