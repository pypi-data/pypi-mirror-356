#!/bin/bash

# Azure Pricing MCP Server Diagnostic Script
# This script helps diagnose common issues

echo "=== Azure Pricing MCP Server Diagnostics ==="
echo ""

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "Project Root: $PROJECT_ROOT"
echo "Script Directory: $SCRIPT_DIR"
echo ""

# Check project structure
echo "=== Project Structure ==="
echo "Checking key files and directories..."

if [ -f "$PROJECT_ROOT/tools/start_server.sh" ]; then
    echo "✅ start_server.sh exists"
    if [ -x "$PROJECT_ROOT/tools/start_server.sh" ]; then
        echo "✅ start_server.sh is executable"
    else
        echo "❌ start_server.sh is not executable"
    fi
else
    echo "❌ start_server.sh not found"
fi

if [ -d "$PROJECT_ROOT/venv" ]; then
    echo "✅ Virtual environment exists"
else
    echo "❌ Virtual environment not found"
fi

if [ -d "$PROJECT_ROOT/mcp_app" ]; then
    echo "✅ mcp_app directory exists"
else
    echo "❌ mcp_app directory not found"
fi

if [ -f "$PROJECT_ROOT/.amazonq/mcp.json" ]; then
    echo "✅ MCP configuration exists"
else
    echo "❌ MCP configuration not found"
fi

if [ -d "$PROJECT_ROOT/logs" ]; then
    echo "✅ Logs directory exists"
    log_count=$(find "$PROJECT_ROOT/logs" -name "*.log" 2>/dev/null | wc -l)
    echo "📊 Log files found: $log_count"
else
    echo "⚠️  Logs directory not found (will be created automatically)"
fi

echo ""

# Check Python environment
echo "=== Python Environment ==="
if [ -d "$PROJECT_ROOT/venv" ]; then
    source "$PROJECT_ROOT/venv/bin/activate"
    echo "Python version: $(python --version)"
    echo "Python path: $(which python)"
    
    echo ""
    echo "Checking required packages..."
    
    packages=("mcp" "pydantic" "httpx" "bs4" "pytest" "pytest-asyncio")
    for package in "${packages[@]}"; do
        if python -c "import $package" 2>/dev/null; then
            version=$(python -c "import $package; print(getattr($package, '__version__', 'unknown'))" 2>/dev/null)
            echo "✅ $package ($version)"
        else
            echo "❌ $package not installed"
        fi
    done
    
    echo ""
    echo "Testing module import..."
    if python -c "import mcp_app.azure_pricing_mcp_server.server" 2>/dev/null; then
        echo "✅ Azure Pricing MCP server module can be imported"
    else
        echo "❌ Cannot import Azure Pricing MCP server module"
        echo "Error details:"
        python -c "import mcp_app.azure_pricing_mcp_server.server" 2>&1 | head -10
    fi
else
    echo "❌ Virtual environment not found"
fi

echo ""

# Check MCP configuration
echo "=== MCP Configuration ==="
if [ -f "$PROJECT_ROOT/.amazonq/mcp.json" ]; then
    echo "Configuration file contents:"
    cat "$PROJECT_ROOT/.amazonq/mcp.json" | jq '.' 2>/dev/null || cat "$PROJECT_ROOT/.amazonq/mcp.json"
    
    echo ""
    echo "Validating JSON..."
    if jq empty "$PROJECT_ROOT/.amazonq/mcp.json" 2>/dev/null; then
        echo "✅ Valid JSON"
    else
        echo "❌ Invalid JSON"
    fi
else
    echo "❌ MCP configuration file not found"
fi

echo ""

# Check environment variables
echo "=== Environment Variables ==="
echo "Current logging environment:"
echo "MCP_DEBUG_LOGGING: ${MCP_DEBUG_LOGGING:-not set}"
echo "MCP_LOG_LEVEL: ${MCP_LOG_LEVEL:-not set}"
echo "MCP_LOG_FORMAT: ${MCP_LOG_FORMAT:-not set}"
echo "MCP_LOG_FILE: ${MCP_LOG_FILE:-not set}"
echo "FASTMCP_LOG_LEVEL: ${FASTMCP_LOG_LEVEL:-not set}"
echo "DEFAULT_CURRENCY: ${DEFAULT_CURRENCY:-not set}"
echo "DEFAULT_REGION: ${DEFAULT_REGION:-not set}"

echo ""

# Check recent logs
echo "=== Recent Logs ==="
if [ -d "$PROJECT_ROOT/logs" ]; then
    recent_logs=$(find "$PROJECT_ROOT/logs" -name "*.log" -mtime -1 2>/dev/null)
    if [ -n "$recent_logs" ]; then
        echo "Recent log files (last 24 hours):"
        for log_file in $recent_logs; do
            echo "📄 $(basename "$log_file") ($(wc -l < "$log_file") lines)"
            echo "   Last modified: $(stat -f "%Sm" "$log_file")"
            echo "   Size: $(stat -f "%z bytes" "$log_file")"
            
            # Show last few lines
            echo "   Last 3 lines:"
            tail -3 "$log_file" 2>/dev/null | sed 's/^/     /'
            echo ""
        done
    else
        echo "No recent log files found"
    fi
else
    echo "No logs directory found"
fi

echo ""

# Test basic server startup
echo "=== Basic Server Test ==="
echo "Testing server startup (will timeout after 5 seconds)..."

cd "$PROJECT_ROOT"
export MCP_DEBUG_LOGGING=true
export MCP_LOG_LEVEL=DEBUG
export MCP_LOG_FILE=./logs/diagnostic-test.log

if timeout 5s ./tools/start_server.sh 2>&1 | head -10; then
    echo "✅ Server started successfully (or timed out as expected)"
else
    echo "❌ Server failed to start"
fi

# Check if diagnostic log was created
if [ -f "$PROJECT_ROOT/logs/diagnostic-test.log" ]; then
    echo ""
    echo "Diagnostic log created:"
    echo "Last 5 lines from diagnostic-test.log:"
    tail -5 "$PROJECT_ROOT/logs/diagnostic-test.log" | sed 's/^/  /'
fi

echo ""
echo "=== Diagnostics Complete ==="
echo ""
echo "Common solutions:"
echo "1. If module import fails: cd $PROJECT_ROOT && pip install -e ."
echo "2. If permissions issue: chmod +x $PROJECT_ROOT/tools/start_server.sh"
echo "3. If MCP not loading: Check Q CLI is in the correct directory"
echo "4. If no logs: Check MCP_LOG_FILE path and permissions"
