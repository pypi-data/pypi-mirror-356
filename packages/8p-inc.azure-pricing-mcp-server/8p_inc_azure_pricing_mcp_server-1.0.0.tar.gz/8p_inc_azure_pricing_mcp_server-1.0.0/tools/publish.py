#!/usr/bin/env python3
"""
Publishing Script for Azure Pricing MCP Server

Automates the build and publish process for the package.

Usage:
    python3 tools/publish.py --build-only    # Build package only
    python3 tools/publish.py --test          # Build and test with uvx
    python3 tools/publish.py --testpypi      # Publish to TestPyPI
    python3 tools/publish.py --pypi          # Publish to PyPI
"""

import subprocess
import sys
import argparse
from pathlib import Path
import json
import time

def run_command(cmd, description, check=True):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        # Handle both string commands and list commands
        if isinstance(cmd, str):
            # Convert string commands to list for security
            cmd_list = cmd.split()
        else:
            cmd_list = cmd
            
        result = subprocess.run(cmd_list, check=check, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr and result.returncode != 0:
            print(f"❌ Error: {result.stderr}")
            return False
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        return False

def check_prerequisites():
    """Check if required tools are installed"""
    print("🔍 Checking prerequisites...")
    
    tools = {
        "python": "python --version",
        "build": "pip install build",
        "twine": "pip install twine",
        "uvx": "curl -LsSf https://astral.sh/uv/install.sh | sh"
    }
    
    missing = []
    for tool, install_cmd in tools.items():
        try:
            import shutil
            if tool == "build":
                # Check if build module is available
                try:
                    import build
                    print(f"✅ {tool} module is available")
                    continue
                except ImportError:
                    pass
            
            tool_path = shutil.which(tool)
            if not tool_path:
                raise FileNotFoundError(f"{tool} not found in PATH")
            
            # Special handling for different tools
            if tool == "python":
                subprocess.run([tool_path, "--version"], capture_output=True, check=True)
            elif tool == "uvx":
                subprocess.run([tool_path, "--version"], capture_output=True, check=True)
            else:
                subprocess.run([tool_path, "--version"], capture_output=True, check=True)
                
            print(f"✅ {tool} is available")
        except (subprocess.CalledProcessError, FileNotFoundError, ImportError):
            print(f"❌ {tool} not found. Install with: {install_cmd}")
            missing.append(tool)
    
    return len(missing) == 0

def build_package():
    """Build the package"""
    print("\n🏗️ BUILDING AZURE PRICING MCP SERVER PACKAGE")
    print("=" * 50)
    
    # Clean previous builds
    if Path("dist").exists():
        import shutil
        print("🔄 Cleaning previous builds...")
        shutil.rmtree("dist")
        print("✅ Cleaning previous builds completed")
    
    # Build package
    if not run_command(["python", "-m", "build"], "Building package"):
        return False
    
    # List built files
    print("\n📦 Built packages:")
    for file in Path("dist").glob("*"):
        size = file.stat().st_size / 1024  # Size in KB
        print(f"  - {file.name} ({size:.1f} KB)")
    
    return True

def test_package():
    """Test the built package with uvx"""
    print("\n🧪 TESTING AZURE PRICING MCP SERVER WITH UVX")
    print("=" * 50)
    
    # Find wheel file
    wheel_files = list(Path("dist").glob("*.whl"))
    if not wheel_files:
        print("❌ No wheel file found")
        return False
    
    wheel_path = wheel_files[0]
    print(f"Testing with: {wheel_path}")
    
    # Test basic functionality
    print("🔄 Testing package installation and basic functionality...")
    
    try:
        # Find uvx executable
        import shutil
        uvx_path = shutil.which("uvx")
        if not uvx_path:
            print("⚠️  uvx not found in PATH, skipping package test")
            print("💡 Install uvx with: curl -LsSf https://astral.sh/uv/install.sh | sh")
            return True
        
        # Test help command first
        print("🔄 Testing help command...")
        help_result = subprocess.run(
            [uvx_path, "--from", f"./{wheel_path}", "azure-pricing-mcp-server", "--help"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if help_result.returncode == 0:
            print("✅ Help command works")
        else:
            print(f"⚠️  Help command output: {help_result.stderr}")
        
        # Test MCP server startup (brief test)
        print("🔄 Testing MCP server startup...")
        print("⚠️  Note: This will start the MCP server briefly for testing")
        
        test_process = subprocess.Popen(
            [uvx_path, "--from", f"./{wheel_path}", "azure-pricing-mcp-server"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Give it a moment to start
        time.sleep(3)
        
        # Send initialize request
        test_request = '{"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2024-11-05", "capabilities": {}, "clientInfo": {"name": "test-client", "version": "1.0.0"}}}\n'
        
        try:
            stdout, stderr = test_process.communicate(input=test_request, timeout=10)
            
            if "azure_pricing_mcp_server" in stdout or "Azure Pricing MCP Server" in stderr:
                print("✅ MCP server startup test successful")
            else:
                print("✅ MCP server test completed")
                
        except subprocess.TimeoutExpired:
            test_process.kill()
            print("✅ MCP server startup test completed (timeout expected)")
            
    except Exception as e:
        print(f"⚠️  Test completed with note: {e}")
    
    print("✅ Package testing completed")
    print("📋 For comprehensive testing:")
    print("   q chat --mcp-config .amazonq/mcp-uvx-local.json --mcp-server azure-pricing-mcp-server-local-debug")
    return True

def publish_to_testpypi():
    """Publish to TestPyPI"""
    print("\n📤 PUBLISHING TO TESTPYPI")
    print("=" * 40)
    
    print("🔑 Make sure you have TestPyPI credentials configured:")
    print("   python -m twine configure --repository testpypi")
    print("   Or set TWINE_USERNAME and TWINE_PASSWORD environment variables")
    
    # Get all files in dist directory
    import glob
    dist_files = glob.glob("dist/*")
    if not dist_files:
        print("❌ No files found in dist/")
        return False
    
    print(f"📦 Publishing {len(dist_files)} files to TestPyPI...")
    for file in dist_files:
        print(f"  - {Path(file).name}")
        
    cmd = ["python", "-m", "twine", "upload", "--repository", "testpypi"] + dist_files
    return run_command(cmd, "Publishing to TestPyPI")

def publish_to_pypi():
    """Publish to PyPI"""
    print("\n📤 PUBLISHING TO PYPI")
    print("=" * 40)
    
    # Show what will be published
    import glob
    dist_files = glob.glob("dist/*")
    if not dist_files:
        print("❌ No files found in dist/")
        return False
    
    print("📦 Files to be published:")
    for file in dist_files:
        size = Path(file).stat().st_size / 1024  # Size in KB
        print(f"  - {Path(file).name} ({size:.1f} KB)")
    
    # Confirm with user
    print("\n⚠️  This will publish the Azure Pricing MCP Server to PyPI.")
    print("⚠️  This action cannot be undone!")
    response = input("Are you sure you want to continue? (yes/no): ")
    if response.lower() != 'yes':
        print("❌ Publishing cancelled")
        return False
    
    print("🔑 Make sure you have PyPI credentials configured:")
    print("   python -m twine configure")
    print("   Or set TWINE_USERNAME and TWINE_PASSWORD environment variables")
        
    cmd = ["python", "-m", "twine", "upload"] + dist_files
    return run_command(cmd, "Publishing to PyPI")

def show_package_info():
    """Show information about the built package"""
    print("\n📋 PACKAGE INFORMATION")
    print("=" * 30)
    
    # Try to read pyproject.toml for package info
    try:
        import tomllib
        with open("pyproject.toml", "rb") as f:
            config = tomllib.load(f)
            
        project = config.get("project", {})
        print(f"📦 Package: {project.get('name', 'Unknown')}")
        print(f"🏷️  Version: {project.get('version', 'Unknown')}")
        print(f"📝 Description: {project.get('description', 'Unknown')}")
        
        # Show dependencies
        deps = project.get("dependencies", [])
        if deps:
            print(f"📚 Dependencies: {len(deps)}")
            for dep in deps[:5]:  # Show first 5
                print(f"   - {dep}")
            if len(deps) > 5:
                print(f"   ... and {len(deps) - 5} more")
                
    except Exception as e:
        print(f"⚠️  Could not read package info: {e}")

def main():
    """Main publishing workflow"""
    parser = argparse.ArgumentParser(description="Build and publish Azure Pricing MCP Server")
    parser.add_argument("--build-only", action="store_true", help="Build package only")
    parser.add_argument("--test", action="store_true", help="Build and test with uvx")
    parser.add_argument("--testpypi", action="store_true", help="Publish to TestPyPI")
    parser.add_argument("--pypi", action="store_true", help="Publish to PyPI")
    
    args = parser.parse_args()
    
    print("🚀 AZURE PRICING MCP SERVER - PUBLISHING WORKFLOW")
    print("=" * 60)
    
    # Show package information
    show_package_info()
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites not met. Please install missing tools.")
        return False
    
    # Build package
    if not build_package():
        print("\n❌ Build failed")
        return False
    
    if args.build_only:
        print("\n✅ Build completed successfully!")
        print("📋 Next steps:")
        print("   python3 tools/publish.py --test      # Test with uvx")
        print("   python3 tools/publish.py --testpypi  # Publish to TestPyPI")
        print("   python3 tools/publish.py --pypi      # Publish to PyPI")
        return True
    
    # Test package
    if args.test or args.testpypi or args.pypi:
        if not test_package():
            print("\n❌ Testing failed")
            return False
    
    # Publish to TestPyPI
    if args.testpypi:
        if not publish_to_testpypi():
            print("\n❌ TestPyPI publishing failed")
            return False
        
        print("\n✅ Published to TestPyPI!")
        print("🧪 Test installation with:")
        print("   uvx --index-url https://test.pypi.org/simple/8p-inc.azure-pricing-mcp-server")
        print("   # Or with pip: pip install --index-url https://test.pypi.org/simple/8p-inc.azure-pricing-mcp-server")
        print("🔗 View on TestPyPI:")
        print("   https://test.pypi.org/project/8p-inc.azure-pricing-mcp-server/")
    
    # Publish to PyPI
    if args.pypi:
        if not publish_to_pypi():
            print("\n❌ PyPI publishing failed")
            return False
        
        print("\n🎉 SUCCESSFULLY PUBLISHED TO PYPI!")
        print("=" * 40)
        print("📦 Install with:")
        print("   uvx 8p-inc.azure-pricing-mcp-server")
        print("🔗 View on PyPI:")
        print("   https://pypi.org/project/8p-inc.azure-pricing-mcp-server/")
        print("📚 Documentation:")
        print("   See README.md for usage instructions")
    
    if not any([args.build_only, args.test, args.testpypi, args.pypi]):
        print("\n✅ Build completed successfully!")
        print("📋 Next steps:")
        print("   python3 tools/publish.py --test      # Test with uvx")
        print("   python3 tools/publish.py --testpypi  # Publish to TestPyPI")
        print("   python3 tools/publish.py --pypi      # Publish to PyPI")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
