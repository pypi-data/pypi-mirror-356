# 🧪 Azure Pricing MCP Server - Testing Guide

This directory contains the complete test suite for the Azure Pricing MCP Server. Tests are organized into categories for better maintainability and targeted testing.

## 📁 Test Structure

```
tests/
├── fixtures/           # Test utilities and mock data
├── integration/        # Multi-component integration tests
├── unit/              # Individual component unit tests
├── test_helpers.py    # Helper function tests
└── README.md          # This file
```

## 🚀 Quick Start

### **Prerequisites**
```bash
# Ensure you're in the project root
cd azure-pricing-mcp-server

# Activate virtual environment
source venv/bin/activate

# Install dependencies (if not already done)
pip install -e .
```

### **Run All Tests**
```bash
pytest
```

## 📊 Test Categories

### **🔧 Unit Tests** (`tests/unit/`)
Test individual components in isolation:

```bash
# Run all unit tests
pytest tests/unit/

# Run specific unit test files
pytest tests/unit/test_server.py
pytest tests/unit/test_api.py
pytest tests/unit/test_web_scraping.py
```

**Available Unit Tests:**
- `test_api.py` - Azure API functionality
- `test_server.py` - MCP server components
- `test_web_scraping.py` - Web scraping functionality
- `test_architecture_patterns.py` - Architecture pattern generation
- `test_report_generation.py` - Cost report generation
- `test_quick_price.py` - Quick pricing functionality
- `test_multiple_services.py` - Multi-service pricing

### **🔗 Integration Tests** (`tests/integration/`)
Test multiple components working together:

```bash
# Run all integration tests
pytest tests/integration/

# Run specific integration test files
pytest tests/integration/test_complete_system.py
pytest tests/integration/test_end_to_end.py
```

**Available Integration Tests:**
- `test_combined_pricing.py` - Combined pricing workflows
- `test_complete_system.py` - Full system functionality
- `test_end_to_end.py` - End-to-end user workflows
- `test_infrastructure.py` - Infrastructure analysis
- `test_infrastructure_pricing.py` - Infrastructure cost analysis
- `test_optimized.py` - Response optimization tests

### **🧪 Fixtures** (`tests/fixtures/`)
Test utilities and debugging tools:

```bash
# Run fixture tests
pytest tests/fixtures/

# Use fixtures in development
python tests/fixtures/debug_bicep.py
```

**Available Fixtures:**
- `test_mcp_server.py` - MCP server test utilities
- `debug_bicep.py` - Bicep debugging tools

## 🎯 Common Testing Scenarios

### **Test Specific Functionality**
```bash
# Test Azure pricing API
pytest tests/unit/test_api.py -v

# Test MCP server functionality
pytest tests/unit/test_server.py -v

# Test complete system integration
pytest tests/integration/test_complete_system.py -v
```

### **Test with Coverage**
```bash
# Run tests with coverage report
pytest --cov=mcp_app.azure_pricing_mcp_server

# Generate detailed coverage report
pytest --cov=mcp_app.azure_pricing_mcp_server --cov-report=html

# View coverage report
open htmlcov/index.html
```

### **Test with Verbose Output**
```bash
# Verbose output for debugging
pytest -v

# Extra verbose with output capture disabled
pytest -v -s

# Show local variables on failures
pytest -v --tb=long
```

### **Test Specific Patterns**
```bash
# Run tests matching a pattern
pytest -k "test_pricing"
pytest -k "test_server"
pytest -k "integration"

# Run tests by markers (if configured)
pytest -m "slow"
pytest -m "api"
```

## 🔧 Advanced Testing Options

### **Parallel Testing**
```bash
# Install pytest-xdist for parallel execution
pip install pytest-xdist

# Run tests in parallel
pytest -n auto
pytest -n 4  # Use 4 processes
```

### **Test Selection**
```bash
# Run only failed tests from last run
pytest --lf

# Run failed tests first, then remaining
pytest --ff

# Stop on first failure
pytest -x

# Stop after N failures
pytest --maxfail=3
```

### **Output Control**
```bash
# Quiet output (less verbose)
pytest -q

# Show test durations
pytest --durations=10

# Show slowest tests
pytest --durations=0
```

