#!/usr/bin/env python3
"""Test script to start the MCP server for testing."""

import os
import sys
import logging

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Set up environment
os.environ['PYTHONPATH'] = project_root
os.environ['FASTMCP_LOG_LEVEL'] = 'INFO'
os.environ['DEFAULT_CURRENCY'] = 'USD'
os.environ['DEFAULT_REGION'] = 'eastus'

# Import and run the server
from mcp_app.azure_pricing_mcp_server.server import main

if __name__ == '__main__':
    print("Starting Azure Pricing MCP Server...")
    print(f"Project root: {project_root}")
    print(f"Python path: {sys.path[0]}")
    
    try:
        main()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")
        sys.exit(1)
