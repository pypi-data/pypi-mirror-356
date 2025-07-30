#!/usr/bin/env python3
"""Test the quick pricing tool."""

import asyncio
from mcp_app.azure_pricing_mcp_server.server import get_quick_azure_price

async def test_quick_price():
    """Test quick pricing tool."""
    print("Testing quick Azure pricing tool...\n")
    
    # Test basic VM pricing
    result = await get_quick_azure_price("Virtual Machines", "eastus")
    print("Quick VM pricing:")
    print(f"Status: {result.get('status')}")
    print(f"Service: {result.get('service')}")
    print(f"SKU: {result.get('sku')}")
    print(f"Region: {result.get('region')}")
    
    if result.get('pricing'):
        pricing = result['pricing']
        print(f"Pricing:")
        print(f"  Hourly: {pricing.get('hourly')}")
        print(f"  Monthly: {pricing.get('monthly')}")
        print(f"  Annual: {pricing.get('annual')}")
    
    print(f"\nResponse size: {len(str(result))} characters")
    print("✅ Quick pricing tool working!")

if __name__ == '__main__':
    asyncio.run(test_quick_price())
