#!/usr/bin/env python3
"""Test if tools are properly registered in the MCP server."""

import asyncio
import sys
from pathlib import Path

# Add the parent directory to the path so we can import the modules
sys.path.insert(0, str(Path(__file__).parent.parent))

async def test_tools_registration():
    """Test if tools are properly registered."""
    
    print("=== Tools Registration Test ===")
    
    try:
        # Import the server module
        from mcp_app.azure_pricing_mcp_server import server
        
        print("✅ Server module imported successfully")
        
        # Check if mcp instance exists
        if hasattr(server, 'mcp'):
            mcp_instance = server.mcp
            print("✅ MCP instance found")
            
            # Try to list tools using the MCP instance method
            try:
                tools_result = await mcp_instance.list_tools()
                
                # Handle different return types
                if hasattr(tools_result, 'tools'):
                    tools_list = tools_result.tools
                elif isinstance(tools_result, list):
                    tools_list = tools_result
                else:
                    tools_list = []
                
                print(f"✅ Tools list retrieved: {len(tools_list)} tools found")
                
                print("\n📋 Registered tools:")
                for i, tool in enumerate(tools_list, 1):
                    tool_name = tool.name if hasattr(tool, 'name') else str(tool)
                    print(f"   {i}. {tool_name}")
                    
                    if hasattr(tool, 'description') and tool.description:
                        desc = tool.description[:80] + "..." if len(tool.description) > 80 else tool.description
                        print(f"      Description: {desc}")
                    
                    # Show input schema if available
                    if hasattr(tool, 'inputSchema') and tool.inputSchema:
                        properties = tool.inputSchema.get('properties', {})
                        if properties:
                            print(f"      Parameters: {', '.join(properties.keys())}")
                
                # Test calling a specific tool
                validate_tool_found = any(
                    (tool.name if hasattr(tool, 'name') else str(tool)) == 'validate_azure_region' 
                    for tool in tools_list
                )
                
                if validate_tool_found:
                    print(f"\n🧪 Testing 'validate_azure_region' tool...")
                    try:
                        result = await mcp_instance.call_tool('validate_azure_region', {'region': 'eastus'})
                        print(f"✅ Tool call successful: {result}")
                    except Exception as e:
                        print(f"❌ Tool call failed: {e}")
                else:
                    print(f"\n❌ Test tool 'validate_azure_region' not found")
                    
            except Exception as e:
                print(f"❌ Error listing tools: {e}")
                import traceback
                traceback.print_exc()
                
        else:
            print("❌ No MCP instance found in server module")
            
    except Exception as e:
        print(f"❌ Error testing tools registration: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n=== Test Complete ===")


if __name__ == "__main__":
    asyncio.run(test_tools_registration())
