"""
Arxiv MCP Server initialization
"""

from . import server
import asyncio


def main():
    """Main entry point for the package."""
    asyncio.run(server.main())
    # print("hello world222")


__all__ = ["main", "server"]