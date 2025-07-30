#!/bin/bash

# Azure Pricing MCP Server Configuration Switcher
# This script helps switch between different logging configurations

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
AMAZONQ_DIR="$PROJECT_ROOT/.amazonq"
MAIN_CONFIG="$AMAZONQ_DIR/mcp.json"
LOGGING_CONFIG="$AMAZONQ_DIR/mcp-logging.json"
LOCAL_CONFIG="$AMAZONQ_DIR/mcp-uvx-local.json"
BACKUP_CONFIG="$AMAZONQ_DIR/mcp.json.backup"

# Available configurations
declare -A CONFIGS=(
    ["debug"]="azure-pricing-mcp-server-debug"
    ["production"]="azure-pricing-mcp-server-production"
    ["troubleshoot"]="azure-pricing-mcp-server-troubleshoot"
    ["console"]="azure-pricing-mcp-server-console-only"
    ["minimal"]="azure-pricing-mcp-server-minimal"
    ["local-debug"]="azure-pricing-mcp-server-local-debug"
    ["local-production"]="azure-pricing-mcp-server-local-production"
    ["local-dev"]="azure-pricing-mcp-server-local-dev"
    ["local-test"]="azure-pricing-mcp-server-local-test"
    ["local-minimal"]="azure-pricing-mcp-server-local-minimal"
)

# Configuration sources
declare -A CONFIG_SOURCES=(
    ["debug"]="$LOGGING_CONFIG"
    ["production"]="$LOGGING_CONFIG"
    ["troubleshoot"]="$LOGGING_CONFIG"
    ["console"]="$LOGGING_CONFIG"
    ["minimal"]="$LOGGING_CONFIG"
    ["local-debug"]="$LOCAL_CONFIG"
    ["local-production"]="$LOCAL_CONFIG"
    ["local-dev"]="$LOCAL_CONFIG"
    ["local-test"]="$LOCAL_CONFIG"
    ["local-minimal"]="$LOCAL_CONFIG"
)

show_help() {
    echo "Azure Pricing MCP Server Configuration Switcher"
    echo ""
    echo "Usage: $0 [COMMAND] [CONFIG_NAME]"
    echo ""
    echo "Commands:"
    echo "  switch <config>    Switch to a specific configuration"
    echo "  list              List available configurations"
    echo "  current           Show current configuration"
    echo "  backup            Backup current configuration"
    echo "  restore           Restore from backup"
    echo "  help              Show this help message"
    echo ""
    echo "Available configurations:"
    echo "  🌐 Remote (PyPI) configurations:"
    echo "    debug             Full debug logging with JSON format (uvx)"
    echo "    production        Production logging with JSON format (uvx)"
    echo "    troubleshoot      Debug logging with plain text format (uvx)"
    echo "    console           Console-only logging with plain text (uvx)"
    echo "    minimal           Minimal logging (warnings/errors only) (uvx)"
    echo ""
    echo "  🏠 Local development configurations:"
    echo "    local-debug       Local debug with comprehensive logging"
    echo "    local-production  Local production-like testing"
    echo "    local-dev         Local development with plain text logs"
    echo "    local-test        Local quick testing (console only)"
    echo "    local-minimal     Local minimal logging"
    echo ""
    echo "Examples:"
    echo "  $0 switch debug          # Use remote PyPI package"
    echo "  $0 switch local-dev      # Use local source code"
    echo "  $0 list"
    echo "  $0 current"
    echo ""
    echo "Note: All configurations use 'uvx' for automatic package management"
}

list_configs() {
    echo "Available configurations (using uvx):"
    echo ""
    for key in "${!CONFIGS[@]}"; do
        server_name="${CONFIGS[$key]}"
        echo "  $key -> $server_name"
        
        # Extract key settings from the logging config
        if [ -f "$LOGGING_CONFIG" ]; then
            debug_logging=$(jq -r ".mcpServers.\"$server_name\".env.MCP_DEBUG_LOGGING // \"not set\"" "$LOGGING_CONFIG")
            log_level=$(jq -r ".mcpServers.\"$server_name\".env.MCP_LOG_LEVEL // \"not set\"" "$LOGGING_CONFIG")
            log_format=$(jq -r ".mcpServers.\"$server_name\".env.MCP_LOG_FORMAT // \"not set\"" "$LOGGING_CONFIG")
            log_file=$(jq -r ".mcpServers.\"$server_name\".env.MCP_LOG_FILE // \"console only\"" "$LOGGING_CONFIG")
            command=$(jq -r ".mcpServers.\"$server_name\".command // \"not set\"" "$LOGGING_CONFIG")
            
            echo "    Command: $command"
            echo "    Debug: $debug_logging, Level: $log_level, Format: $log_format"
            echo "    Output: $log_file"
            echo ""
        fi
    done
}