## 🐛 Debugging Tests

### **Debug Failing Tests**
```bash
# Run with Python debugger
pytest --pdb

# Drop into debugger on failures
pytest --pdb-trace

# Show local variables in tracebacks
pytest --tb=long
```

### **Capture Output**
```bash
# Show print statements
pytest -s

# Capture and show output on failures only
pytest --capture=no
```

### **Test Specific Functions**
```bash
# Run specific test function
pytest tests/unit/test_server.py::test_server_initialization

# Run specific test class
pytest tests/test_helpers.py::TestHelperFunctions
```

## 📈 Performance Testing

### **Measure Test Performance**
```bash
# Show test durations
pytest --durations=10

# Profile test execution
pytest --profile

# Benchmark tests (if pytest-benchmark installed)
pytest --benchmark-only
```

## 🔍 Test Discovery

### **List All Tests**
```bash
# Show all discoverable tests
pytest --collect-only

# Show tests in specific directory
pytest tests/unit/ --collect-only

# Count total tests
pytest --collect-only -q | grep -c "test session starts"
```

## 🛠️ Configuration

### **pytest.ini Configuration**
The project uses configuration in `pyproject.toml`:

```toml
[tool.pytest.ini_options]
addopts = "--cov=mcp_app.azure_pricing_mcp_server --cov-report=term-missing"
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
```

### **Custom Configuration**
```bash
# Override configuration
pytest --cov-report=html --cov-report=term

# Use different test paths
pytest custom_tests/

# Custom markers
pytest -m "not slow"
```

## 🚨 Troubleshooting

### **Common Issues**

#### **Import Errors**
```bash
# Ensure you're in project root
cd azure-pricing-mcp-server

# Check Python path
python -c "import sys; print(sys.path)"

# Install in development mode
pip install -e .
```

#### **Missing Dependencies**
```bash
# Install test dependencies
pip install pytest pytest-cov pytest-asyncio

# Install all dependencies
pip install -e .[dev]
```

#### **Virtual Environment Issues**
```bash
# Activate virtual environment
source venv/bin/activate

# Verify environment
which python
which pytest
```

### **Environment Variables**
```bash
# Set test environment variables
export FASTMCP_LOG_LEVEL=DEBUG
export DEFAULT_CURRENCY=USD
export DEFAULT_REGION=eastus

# Run tests with environment
FASTMCP_LOG_LEVEL=DEBUG pytest tests/
```

## 📊 Test Reports

### **Generate Reports**
```bash
# HTML coverage report
pytest --cov=mcp_app.azure_pricing_mcp_server --cov-report=html

# XML coverage report (for CI/CD)
pytest --cov=mcp_app.azure_pricing_mcp_server --cov-report=xml

# JSON report
pytest --json-report --json-report-file=report.json
```

### **View Reports**
```bash
# Open HTML coverage report
open htmlcov/index.html

# View terminal coverage
pytest --cov=mcp_app.azure_pricing_mcp_server --cov-report=term-missing
```

## 🎯 Best Practices

### **Writing Tests**
- Use descriptive test names
- Test one thing per test function
- Use fixtures for common setup
- Mock external dependencies
- Test both success and failure cases

### **Running Tests**
- Run tests frequently during development
- Use coverage to identify untested code
- Run full test suite before commits
- Use parallel execution for large test suites

### **Debugging**
- Use `pytest -s` to see print statements
- Use `pytest --pdb` to debug failures
- Add `import pdb; pdb.set_trace()` for breakpoints
- Check test logs for detailed error information

## 📞 Getting Help

### **Pytest Documentation**
- [Pytest Official Docs](https://docs.pytest.org/)
- [Pytest Good Practices](https://docs.pytest.org/en/stable/explanation/goodpractices.html)

### **Project-Specific Help**
```bash
# Show pytest help
pytest --help

# Show available fixtures
pytest --fixtures

# Show markers
pytest --markers
```

---

## 🎉 Happy Testing!

This test suite ensures the Azure Pricing MCP Server works correctly across all components and use cases. Regular testing helps maintain code quality and catch issues early.

For questions or issues with testing, refer to the main project documentation or create an issue in the project repository.

*Last updated: June 19, 2025*
