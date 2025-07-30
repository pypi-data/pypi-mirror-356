#!/usr/bin/env python3
"""Test script to verify MCP server functionality."""

import asyncio
import sys
from mcp_app.azure_pricing_mcp_server.server import get_azure_pricing_from_api, compare_regional_pricing, validate_azure_region


async def test_mcp_tools():
    """Test MCP server tools."""
    print("Testing Azure Pricing MCP Server tools...")
    
    try:
        # Test get_azure_pricing_from_api
        print("\n1. Testing get_azure_pricing_from_api...")
        result = await get_azure_pricing_from_api(
            service_name="Virtual Machines",
            region="eastus",
            limit=5
        )
        
        if result['status'] == 'success':
            print(f"✓ Successfully retrieved pricing data")
            print(f"  - Total items: {result['data']['summary']['total_items']}")
            print(f"  - Unique services: {result['data']['summary']['unique_services']}")
            print(f"  - Currency: {result['data']['summary']['currency']}")
        else:
            print(f"❌ Failed: {result.get('error', 'Unknown error')}")
            return False
        
        # Test compare_regional_pricing
        print("\n2. Testing compare_regional_pricing...")
        result = await compare_regional_pricing(
            service_name="Virtual Machines",
            regions=["eastus", "westeurope"],
            sku_name="D2s v3"
        )
        
        if result['status'] == 'success':
            print(f"✓ Successfully compared regional pricing")
            comparison = result['data']
            print(f"  - Regions compared: {comparison['summary']['total_regions']}")
            print(f"  - Regions with data: {comparison['summary']['regions_with_data']}")
            if comparison['summary']['cheapest_region']:
                cheapest = comparison['summary']['cheapest_region']
                print(f"  - Cheapest region: {cheapest['region']} (${cheapest['average_price']:.4f})")
        else:
            print(f"❌ Failed: {result.get('error', 'Unknown error')}")
            return False
        
        # Test validate_azure_region
        print("\n3. Testing validate_azure_region...")
        result = await validate_azure_region("eastus")
        
        if result['status'] == 'success':
            print(f"✓ Region validation working")
            print(f"  - eastus is valid: {result['data']['is_valid']}")
        else:
            print(f"❌ Failed: {result.get('error', 'Unknown error')}")
            return False
        
        # Test invalid region
        result = await validate_azure_region("invalid-region")
        if result['status'] == 'success':
            print(f"  - invalid-region is valid: {result['data']['is_valid']}")
        
        print("\n✅ All MCP tool tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = asyncio.run(test_mcp_tools())
    sys.exit(0 if success else 1)
