#!/bin/bash

# Azure Pricing MCP Server Startup Script
# This script activates the virtual environment and starts the MCP server

# Enable error handling
set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Go up one level to the project root
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Set default logging environment variables if not already set
export MCP_DEBUG_LOGGING="${MCP_DEBUG_LOGGING:-false}"
export MCP_LOG_LEVEL="${MCP_LOG_LEVEL:-INFO}"
export MCP_LOG_FORMAT="${MCP_LOG_FORMAT:-json}"
export FASTMCP_LOG_LEVEL="${FASTMCP_LOG_LEVEL:-INFO}"
export DEFAULT_CURRENCY="${DEFAULT_CURRENCY:-USD}"
export DEFAULT_REGION="${DEFAULT_REGION:-eastus}"

# Create logs directory if it doesn't exist
mkdir -p "$PROJECT_ROOT/logs"

# Optional: Set log file if MCP_LOG_FILE is provided
if [ -n "$MCP_LOG_FILE" ]; then
    # If it's a relative path, make it relative to project root
    if [[ "$MCP_LOG_FILE" != /* ]]; then
        export MCP_LOG_FILE="$PROJECT_ROOT/$MCP_LOG_FILE"
    fi
    echo "Logging to file: $MCP_LOG_FILE" >&2
    
    # Create log file directory if it doesn't exist
    mkdir -p "$(dirname "$MCP_LOG_FILE")"
fi

# Print current logging configuration to stderr (so it doesn't interfere with MCP protocol)
echo "=== Azure Pricing MCP Server Startup ===" >&2
echo "Project Root: $PROJECT_ROOT" >&2
echo "Debug Logging: $MCP_DEBUG_LOGGING" >&2
echo "Log Level: $MCP_LOG_LEVEL" >&2
echo "Log Format: $MCP_LOG_FORMAT" >&2
echo "Log File: ${MCP_LOG_FILE:-console only}" >&2
echo "Default Currency: $DEFAULT_CURRENCY" >&2
echo "Default Region: $DEFAULT_REGION" >&2
echo "========================================" >&2

# Check if virtual environment exists
if [ ! -d "$PROJECT_ROOT/venv" ]; then
    echo "Error: Virtual environment not found at $PROJECT_ROOT/venv" >&2
    echo "Please create a virtual environment first:" >&2
    echo "  cd $PROJECT_ROOT && python -m venv venv" >&2
    echo "  source venv/bin/activate && pip install -e ." >&2
    exit 1
fi

# Activate the virtual environment
echo "Activating virtual environment..." >&2
source "$PROJECT_ROOT/venv/bin/activate"

# Change to project root directory
cd "$PROJECT_ROOT"

# Check if the module can be imported
echo "Testing module import..." >&2
if ! python -c "import mcp_app.azure_pricing_mcp_server.server" 2>/dev/null; then
    echo "Error: Cannot import the Azure Pricing MCP server module" >&2
    echo "Please install the package:" >&2
    echo "  cd $PROJECT_ROOT && pip install -e ." >&2
    exit 1
fi

echo "Starting Azure Pricing MCP Server..." >&2

# Start the MCP server using the Python module
exec python -m mcp_app.azure_pricing_mcp_server.server