show_current() {
    if [ ! -f "$MAIN_CONFIG" ]; then
        echo "No current configuration found at $MAIN_CONFIG"
        return 1
    fi
    
    echo "Current configuration:"
    echo ""
    
    # Get the first server name from the current config
    server_name=$(jq -r '.mcpServers | keys[0]' "$MAIN_CONFIG")
    
    if [ "$server_name" != "null" ]; then
        echo "Server: $server_name"
        
        # Show key settings
        command=$(jq -r ".mcpServers.\"$server_name\".command // \"not set\"" "$MAIN_CONFIG")
        args=$(jq -r ".mcpServers.\"$server_name\".args // [] | join(\" \")" "$MAIN_CONFIG")
        debug_logging=$(jq -r ".mcpServers.\"$server_name\".env.MCP_DEBUG_LOGGING // \"not set\"" "$MAIN_CONFIG")
        log_level=$(jq -r ".mcpServers.\"$server_name\".env.MCP_LOG_LEVEL // \"not set\"" "$MAIN_CONFIG")
        log_format=$(jq -r ".mcpServers.\"$server_name\".env.MCP_LOG_FORMAT // \"not set\"" "$MAIN_CONFIG")
        log_file=$(jq -r ".mcpServers.\"$server_name\".env.MCP_LOG_FILE // \"console only\"" "$MAIN_CONFIG")
        timeout=$(jq -r ".mcpServers.\"$server_name\".timeout // \"not set\"" "$MAIN_CONFIG")
        
        echo "Command: $command $args"
        echo "Debug Logging: $debug_logging"
        echo "Log Level: $log_level"
        echo "Log Format: $log_format"
        echo "Log File: $log_file"
        echo "Timeout: ${timeout}ms"
        
        if [ "$command" = "uvx" ]; then
            echo "✅ Using uvx for automatic package management"
        else
            echo "⚠️  Not using uvx - consider switching to uvx-based configuration"
        fi
    else
        echo "No servers configured"
    fi
}

backup_config() {
    if [ -f "$MAIN_CONFIG" ]; then
        cp "$MAIN_CONFIG" "$BACKUP_CONFIG"
        echo "Configuration backed up to $BACKUP_CONFIG"
    else
        echo "No configuration to backup"
        return 1
    fi
}

restore_config() {
    if [ -f "$BACKUP_CONFIG" ]; then
        cp "$BACKUP_CONFIG" "$MAIN_CONFIG"
        echo "Configuration restored from backup"
        show_current
    else
        echo "No backup configuration found"
        return 1
    fi
}

switch_config() {
    local config_key="$1"
    
    if [ -z "$config_key" ]; then
        echo "Error: Configuration name required"
        echo "Use '$0 list' to see available configurations"
        return 1
    fi
    
    if [ -z "${CONFIGS[$config_key]}" ]; then
        echo "Error: Unknown configuration '$config_key'"
        echo "Use '$0 list' to see available configurations"
        return 1
    fi
    
    local server_name="${CONFIGS[$config_key]}"
    local config_file="${CONFIG_SOURCES[$config_key]}"
    
    if [ ! -f "$config_file" ]; then
        echo "Error: Configuration file not found: $config_file"
        if [[ "$config_key" == local-* ]]; then
            echo "Hint: Local configurations require mcp-uvx-local.json"
            echo "      Make sure you have built the package locally"
        fi
        return 1
    fi
    
    # Check if the server exists in the config
    if ! jq -e ".mcpServers.\"$server_name\"" "$config_file" > /dev/null; then
        echo "Error: Server '$server_name' not found in configuration file"
        return 1
    fi
    
    # Backup current config if it exists
    if [ -f "$MAIN_CONFIG" ]; then
        backup_config
    fi
    
    # Determine configuration type
    local config_type="remote (PyPI)"
    if [[ "$config_key" == local-* ]]; then
        config_type="local (source code)"
    fi
    
    # Create new config with just the selected server
    echo "Switching to configuration: $config_key ($server_name)"
    echo "Configuration type: $config_type"
    echo "Using uvx for automatic package management..."
    
    jq "{
        mcpServers: {
            \"azure-pricing-mcp-server\": .mcpServers.\"$server_name\"
        }
    }" "$config_file" > "$MAIN_CONFIG"
    
    if [ $? -eq 0 ]; then
        echo "✅ Configuration switched successfully!"
        echo ""
        show_current
        
        # Create logs directory if it doesn't exist
        mkdir -p "$PROJECT_ROOT/logs"
        
        echo ""
        echo "🚀 Ready to use:"
        echo "   q chat"
        echo ""
        echo "📊 Monitor logs:"
        log_file=$(jq -r ".mcpServers.\"azure-pricing-mcp-server\".env.MCP_LOG_FILE // \"\"" "$MAIN_CONFIG")
        if [ -n "$log_file" ] && [ "$log_file" != "null" ]; then
            echo "   tail -f $log_file"
            if [[ "$log_file" == *".json"* ]] || jq -r ".mcpServers.\"azure-pricing-mcp-server\".env.MCP_LOG_FORMAT" "$MAIN_CONFIG" | grep -q "json"; then
                echo "   tail -f $log_file | jq '.'"
            fi
        else
            echo "   (Console output only - no log file configured)"
        fi
        
        echo ""
        echo "✨ Benefits of uvx:"
        echo "   • Automatic package management"
        echo "   • Always uses latest version"
        echo "   • No local installation required"
        echo "   • Isolated Python environment"
    else
        echo "❌ Error: Failed to switch configuration"
        return 1
    fi
}

# Main script logic
case "${1:-help}" in
    "switch")
        switch_config "$2"
        ;;
    "list")
        list_configs
        ;;
    "current")
        show_current
        ;;
    "backup")
        backup_config
        ;;
    "restore")
        restore_config
        ;;
    "help"|*)
        show_help
        ;;
esac
