#!/usr/bin/env python3
"""Test script to demonstrate Azure Pricing MCP Server logging functionality."""

import asyncio
import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_app.azure_pricing_mcp_server.logging_config import mcp_logger


async def test_logging():
    """Test the logging functionality with different scenarios."""
    
    print("=== Azure Pricing MCP Server Logging Test ===")
    print(f"Debug Logging: {os.getenv('MCP_DEBUG_LOGGING', 'false')}")
    print(f"Log Level: {os.getenv('MCP_LOG_LEVEL', 'INFO')}")
    print(f"Log Format: {os.getenv('MCP_LOG_FORMAT', 'json')}")
    print(f"Log File: {os.getenv('MCP_LOG_FILE', 'console only')}")
    print("=" * 50)
    
    # Test basic logging levels
    mcp_logger.debug("This is a debug message")
    mcp_logger.info("This is an info message")
    mcp_logger.warning("This is a warning message")
    mcp_logger.error("This is an error message")
    
    # Test request logging
    mcp_logger.log_request("test_tool", {
        "service_name": "Virtual Machines",
        "region": "eastus",
        "currency": "USD"
    }, {"user_id": "test_user"})
    
    # Test response logging
    mcp_logger.log_response("test_tool", {
        "status": "success",
        "data": {"price": 0.096, "unit": "hour"},
        "count": 1
    }, 1250.5, {"user_id": "test_user"})
    
    # Test internal process logging
    mcp_logger.log_internal_process("data_processing", {
        "input_records": 100,
        "filtered_records": 85,
        "processing_time_ms": 45.2
    })
    
    # Test error logging with exception
    try:
        raise ValueError("This is a test exception")
    except Exception as e:
        mcp_logger.error(f"Test exception caught: {e}", exc_info=True)
    
    print("\n=== Logging Test Complete ===")
    print("Check your console output and log file (if configured)")


if __name__ == "__main__":
    # Set some test environment variables if not already set
    if not os.getenv('MCP_DEBUG_LOGGING'):
        os.environ['MCP_DEBUG_LOGGING'] = 'true'
    if not os.getenv('MCP_LOG_LEVEL'):
        os.environ['MCP_LOG_LEVEL'] = 'DEBUG'
    if not os.getenv('MCP_LOG_FORMAT'):
        os.environ['MCP_LOG_FORMAT'] = 'plain'
    
    asyncio.run(test_logging())
