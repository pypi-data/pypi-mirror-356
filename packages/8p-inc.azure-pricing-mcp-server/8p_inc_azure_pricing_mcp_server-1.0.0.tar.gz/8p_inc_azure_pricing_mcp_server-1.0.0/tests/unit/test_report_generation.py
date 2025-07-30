#!/usr/bin/env python3
"""Test report generation functionality."""

import asyncio
from mcp_app.azure_pricing_mcp_server.server import generate_cost_report

async def test_report_generation():
    """Test report generation functionality."""
    print("Testing Azure pricing report generation...\n")
    
    # Sample pricing data
    sample_pricing_data = {
        'summary': {
            'total_services': 3,
            'regions_covered': 2,
            'estimated_monthly_cost': '$157.52',
            'estimated_annual_cost': '$1,890.24'
        },
        'services': {
            'Virtual Machines': {
                'pricing': {
                    'hourly': '$0.0688',
                    'monthly': '$50.22',
                    'annual': '$602.64'
                },
                'sku': 'Standard_B2s',
                'region': 'eastus',
                'free_tier': None
            },
            'Storage': {
                'pricing': {
                    'hourly': '$0.01',
                    'monthly': '$7.30',
                    'annual': '$87.60'
                },
                'sku': 'Standard_LRS',
                'region': 'eastus',
                'free_tier': 'First 5 GB free for 12 months'
            },
            'App Service': {
                'pricing': {
                    'hourly': '$0.137',
                    'monthly': '$100.00',
                    'annual': '$1,200.00'
                },
                'sku': 'S1',
                'region': 'westeurope',
                'free_tier': 'F1 tier available with 1 GB storage'
            }
        },
        'regional_comparison': {
            'eastus': {
                'average_hourly_price': '$0.0394',
                'average_monthly_cost': '$28.76',
                'sample_count': 2
            },
            'westeurope': {
                'average_hourly_price': '$0.137',
                'average_monthly_cost': '$100.00',
                'sample_count': 1
            }
        },
        'infrastructure': {
            'project_type': 'Terraform',
            'total_resources': 5,
            'unique_services': 3,
            'services_found': [
                {'service': 'Virtual Machines', 'resource_count': 2, 'pricing_available': True},
                {'service': 'Storage', 'resource_count': 2, 'pricing_available': True},
                {'service': 'App Service', 'resource_count': 1, 'pricing_available': True}
            ]
        },
        'recommendations': [
            'Consider using Azure Reserved Instances for Virtual Machines to save up to 72%',
            'Use Azure Spot VMs for non-critical workloads to save up to 90%',
            'Implement auto-scaling for App Service to optimize costs',
            'Consider moving to cheaper regions like East US for development environments'
        ]
    }
    
    # Test markdown report generation
    print("1. Testing Markdown report generation...")
    markdown_result = await generate_cost_report(
        pricing_data=sample_pricing_data,
        report_format="markdown",
        include_recommendations=True
    )
    
    print(f"Markdown Status: {markdown_result.get('status')}")
    print(f"Response size: {len(str(markdown_result))} characters")
    
    if markdown_result.get('status') == 'success':
        if 'report_content' in markdown_result:
            content = markdown_result['report_content']
            print(f"  Full report: {len(content)} characters")
            print("  Report preview:")
            print("  " + "\n  ".join(content.split('\n')[:10]))
        elif 'report_preview' in markdown_result:
            summary = markdown_result.get('report_summary', {})
            print(f"  Large report: {summary.get('total_characters')} characters")
            print(f"  Sections: {len(summary.get('sections', []))}")
            print("  Preview available (truncated for context window)")
    
    # Test CSV report generation
    print("\n2. Testing CSV report generation...")
    csv_result = await generate_cost_report(
        pricing_data=sample_pricing_data,
        report_format="csv",
        include_recommendations=True
    )
    
    print(f"CSV Status: {csv_result.get('status')}")
    print(f"Response size: {len(str(csv_result))} characters")
    
    if csv_result.get('status') == 'success':
        if 'report_content' in csv_result:
            content = csv_result['report_content']
            print(f"  Full report: {len(content)} characters")
            print("  Report preview:")
            print("  " + "\n  ".join(content.split('\n')[:10]))
    
    # Test minimal data
    print("\n3. Testing with minimal data...")
    minimal_data = {
        'services': {
            'Virtual Machines': {
                'pricing': {'hourly': '$0.05', 'monthly': '$36.50'},
                'sku': 'Standard_B1s',
                'region': 'eastus'
            }
        }
    }
    
    minimal_result = await generate_cost_report(
        pricing_data=minimal_data,
        report_format="markdown",
        include_recommendations=False
    )
    
    print(f"Minimal Status: {minimal_result.get('status')}")
    print(f"Response size: {len(str(minimal_result))} characters")
    
    # Test error handling
    print("\n4. Testing error handling...")
    error_result = await generate_cost_report(
        pricing_data={},  # Empty data
        report_format="markdown"
    )
    
    print(f"Error test status: {error_result.get('status')}")
    if error_result.get('status') == 'success':
        print("  Empty data handled gracefully")
    else:
        print(f"  Error message: {error_result.get('message', 'No error message')}")
    
    print("\n✅ Report generation test completed!")

if __name__ == '__main__':
    asyncio.run(test_report_generation())
