#!/usr/bin/env python3
"""Test web scraping functionality."""

import asyncio
from mcp_app.azure_pricing_mcp_server.web_scraper import scrape_azure_pricing
from mcp_app.azure_pricing_mcp_server.server import get_azure_pricing_from_web

async def test_web_scraping():
    """Test web scraping functionality."""
    print("Testing Azure pricing web scraping...\n")
    
    # Test direct scraper
    print("1. Testing direct web scraper...")
    result = await scrape_azure_pricing("virtual-machines")
    print(f"Status: {result.get('status')}")
    
    if result.get('status') == 'success':
        data = result['data']
        print(f"Service: {data.get('service')}")
        print(f"URL: {data.get('url')}")
        print(f"Pricing summaries found: {len(data.get('pricing_summary', []))}")
        print(f"Free tier info: {'Yes' if data.get('free_tier') else 'No'}")
        print(f"Special offers: {len(data.get('special_offers', []))}")
    else:
        print(f"Error: {result.get('message')}")
    
    # Test MCP tool
    print("\n2. Testing MCP web scraping tool...")
    result = await get_azure_pricing_from_web("virtual-machines")
    print(f"Status: {result.get('status')}")
    print(f"Response size: {len(str(result))} characters")
    
    if result.get('status') == 'success':
        summary = result.get('summary', {})
        print(f"Pricing highlights: {len(summary.get('pricing_highlights', []))}")
        print(f"Free tier: {'Yes' if summary.get('free_tier') else 'No'}")
        print(f"Special offers: {len(summary.get('special_offers', []))}")
    
    print("\n✅ Web scraping test completed!")

if __name__ == '__main__':
    asyncio.run(test_web_scraping())
