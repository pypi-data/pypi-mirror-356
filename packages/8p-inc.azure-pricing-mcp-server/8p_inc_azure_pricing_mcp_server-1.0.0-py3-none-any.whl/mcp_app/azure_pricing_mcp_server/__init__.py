"""Azure Pricing MCP Server.

This module provides a Model Context Protocol (MCP) server for Azure pricing analysis.
It integrates with Azure's Retail Prices API to provide comprehensive cost analysis
and pricing information for Azure services.
"""

__version__ = '1.0.0'
__author__ = '8P Inc'
__email__ = 'azure-pricing-mcp@8p-inc.com'

from .server import main

__all__ = ['main']
