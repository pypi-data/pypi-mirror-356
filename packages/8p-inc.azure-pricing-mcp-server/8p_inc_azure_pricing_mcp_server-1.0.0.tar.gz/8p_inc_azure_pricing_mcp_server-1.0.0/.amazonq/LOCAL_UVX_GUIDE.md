# Azure Pricing MCP Server - Local uvx Development Guide

## 🏠 **Local Development with uvx and Built Packages**

This guide explains how to use `uvx` to run the Azure Pricing MCP Server locally from your **built package in the `dist/` directory**, which is the proper way to test your built package before publishing.

## 📦 **Using Built Packages vs Source Code**

### **✅ Correct Approach: Built Package**
```json
{
  "command": "uvx",
  "args": ["--from", "./dist/azure_pricing_mcp_server-1.0.0-py3-none-any.whl", "azure-pricing-mcp-server"]
}
```

### **❌ Previous Approach: Source Directory**
```json
{
  "command": "uvx",
  "args": ["--from", ".", "azure-pricing-mcp-server"]
}
```

## 🎯 **Why Use Built Packages?**

### **📦 Proper Package Testing**
- **Tests the actual built package** - Same as what gets published
- **Validates build process** - Ensures packaging works correctly
- **Dependency resolution** - Tests actual package dependencies
- **Entry points verification** - Confirms console scripts work

### **🔧 Better Development Workflow**
- **Build once, test multiple times** - No repeated source parsing
- **Faster startup** - Pre-built package loads faster
- **Consistent behavior** - Matches published package exactly
- **Version testing** - Test specific built versions

## 🔧 **Available Local Configurations**

### **1. `azure-pricing-mcp-server-local-debug` 🔍**
**Purpose**: Local development with comprehensive debug logging

```json
{
  "command": "uvx",
  "args": ["--from", "./dist/azure_pricing_mcp_server-1.0.0-py3-none-any.whl", "azure-pricing-mcp-server"],
  "env": {
    "MCP_DEBUG_LOGGING": "true",
    "MCP_LOG_LEVEL": "DEBUG",
    "MCP_LOG_FORMAT": "json"
  }
}
```

**Features**:
- ✅ Runs from built wheel package
- ✅ Full debug logging with JSON format
- ✅ Extended timeout for debugging
- ✅ Tests actual packaged code

---

### **2. `azure-pricing-mcp-server-local-production` 🚀**
**Purpose**: Local testing with production-like settings

```json
{
  "command": "uvx",
  "args": ["--from", "./dist/azure_pricing_mcp_server-1.0.0-py3-none-any.whl", "azure-pricing-mcp-server"],
  "env": {
    "MCP_DEBUG_LOGGING": "false",
    "MCP_LOG_LEVEL": "INFO",
    "MCP_LOG_FORMAT": "json"
  }
}
```

**Features**:
- ✅ Production-level logging
- ✅ Structured JSON output
- ✅ Tests built package behavior
- ✅ Validates packaging for production

---

### **3. `azure-pricing-mcp-server-local-latest` 📦**
**Purpose**: Use latest built package automatically

```json
{
  "command": "uvx",
  "args": ["--from", "./dist/", "azure-pricing-mcp-server"],
  "env": {
    "MCP_DEBUG_LOGGING": "true",
    "MCP_LOG_LEVEL": "DEBUG",
    "MCP_LOG_FORMAT": "json"
  }
}
```

**Features**:
- ✅ Automatically uses latest package in dist/
- ✅ No need to specify exact filename
- ✅ Convenient for continuous building
- ✅ Always tests most recent build

---

### **3. `azure-pricing-mcp-server-local-dev` 🛠️**
**Purpose**: Active development with human-readable logs

```json
{
  "command": "uvx",
  "args": ["--from", ".", "azure-pricing-mcp-server"],
  "env": {
    "MCP_DEBUG_LOGGING": "true",
    "MCP_LOG_LEVEL": "DEBUG",
    "MCP_LOG_FORMAT": "plain",
    "CACHE_TTL_SECONDS": "300"
  }
}
```

**Features**:
- ✅ Human-readable plain text logs
- ✅ Shorter cache TTL for development
- ✅ Extended timeout for debugging
- ✅ Additional Azure API configuration

---

### **4. `azure-pricing-mcp-server-local-test` 🧪**
**Purpose**: Quick testing with console output

```json
{
  "command": "uvx",
  "args": ["--from", ".", "azure-pricing-mcp-server"],
  "env": {
    "MCP_DEBUG_LOGGING": "true",
    "MCP_LOG_LEVEL": "DEBUG",
    "MCP_LOG_FORMAT": "plain"
  }
}
```

**Features**:
- ✅ Console-only output (no log file)
- ✅ Quick startup for testing
- ✅ Human-readable format
- ✅ Full debug information

---

### **5. `azure-pricing-mcp-server-local-minimal` ⚡**
**Purpose**: Minimal logging for performance testing

```json
{
  "command": "uvx",
  "args": ["--from", ".", "azure-pricing-mcp-server"],
  "env": {
    "MCP_DEBUG_LOGGING": "false",
    "MCP_LOG_LEVEL": "WARNING",
    "MCP_LOG_FORMAT": "json"
  }
}
```

**Features**:
- ✅ Minimal performance overhead
- ✅ Only warnings and errors
- ✅ Fast response times
- ✅ Local source with minimal logging

## 🚀 **How to Use Local uvx Configurations**

