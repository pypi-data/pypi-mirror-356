#!/usr/bin/env python3
"""Complete system test of all Azure Pricing MCP Server functionality."""

import asyncio
import tempfile
from pathlib import Path
from mcp_app.azure_pricing_mcp_server.server import (
    get_quick_azure_price,
    get_azure_pricing_summary,
    get_azure_pricing_from_web,
    compare_regional_pricing,
    analyze_terraform_project,
    generate_cost_report,
    get_azure_patterns,
    validate_azure_region
)

async def test_complete_system():
    """Test the complete Azure Pricing MCP Server system."""
    print("🚀 Azure Pricing MCP Server - Complete System Test")
    print("=" * 70)
    
    test_results = {}
    
    # Test 1: Quick pricing
    print("\n1️⃣ Quick Pricing")
    print("-" * 30)
    try:
        result = await get_quick_azure_price("Virtual Machines", "eastus")
        test_results['quick_pricing'] = result.get('status') == 'success'
        print(f"✅ Status: {result.get('status')}")
        if result.get('status') == 'success':
            pricing = result.get('pricing', {})
            print(f"   Monthly: {pricing.get('monthly')}")
    except Exception as e:
        test_results['quick_pricing'] = False
        print(f"❌ Error: {e}")
    
    # Test 2: Service summary
    print("\n2️⃣ Service Summary")
    print("-" * 30)
    try:
        result = await get_azure_pricing_summary("Storage", "eastus")
        test_results['service_summary'] = result.get('status') == 'success'
        print(f"✅ Status: {result.get('status')}")
        if result.get('status') == 'success':
            summary = result.get('summary', {})
            print(f"   SKUs found: {len(summary.get('popular_skus', []))}")
    except Exception as e:
        test_results['service_summary'] = False
        print(f"❌ Error: {e}")
    
    # Test 3: Web scraping
    print("\n3️⃣ Web Scraping")
    print("-" * 30)
    try:
        result = await get_azure_pricing_from_web("functions")
        test_results['web_scraping'] = result.get('status') == 'success'
        print(f"✅ Status: {result.get('status')}")
        if result.get('status') == 'success':
            summary = result.get('summary', {})
            print(f"   Free tier: {'Yes' if summary.get('free_tier') else 'No'}")
    except Exception as e:
        test_results['web_scraping'] = False
        print(f"❌ Error: {e}")
    
    # Test 4: Regional comparison
    print("\n4️⃣ Regional Comparison")
    print("-" * 30)
    try:
        result = await compare_regional_pricing("Virtual Machines", ["eastus", "westeurope"])
        test_results['regional_comparison'] = result.get('status') == 'success'
        print(f"✅ Status: {result.get('status')}")
        if result.get('status') == 'success':
            comparison = result.get('comparison', {})
            print(f"   Regions compared: {comparison.get('regions_compared')}")
    except Exception as e:
        test_results['regional_comparison'] = False
        print(f"❌ Error: {e}")
    
    # Test 5: Infrastructure analysis
    print("\n5️⃣ Infrastructure Analysis")
    print("-" * 30)
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            tf_project = Path(temp_dir) / "test_tf"
            tf_project.mkdir()
            
            tf_file = tf_project / "main.tf"
            tf_file.write_text('''
resource "azurerm_linux_virtual_machine" "test" {
  name = "test-vm"
}
resource "azurerm_storage_account" "test" {
  name = "teststorage"
}
''')
            
            result = await analyze_terraform_project(str(tf_project))
            test_results['infrastructure_analysis'] = result.get('status') == 'success'
            print(f"✅ Status: {result.get('status')}")
            if result.get('status') == 'success':
                summary = result.get('summary', {})
                print(f"   Resources found: {summary.get('total_resources')}")
    except Exception as e:
        test_results['infrastructure_analysis'] = False
        print(f"❌ Error: {e}")
    
    # Test 6: Report generation
    print("\n6️⃣ Report Generation")
    print("-" * 30)
    try:
        sample_data = {
            'services': {
                'Virtual Machines': {
                    'pricing': {'hourly': '$0.05', 'monthly': '$36.50'},
                    'sku': 'Standard_B1s',
                    'region': 'eastus'
                }
            },
            'summary': {
                'total_services': 1,
                'estimated_monthly_cost': '$36.50'
            }
        }
        
        result = await generate_cost_report(sample_data, "markdown")
        test_results['report_generation'] = result.get('status') == 'success'
        print(f"✅ Status: {result.get('status')}")
        if result.get('status') == 'success':
            if 'report_content' in result:
                print(f"   Report size: {len(result['report_content'])} chars")
            else:
                print(f"   Large report handled with preview")
    except Exception as e:
        test_results['report_generation'] = False
        print(f"❌ Error: {e}")
    
    # Test 7: Architecture patterns
    print("\n7️⃣ Architecture Patterns")
    print("-" * 30)
    try:
        result = await get_azure_patterns("web-app-basic")
        test_results['architecture_patterns'] = result.get('status') == 'success'
        print(f"✅ Status: {result.get('status')}")
        if result.get('status') == 'success':
            print(f"   Pattern: {result.get('pattern_name')}")
            print(f"   Cost: {result.get('total_cost')}")
    except Exception as e:
        test_results['architecture_patterns'] = False
        print(f"❌ Error: {e}")
    
    # Test 8: Region validation
    print("\n8️⃣ Region Validation")
    print("-" * 30)
    try:
        result = await validate_azure_region("eastus")
        test_results['region_validation'] = result.get('status') == 'success'
        print(f"✅ Status: {result.get('status')}")
        if result.get('status') == 'success':
            data = result.get('data', {})
            print(f"   Valid region: {data.get('is_valid')}")
    except Exception as e:
        test_results['region_validation'] = False
        print(f"❌ Error: {e}")
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 SYSTEM TEST SUMMARY")
    print("=" * 70)
    
    passed_tests = sum(test_results.values())
    total_tests = len(test_results)
    
    for test_name, passed in test_results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title():25} | {status}")
    
    print("-" * 70)
    print(f"TOTAL: {passed_tests}/{total_tests} tests passed ({passed_tests/total_tests*100:.1f}%)")
    
    if passed_tests == total_tests:
        print("\n🎉 ALL TESTS PASSED! Azure Pricing MCP Server is fully functional!")
        return True
    else:
        print(f"\n⚠️  {total_tests - passed_tests} test(s) failed. Please check the errors above.")
        return False

if __name__ == '__main__':
    success = asyncio.run(test_complete_system())
    exit(0 if success else 1)
