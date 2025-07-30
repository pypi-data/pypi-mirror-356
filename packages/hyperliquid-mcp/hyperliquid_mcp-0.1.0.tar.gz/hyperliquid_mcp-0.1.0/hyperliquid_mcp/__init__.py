"""
Hyperliquid MCP Server

A Model Context Protocol (MCP) server for interacting with Hyperliquid DEX.
Provides tools for trading, account management, and market data access.
"""

from .server import mcp
from .version import __version__

__all__ = ["mcp", "__version__"]