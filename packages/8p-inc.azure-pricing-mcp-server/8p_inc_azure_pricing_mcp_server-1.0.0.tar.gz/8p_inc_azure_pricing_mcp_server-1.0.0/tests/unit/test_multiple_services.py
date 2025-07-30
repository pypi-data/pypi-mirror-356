#!/usr/bin/env python3
"""Test web scraping for multiple services."""

import asyncio
from mcp_app.azure_pricing_mcp_server.server import get_azure_pricing_from_web

async def test_multiple_services():
    """Test web scraping for multiple Azure services."""
    print("Testing web scraping for multiple Azure services...\n")
    
    services = ['virtual-machines', 'storage', 'app-service', 'functions']
    
    for service in services:
        print(f"Testing {service}...")
        result = await get_azure_pricing_from_web(service)
        
        print(f"  Status: {result.get('status')}")
        print(f"  Response size: {len(str(result))} characters")
        
        if result.get('status') == 'success':
            summary = result.get('summary', {})
            print(f"  Pricing highlights: {len(summary.get('pricing_highlights', []))}")
            print(f"  Free tier: {'Yes' if summary.get('free_tier') else 'No'}")
            print(f"  Special offers: {len(summary.get('special_offers', []))}")
        else:
            print(f"  Error: {result.get('message', 'Unknown error')}")
        
        print()
    
    print("✅ Multiple services test completed!")

if __name__ == '__main__':
    asyncio.run(test_multiple_services())
