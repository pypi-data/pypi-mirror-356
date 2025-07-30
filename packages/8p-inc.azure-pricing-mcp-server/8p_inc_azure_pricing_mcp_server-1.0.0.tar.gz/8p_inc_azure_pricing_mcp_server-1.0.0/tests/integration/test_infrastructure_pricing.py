#!/usr/bin/env python3
"""Test combined infrastructure analysis and pricing."""

import asyncio
import tempfile
from pathlib import Path
from mcp_app.azure_pricing_mcp_server.server import (
    analyze_terraform_project,
    get_quick_azure_price
)

async def test_infrastructure_pricing():
    """Test combined infrastructure analysis and pricing."""
    print("Testing combined infrastructure analysis + pricing...\n")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        tf_project = temp_path / "terraform_test"
        tf_project.mkdir()
        
        # Create Terraform file with common Azure resources
        tf_file = tf_project / "main.tf"
        tf_content = '''
resource "azurerm_linux_virtual_machine" "web" {
  name = "vm-web"
  size = "Standard_B2s"
}

resource "azurerm_storage_account" "main" {
  name = "storagetest"
  account_tier = "Standard"
}

resource "azurerm_app_service_plan" "main" {
  name = "asp-test"
  sku {
    tier = "Standard"
    size = "S1"
  }
}
'''
        tf_file.write_text(tf_content)
        
        # 1. Analyze infrastructure
        print("1. Analyzing Terraform project...")
        analysis_result = await analyze_terraform_project(str(tf_project))
        
        print(f"Analysis Status: {analysis_result.get('status')}")
        if analysis_result.get('status') == 'success':
            summary = analysis_result.get('summary', {})
            services = analysis_result.get('services_found', [])
            
            print(f"  Found {summary.get('total_resources')} resources")
            print(f"  Across {summary.get('unique_services')} services")
            print("  Services identified:")
            for service in services:
                print(f"    - {service['service']}: {service['resource_count']} resources")
        
        # 2. Get pricing for identified services
        print("\n2. Getting pricing for identified services...")
        
        services_to_price = ['Virtual Machines', 'Storage', 'App Service']
        region = 'eastus'
        
        pricing_results = {}
        for service in services_to_price:
            print(f"  Getting pricing for {service}...")
            pricing_result = await get_quick_azure_price(service, region)
            
            if pricing_result.get('status') == 'success':
                pricing = pricing_result.get('pricing', {})
                pricing_results[service] = {
                    'sku': pricing_result.get('sku'),
                    'monthly_cost': pricing.get('monthly'),
                    'annual_cost': pricing.get('annual')
                }
                print(f"    ✅ {service}: {pricing.get('monthly')}/month")
            else:
                print(f"    ❌ {service}: Pricing not available")
        
        # 3. Generate cost estimate summary
        print("\n3. Infrastructure Cost Estimate Summary:")
        print("=" * 50)
        
        total_monthly = 0
        for service, pricing in pricing_results.items():
            monthly_cost = float(pricing['monthly_cost'].replace('$', ''))
            total_monthly += monthly_cost
            print(f"{service:20} | {pricing['monthly_cost']:>12}/month | {pricing['sku']}")
        
        print("-" * 50)
        print(f"{'TOTAL ESTIMATED':20} | ${total_monthly:>11.2f}/month | ${total_monthly * 12:.2f}/year")
        print("=" * 50)
        
        print("\n📊 Analysis Complete!")
        print(f"✅ Infrastructure analysis: {len(str(analysis_result))} chars")
        print(f"✅ Pricing data: {len(str(pricing_results))} chars")
        print(f"✅ Combined workflow: Infrastructure → Pricing → Cost Estimation")
        
        # 4. Optimization recommendations
        print("\n4. Cost Optimization Recommendations:")
        print("💡 Consider using Spot instances for non-critical VMs")
        print("💡 Use Standard_LRS storage for development environments")
        print("💡 Scale App Service plans based on actual usage")
        print("💡 Implement auto-scaling to optimize costs")

if __name__ == '__main__':
    asyncio.run(test_infrastructure_pricing())
