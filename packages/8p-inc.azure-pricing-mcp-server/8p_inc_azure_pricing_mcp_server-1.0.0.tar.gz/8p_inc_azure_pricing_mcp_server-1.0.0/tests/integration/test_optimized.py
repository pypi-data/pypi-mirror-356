#!/usr/bin/env python3
"""Test script to verify optimized MCP server responses."""

import asyncio
import sys
import json
from mcp_app.azure_pricing_mcp_server.server import get_azure_pricing_from_api, get_azure_pricing_summary


async def test_optimized_responses():
    """Test optimized server responses."""
    print("Testing optimized Azure Pricing MCP Server responses...\n")
    
    try:
        # Test optimized pricing API
        print("1. Testing optimized get_azure_pricing_from_api...")
        result = await get_azure_pricing_from_api(
            service_name="Virtual Machines",
            region="eastus",
            limit=5
        )
        
        print(f"Response size: {len(str(result))} characters")
        print(f"Status: {result.get('status')}")
        print(f"Items returned: {result.get('summary', {}).get('total_items', 0)}")
        
        if result.get('pricing_data'):
            print("Sample item:")
            sample = result['pricing_data'][0]
            print(f"  - Service: {sample.get('service')}")
            print(f"  - SKU: {sample.get('sku')}")
            print(f"  - Price: {sample.get('hourly_price')}/hour")
            print(f"  - Monthly: {sample.get('monthly_cost')}")
        
        # Test new summary tool
        print("\n2. Testing new get_azure_pricing_summary...")
        result = await get_azure_pricing_summary(
            service_name="Virtual Machines",
            region="eastus"
        )
        
        print(f"Response size: {len(str(result))} characters")
        print(f"Status: {result.get('status')}")
        
        if result.get('summary'):
            summary = result['summary']
            print(f"Service: {summary.get('service')}")
            print(f"Price range: {summary.get('price_range', {}).get('lowest')} - {summary.get('price_range', {}).get('highest')}")
            print(f"Popular SKUs: {len(summary.get('popular_skus', []))}")
            
            if summary.get('popular_skus'):
                top_sku = summary['popular_skus'][0]
                print(f"Cheapest option: {top_sku.get('sku')} - {top_sku.get('hourly_price')}/hour ({top_sku.get('monthly_estimate')}/month)")
        
        print("\n✅ Optimized responses working correctly!")
        print(f"Note: {result.get('note', '')}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = asyncio.run(test_optimized_responses())
    sys.exit(0 if success else 1)
