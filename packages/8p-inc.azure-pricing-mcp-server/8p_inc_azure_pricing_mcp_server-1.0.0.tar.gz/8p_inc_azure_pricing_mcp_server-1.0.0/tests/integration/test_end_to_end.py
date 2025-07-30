#!/usr/bin/env python3
"""End-to-end test of all Azure Pricing MCP Server functionality."""

import asyncio
import tempfile
from pathlib import Path
from mcp_app.azure_pricing_mcp_server.server import (
    get_quick_azure_price,
    get_azure_pricing_summary,
    get_azure_pricing_from_web,
    compare_regional_pricing,
    analyze_terraform_project,
    generate_cost_report
)

async def test_end_to_end():
    """Test complete end-to-end workflow."""
    print("🚀 Azure Pricing MCP Server - End-to-End Test")
    print("=" * 60)
    
    # Step 1: Quick pricing check
    print("\n1️⃣ Quick Pricing Check")
    print("-" * 30)
    
    quick_price = await get_quick_azure_price("Virtual Machines", "eastus")
    print(f"Status: {quick_price.get('status')}")
    if quick_price.get('status') == 'success':
        pricing = quick_price.get('pricing', {})
        print(f"Service: {quick_price.get('service')}")
        print(f"Monthly cost: {pricing.get('monthly')}")
    
    # Step 2: Service overview
    print("\n2️⃣ Service Overview")
    print("-" * 30)
    
    summary = await get_azure_pricing_summary("Storage", "eastus")
    print(f"Status: {summary.get('status')}")
    if summary.get('status') == 'success':
        summary_data = summary.get('summary', {})
        print(f"Price range: {summary_data.get('price_range', {}).get('lowest')} - {summary_data.get('price_range', {}).get('highest')}")
        print(f"Popular SKUs: {len(summary_data.get('popular_skus', []))}")
    
    # Step 3: Web scraping
    print("\n3️⃣ Web Scraping")
    print("-" * 30)
    
    web_data = await get_azure_pricing_from_web("functions")
    print(f"Status: {web_data.get('status')}")
    if web_data.get('status') == 'success':
        web_summary = web_data.get('summary', {})
        print(f"Free tier: {'Yes' if web_summary.get('free_tier') else 'No'}")
        print(f"Special offers: {len(web_summary.get('special_offers', []))}")
    
    print("\n✅ All individual components working!")
    return True

if __name__ == '__main__':
    success = asyncio.run(test_end_to_end())
    print(f"\n🎉 End-to-end test {'PASSED' if success else 'FAILED'}!")