### **Prerequisites**
1. **Build the package locally**:
   ```bash
   cd azure-pricing-mcp-server
   pip install build
   python -m build
   ```
   This creates files in `dist/`:
   - `azure_pricing_mcp_server-1.0.0-py3-none-any.whl` (wheel package)
   - `azure_pricing_mcp_server-1.0.0.tar.gz` (source distribution)

2. **Install uvx** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

### **Method 1: Use Specific Wheel File**
```bash
# Use specific built wheel
q chat --mcp-config .amazonq/mcp-uvx-local.json --mcp-server azure-pricing-mcp-server-local-debug
```

### **Method 2: Use Latest Built Package**
```bash
# Use latest package in dist/ directory
q chat --mcp-config .amazonq/mcp-uvx-local.json --mcp-server azure-pricing-mcp-server-local-latest
```

### **Method 3: Copy Configuration**
```bash
# Copy local config to main config
cp .amazonq/mcp-uvx-local.json .amazonq/mcp.json

# Edit to keep only the configuration you want
nano .amazonq/mcp.json
```

## 🔄 **Development Workflow**

### **1. Make Code Changes**
```bash
# Edit your Python code
nano mcp_app/azure_pricing_mcp_server/server.py
```

### **2. Build Package**
```bash
# Build the package to create new wheel
python -m build
```

### **3. Test Built Package**
```bash
# Test the newly built package
q chat --mcp-config .amazonq/mcp-uvx-local.json --mcp-server azure-pricing-mcp-server-local-latest
```

### **4. Monitor Logs**
```bash
# Watch logs in real-time
tail -f ./logs/azure-pricing-mcp-local-debug.log | jq '.'
```

This workflow ensures you're testing the **actual built package** that would be published, not just the source code.

## 🔍 **uvx Local Development Benefits**

### **🏠 Local Source Code**
- **Immediate changes** - No need to publish to PyPI
- **Debug locally** - Full access to source code
- **Rapid iteration** - Test changes immediately
- **Development flexibility** - Modify and test quickly

### **🔧 uvx Advantages**
- **Isolated environment** - Clean Python environment for each run
- **Dependency management** - Handles all dependencies automatically
- **No virtual env needed** - uvx manages Python environment
- **Consistent behavior** - Same as production uvx usage

### **📊 Comparison: Local vs Remote**

| Aspect | Local (`--from .`) | Remote (`@latest`) |
|--------|-------------------|-------------------|
| **Source** | Local directory | PyPI package |
| **Updates** | Immediate | Requires publishing |
| **Development** | Perfect | Limited |
| **Testing** | Full control | Published versions only |
| **Debugging** | Complete access | Limited |
| **Performance** | Faster startup | Network dependent |

## 🧪 **Testing Commands**

### **Validate Configuration**
```bash
# Check JSON syntax
jq empty .amazonq/mcp-uvx-local.json && echo "✅ Valid JSON" || echo "❌ Invalid JSON"

# List all local configurations
jq -r '.mcpServers | keys[]' .amazonq/mcp-uvx-local.json
```

### **Test Local Package**
```bash
# Test if uvx can find the local package
uvx --from . azure-pricing-mcp-server --help

# Test with specific configuration
uvx --from . azure-pricing-mcp-server
```

### **Debug Startup Issues**
```bash
# Run with verbose uvx output
uvx --verbose --from . azure-pricing-mcp-server

# Check package installation
uvx --from . --python-preference system azure-pricing-mcp-server
```

## 📝 **Log File Locations**

Local configurations create logs in the `./logs/` directory:

```
azure-pricing-mcp-server/
├── logs/
│   ├── azure-pricing-mcp-local-debug.log
│   ├── azure-pricing-mcp-local-production.log
│   ├── azure-pricing-mcp-local-dev.log
│   └── azure-pricing-mcp-local-minimal.log
└── .amazonq/
    ├── mcp.json
    ├── mcp-logging.json
    └── mcp-uvx-local.json
```

## 🔧 **Troubleshooting**

### **Common Issues**

#### **1. Package Not Found**
```bash
# Error: Could not find package
# Solution: Build the package first
python -m build
```

#### **2. uvx Not Found**
```bash
# Error: uvx command not found
# Solution: Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### **3. Permission Issues**
```bash
# Error: Permission denied
# Solution: Check file permissions
chmod +x .amazonq/mcp-uvx-local.json
```

### **Debug Commands**
```bash
# Check uvx installation
uvx --version

# List uvx environments
uvx list

# Clean uvx cache
uvx cache clean

# Verbose uvx execution
uvx --verbose --from . azure-pricing-mcp-server
```

## 🎯 **Best Practices**

### **Development**
- Use `local-dev` for active development
- Use `local-test` for quick testing
- Use `local-debug` for detailed debugging

### **Testing**
- Use `local-production` for production-like testing
- Use `local-minimal` for performance testing
- Monitor logs to understand behavior

### **Deployment**
- Test locally before publishing
- Use local configs for development
- Switch to remote configs for production

## 🎉 **Summary**

The `mcp-uvx-local.json` configuration enables:
- ✅ **Local development** with immediate code changes
- ✅ **Multiple testing scenarios** with different log levels
- ✅ **uvx benefits** with local source code
- ✅ **Flexible configuration** for various development needs
- ✅ **Easy switching** between local and remote versions

Perfect for development, testing, and debugging your Azure Pricing MCP Server! 🚀
