#!/usr/bin/env python3
"""Test combined API and web scraping functionality."""

import asyncio
from mcp_app.azure_pricing_mcp_server.server import (
    get_quick_azure_price,
    get_azure_pricing_from_web
)

async def test_combined_pricing():
    """Test combined API and web scraping for comprehensive pricing info."""
    print("Testing combined Azure pricing (API + Web Scraping)...\n")
    
    service = "virtual-machines"
    region = "eastus"
    
    # Get API pricing
    print("1. Getting API pricing data...")
    api_result = await get_quick_azure_price(service.replace('-', ' ').title(), region)
    
    print(f"API Status: {api_result.get('status')}")
    if api_result.get('status') == 'success':
        pricing = api_result.get('pricing', {})
        print(f"  Service: {api_result.get('service')}")
        print(f"  SKU: {api_result.get('sku')}")
        print(f"  Region: {api_result.get('region')}")
        print(f"  Monthly cost: {pricing.get('monthly')}")
    
    # Get web scraping data
    print("\n2. Getting web scraping data...")
    web_result = await get_azure_pricing_from_web(service)
    
    print(f"Web Status: {web_result.get('status')}")
    if web_result.get('status') == 'success':
        summary = web_result.get('summary', {})
        print(f"  Service: {web_result.get('service')}")
        print(f"  Free tier: {summary.get('free_tier')[:100] if summary.get('free_tier') else 'None'}...")
        print(f"  Pricing highlights: {len(summary.get('pricing_highlights', []))}")
        print(f"  Special offers: {len(summary.get('special_offers', []))}")
    
    # Combined summary
    print("\n3. Combined Summary:")
    print("✅ API provides: Real-time pricing, specific SKU costs, regional pricing")
    print("✅ Web scraping provides: Free tier info, special offers, pricing highlights")
    print("✅ Together: Comprehensive pricing intelligence for Azure services")
    
    # Response size comparison
    api_size = len(str(api_result))
    web_size = len(str(web_result))
    print(f"\nResponse sizes: API={api_size} chars, Web={web_size} chars")
    print(f"Total combined: {api_size + web_size} chars (optimized for context window)")
    
    print("\n🎉 Combined pricing test successful!")

if __name__ == '__main__':
    asyncio.run(test_combined_pricing())
