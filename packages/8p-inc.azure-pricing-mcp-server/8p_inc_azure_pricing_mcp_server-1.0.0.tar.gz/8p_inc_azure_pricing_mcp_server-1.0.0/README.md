# Azure Pricing MCP Server

A production-ready Model Context Protocol (MCP) server for Azure pricing analysis, designed for Amazon Q CLI integration.

## 🚀 Quick Start

```bash
# Install and use with Amazon Q CLI
uvx 8p-inc.azure-pricing-mcp-server
q chat
```

## 📋 Available Tools

| Tool | Purpose | Use Case |
|------|---------|----------|
| `get_quick_price` | Ultra-fast pricing estimates | Immediate cost checks |
| `get_pricing_api` | Comprehensive pricing data | Detailed analysis |
| `get_pricing_summary` | Service overviews | Service exploration |
| `compare_regions` | Regional cost comparisons | Multi-region planning |
| `get_pricing_web` | Web scraping for offers | Free tiers & specials |
| `analyze_terraform` | Terraform cost analysis | IaC cost estimation |
| `analyze_bicep` | Bicep cost analysis | ARM template costs |
| `generate_report` | Professional reports | Stakeholder presentations |
| `get_patterns` | Architecture patterns | Solution templates |
| `validate_region` | Region validation | Input verification |

## 🏗️ Architecture Patterns

Pre-built cost analysis for 6 common Azure patterns:
- **Basic Web App**: $18/month (App Service + SQL)
- **Scalable Web App**: $215/month (Load balanced + Cache)
- **Microservices**: $311/month (AKS + Containers)
- **Serverless**: Pay-per-use (Functions + Logic Apps)
- **Data Analytics**: $1,730/month (Synapse + Data Factory)
- **IoT Solution**: $279/month (IoT Hub + Stream Analytics)

## 🔧 Configuration

### Basic MCP Configuration
```json
{
  "mcpServers": {
    "azure-pricing": {
      "command": "uvx",
      "args": ["8p-inc.azure-pricing-mcp-server@latest"],
      "env": {
        "DEFAULT_CURRENCY": "USD",
        "DEFAULT_REGION": "eastus"
      }
    }
  }
}
```

### Environment Variables
- `MCP_DEBUG_LOGGING`: Enable debug logging (default: false)
- `MCP_LOG_LEVEL`: Log level (default: INFO)
- `MCP_LOG_FILE`: Optional log file path
- `DEFAULT_CURRENCY`: Default currency (default: USD)
- `DEFAULT_REGION`: Default Azure region (default: eastus)

## 🛠️ Development

```bash
# Local development
git clone <repository>
cd azure-pricing-mcp-server
python -m build
uvx --from ./dist/8p_inc_azure_pricing_mcp_server-1.0.0-py3-none-any.whl azure-pricing-mcp-server

# Publishing
python3 tools/publish.py --test      # Test locally
python3 tools/publish.py --testpypi  # Publish to TestPyPI
python3 tools/publish.py --pypi      # Publish to PyPI
```

## 📊 Features

- **Real-time Azure pricing** from official APIs
- **Infrastructure analysis** for Terraform and Bicep
- **Regional cost comparisons** across Azure regions
- **Professional reporting** in Markdown and CSV formats
- **Comprehensive logging** with structured JSON output
- **Production-ready** with full test coverage

## 🎯 Status

✅ **Production Ready** - All 10 tools functional  
✅ **MCP Compliant** - Passes protocol specifications  
✅ **Performance Optimized** - Sub-2 second responses  
✅ **Well Documented** - Complete guides available  

For detailed documentation, see [COMPREHENSIVE_GUIDE.md](COMPREHENSIVE_GUIDE.md).

## 📦 Package Info

- **Package**: `8p-inc.azure-pricing-mcp-server`
- **Version**: 1.0.0
- **Python**: 3.8+
- **License**: MIT
