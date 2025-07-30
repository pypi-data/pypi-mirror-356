"""
arXiv Search MCP Server

An MCP server that provides search functionality for arXiv.org papers using the arXiv API.
Supports searching by terms, subject categories, date ranges, and result count limits.
"""

__version__ = "0.1.0"
__author__ = "Gavin Huang"
__email__ = "gavin@example.com"  # Replace with your actual email

from .server import mcp

__all__ = ["mcp", "__version__"]
