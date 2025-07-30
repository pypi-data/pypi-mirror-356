#!/bin/bash

# Azure Pricing MCP Server Configuration Validator
# This script validates MCP configuration files

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
AMAZONQ_DIR="$PROJECT_ROOT/.amazonq"

validate_json() {
    local file="$1"
    local name="$2"
    
    echo "Validating $name: $file"
    
    if [ ! -f "$file" ]; then
        echo "  ❌ File not found"
        return 1
    fi
    
    # Check if it's valid JSON
    if ! jq empty "$file" 2>/dev/null; then
        echo "  ❌ Invalid JSON format"
        return 1
    fi
    
    echo "  ✅ Valid JSON format"
    
    # Check for required structure
    if ! jq -e '.mcpServers' "$file" >/dev/null 2>&1; then
        echo "  ❌ Missing 'mcpServers' section"
        return 1
    fi
    
    echo "  ✅ Has 'mcpServers' section"
    
    # Count servers
    local server_count=$(jq '.mcpServers | length' "$file")
    echo "  📊 Contains $server_count server(s)"
    
    # Validate each server
    local servers=$(jq -r '.mcpServers | keys[]' "$file")
    local all_valid=true
    
    while IFS= read -r server; do
        echo "  🔍 Validating server: $server"
        
        # Check required fields
        if ! jq -e ".mcpServers.\"$server\".command" "$file" >/dev/null 2>&1; then
            echo "    ❌ Missing 'command' field"
            all_valid=false
        else
            local command=$(jq -r ".mcpServers.\"$server\".command" "$file")
            echo "    ✅ Command: $command"
        fi
        
        # Check if command file exists (relative to project root)
        local command_path="$PROJECT_ROOT/$(jq -r ".mcpServers.\"$server\".command" "$file")"
        if [ -f "$command_path" ]; then
            echo "    ✅ Command file exists"
            if [ -x "$command_path" ]; then
                echo "    ✅ Command file is executable"
            else
                echo "    ⚠️  Command file is not executable"
            fi
        else
            echo "    ❌ Command file not found: $command_path"
            all_valid=false
        fi
        
        # Check environment variables
        if jq -e ".mcpServers.\"$server\".env" "$file" >/dev/null 2>&1; then
            local env_count=$(jq ".mcpServers.\"$server\".env | length" "$file")
            echo "    ✅ Environment variables: $env_count"
            
            # Check for logging-specific env vars
            local log_vars=("MCP_DEBUG_LOGGING" "MCP_LOG_LEVEL" "MCP_LOG_FORMAT" "MCP_LOG_FILE")
            for var in "${log_vars[@]}"; do
                if jq -e ".mcpServers.\"$server\".env.\"$var\"" "$file" >/dev/null 2>&1; then
                    local value=$(jq -r ".mcpServers.\"$server\".env.\"$var\"" "$file")
                    echo "    📝 $var: $value"
                fi
            done
        fi
        
        # Check timeout
        if jq -e ".mcpServers.\"$server\".timeout" "$file" >/dev/null 2>&1; then
            local timeout=$(jq -r ".mcpServers.\"$server\".timeout" "$file")
            echo "    ⏱️  Timeout: ${timeout}ms"
        fi
        
        echo ""
    done <<< "$servers"
    
    if [ "$all_valid" = true ]; then
        echo "  ✅ All servers are valid"
        return 0
    else
        echo "  ❌ Some servers have issues"
        return 1
    fi
}

echo "=== Azure Pricing MCP Server Configuration Validator ==="
echo ""

# Validate main configuration
if [ -f "$AMAZONQ_DIR/mcp.json" ]; then
    validate_json "$AMAZONQ_DIR/mcp.json" "Main Configuration"
    echo ""
else
    echo "Main configuration not found: $AMAZONQ_DIR/mcp.json"
    echo ""
fi

# Validate logging configuration
if [ -f "$AMAZONQ_DIR/mcp-logging.json" ]; then
    validate_json "$AMAZONQ_DIR/mcp-logging.json" "Logging Configuration"
    echo ""
else
    echo "Logging configuration not found: $AMAZONQ_DIR/mcp-logging.json"
    echo ""
fi

# Check logs directory
echo "Checking logs directory:"
if [ -d "$PROJECT_ROOT/logs" ]; then
    echo "  ✅ Logs directory exists: $PROJECT_ROOT/logs"
    local log_count=$(find "$PROJECT_ROOT/logs" -name "*.log" | wc -l)
    echo "  📊 Log files found: $log_count"
    
    if [ $log_count -gt 0 ]; then
        echo "  📄 Log files:"
        find "$PROJECT_ROOT/logs" -name "*.log" -exec basename {} \; | sed 's/^/    - /'
    fi
else
    echo "  ⚠️  Logs directory not found (will be created automatically)"
fi

echo ""
echo "=== Validation Complete ==="
