#!/usr/bin/env python3
"""Test script to verify Azure API integration."""

import asyncio
import sys
from mcp_app.azure_pricing_mcp_server.helpers import fetch_azure_pricing_data, format_pricing_data


async def test_azure_api():
    """Test Azure API integration."""
    print("Testing Azure Retail Prices API integration...")
    
    try:
        # Test basic API call
        print("\n1. Testing basic API call...")
        data = await fetch_azure_pricing_data(top=5)
        print(f"✓ Successfully fetched {data.get('Count', 0)} items")
        
        # Test with service filter
        print("\n2. Testing with service filter...")
        data = await fetch_azure_pricing_data(
            filters={'service_name': 'Virtual Machines'}, 
            top=3
        )
        print(f"✓ Successfully fetched {data.get('Count', 0)} Virtual Machines items")
        
        # Test data formatting
        print("\n3. Testing data formatting...")
        formatted = format_pricing_data(data)
        print(f"✓ Formatted {formatted['summary']['total_items']} items")
        print(f"  - Unique services: {formatted['summary']['unique_services']}")
        print(f"  - Unique regions: {formatted['summary']['unique_regions']}")
        
        # Show sample item
        if formatted['items']:
            item = formatted['items'][0]
            print(f"\nSample item:")
            print(f"  Service: {item['service_name']}")
            print(f"  Product: {item['product_name']}")
            print(f"  SKU: {item['sku_name']}")
            print(f"  Region: {item['location']} ({item['arm_region_name']})")
            print(f"  Price: ${item['unit_price']:.4f} per {item['unit_of_measure']}")
            print(f"  Monthly cost: ${item['monthly_cost']:.2f}")
        
        print("\n✅ All tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False


if __name__ == '__main__':
    success = asyncio.run(test_azure_api())
    sys.exit(0 if success else 1)
