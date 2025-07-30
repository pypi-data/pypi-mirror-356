"""Azure Pricing MCP Server implementation.

This server provides tools for analyzing Azure service costs and pricing information.
"""

import asyncio
import logging
import os
import sys
from typing import Any, Dict, List, Optional

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

from .helpers import (
    AzurePricingFilter,
    fetch_azure_pricing_data,
    format_pricing_data,
    get_regional_pricing,
    get_service_families,
    validate_region_name,
)
from .logging_config import mcp_logger, log_mcp_tool
from .web_scraper import scrape_azure_pricing


# Set up logging - use the enhanced MCP logger
logger = mcp_logger

# Initialize FastMCP server
mcp = FastMCP('Azure Pricing MCP Server')


class PricingQueryRequest(BaseModel):
    """Request model for pricing queries."""
    
    service_name: Optional[str] = Field(None, description="Azure service name to query")
    region: Optional[str] = Field(None, description="Azure region name")
    product_name: Optional[str] = Field(None, description="Product name filter")
    sku_name: Optional[str] = Field(None, description="SKU name filter")
    meter_name: Optional[str] = Field(None, description="Meter name filter")
    currency: Optional[str] = Field('USD', description="Currency code (default: USD)")
    limit: Optional[int] = Field(100, description="Maximum number of results (default: 100)")


class RegionalComparisonRequest(BaseModel):
    """Request model for regional pricing comparison."""
    
    service_name: str = Field(..., description="Azure service name to compare")
    regions: List[str] = Field(..., description="List of Azure regions to compare")
    product_name: Optional[str] = Field(None, description="Product name filter")
    sku_name: Optional[str] = Field(None, description="SKU name filter")


@mcp.tool(name="get_pricing_api")
@log_mcp_tool(logger)
async def get_azure_pricing_from_api(
    service_name: Optional[str] = None,
    region: Optional[str] = None,
    product_name: Optional[str] = None,
    sku_name: Optional[str] = None,
    meter_name: Optional[str] = None,
    currency: str = 'USD',
    limit: int = 10
) -> Dict[str, Any]:
    """Get Azure pricing information from the Retail Prices API.
    
    This tool queries the Azure Retail Prices API to retrieve current pricing
    information for Azure services. You can filter by service name, region,
    product name, SKU name, or meter name.
    
    Args:
        service_name: Azure service name (e.g., 'Virtual Machines', 'Storage')
        region: Azure region name (e.g., 'eastus', 'westeurope')
        product_name: Product name filter (e.g., 'Virtual Machines Dv3 Series')
        sku_name: SKU name filter (e.g., 'D2s v3')
        meter_name: Meter name filter (e.g., 'D2s v3')
        currency: Currency code (default: USD)
        limit: Maximum number of results to return (default: 10, max: 50)
        
    Returns:
        Dictionary containing pricing data with formatted items and summary
        
    Example:
        >>> await get_azure_pricing_from_api(service_name="Virtual Machines", region="eastus")
    """
    logger.info(f"Getting Azure pricing for service: {service_name}, region: {region}")
    
    # Validate region if provided
    if region and not validate_region_name(region):
        logger.warning(f"Invalid region name: {region}")
        return {
            'error': f'Invalid region name: {region}',
            'valid_regions': [
                'eastus', 'eastus2', 'westus', 'westus2', 'centralus',
                'northeurope', 'westeurope', 'eastasia', 'southeastasia'
            ]
        }
    
    # Build filters
    filters = {}
    if service_name:
        filters['service_name'] = service_name
    if region:
        filters['arm_region_name'] = region
    if product_name:
        filters['product_name'] = product_name
    if sku_name:
        filters['sku_name'] = sku_name
    if meter_name:
        filters['meter_name'] = meter_name
    if currency:
        filters['currency_code'] = currency
    
    try:
        # Fetch data from Azure API
        raw_data = await fetch_azure_pricing_data(filters, top=min(limit, 50))
        
        # Format and return data
        formatted_data = format_pricing_data(raw_data)
        
        # Optimize response - limit items and include only essential data
        optimized_items = []
        for item in formatted_data['items'][:limit]:
            optimized_items.append({
                'service': item['service_name'],
                'product': item['product_name'],
                'sku': item['sku_name'],
                'region': item['location'],
                'hourly_price': f"${item['unit_price']:.4f}",
                'monthly_cost': f"${item['monthly_cost']:.2f}",
                'unit': item['unit_of_measure'],
                'type': item['type']
            })
        
        logger.info(f"Successfully retrieved {len(optimized_items)} pricing items")
        
        return {
            'status': 'success',
            'summary': {
                'total_items': len(optimized_items),
                'service': service_name,
                'region': region,
                'currency': currency
            },
            'pricing_data': optimized_items[:10],  # Limit to top 10 for readability
            'note': f"Showing top {min(len(optimized_items), 10)} results. Use filters for more specific queries."
        }
        
    except Exception as e:
        logger.error(f"Error fetching Azure pricing data: {e}")
        return {
            'status': 'error',
            'error': str(e),
            'message': 'Failed to retrieve pricing data from Azure API'
        }


@mcp.tool(name="compare_regions")
@log_mcp_tool(logger)
async def compare_regional_pricing(
    service_name: str,
    regions: List[str],
    product_name: Optional[str] = None,
    sku_name: Optional[str] = None
) -> Dict[str, Any]:
    """Compare Azure pricing across multiple regions.
    
    This tool compares pricing for a specific Azure service across multiple regions
    to help identify cost optimization opportunities.
    
    Args:
        service_name: Azure service name to compare
        regions: List of Azure regions to compare (e.g., ['eastus', 'westeurope'])
        product_name: Optional product name filter
        sku_name: Optional SKU name filter
        
    Returns:
        Dictionary containing regional pricing comparison
        
    Example:
        >>> await compare_regional_pricing("Virtual Machines", ["eastus", "westeurope"])
    """
    logger.info(f"Comparing regional pricing for {service_name} across {len(regions)} regions")
    
    # Validate regions
    invalid_regions = [r for r in regions if not validate_region_name(r)]
    if invalid_regions:
        return {
            'status': 'error',
            'error': f'Invalid regions: {invalid_regions}',
            'message': 'Please provide valid Azure region names'
        }
    
    try:
        # Get pricing data for each region
        regional_data = await get_regional_pricing(service_name, regions, product_name, sku_name)
        
        # Format comparison data - optimize for readability
        comparison = {
            'service': service_name,
            'regions_compared': len(regions),
            'summary': {
                'cheapest_region': None,
                'most_expensive_region': None,
                'price_difference': None
            },
            'regional_data': {}
        }
        
        region_prices = {}
        
        for region, items in regional_data.items():
            if items:
                # Calculate average price and get sample items
                prices = [item.get('unitPrice', 0) for item in items]
                avg_price = sum(prices) / len(prices) if prices else 0
                region_prices[region] = avg_price
                
                # Include only essential data for each region
                comparison['regional_data'][region] = {
                    'average_hourly_price': f"${avg_price:.4f}",
                    'average_monthly_cost': f"${avg_price * 730:.2f}",
                    'sample_count': len(items),
                    'top_skus': [
                        {
                            'sku': item.get('skuName', ''),
                            'price': f"${item.get('unitPrice', 0):.4f}/hour"
                        }
                        for item in items[:3]  # Only top 3 SKUs
                    ]
                }
            else:
                comparison['regional_data'][region] = {
                    'message': 'No pricing data available for this region'
                }
        
        # Find cheapest and most expensive regions
        if region_prices:
            cheapest = min(region_prices.items(), key=lambda x: x[1])
            most_expensive = max(region_prices.items(), key=lambda x: x[1])
            
            comparison['summary'] = {
                'cheapest_region': {
                    'region': cheapest[0],
                    'avg_hourly_price': f"${cheapest[1]:.4f}",
                    'avg_monthly_cost': f"${cheapest[1] * 730:.2f}"
                },
                'most_expensive_region': {
                    'region': most_expensive[0],
                    'avg_hourly_price': f"${most_expensive[1]:.4f}",
                    'avg_monthly_cost': f"${most_expensive[1] * 730:.2f}"
                },
                'potential_savings': f"${(most_expensive[1] - cheapest[1]) * 730:.2f}/month"
            }
        
        return {
            'status': 'success',
            'comparison': comparison
        }
        
    except Exception as e:
        logger.error(f"Error comparing regional pricing: {e}")
        return {
            'status': 'error',
            'error': str(e),
            'message': 'Failed to compare regional pricing'
        }


@mcp.tool(name="get_pricing_summary")
@log_mcp_tool(logger)
async def get_azure_pricing_summary(
    service_name: str,
    region: Optional[str] = None,
    sku_filter: Optional[str] = None
) -> Dict[str, Any]:
    """Get a concise summary of Azure pricing for a specific service.
    
    This tool provides a focused, readable summary of Azure pricing without
    overwhelming detail. Perfect for quick cost estimates and comparisons.
    
    Args:
        service_name: Azure service name (e.g., 'Virtual Machines', 'Storage')
        region: Azure region name (e.g., 'eastus', 'westeurope') - optional
        sku_filter: Filter by SKU name (e.g., 'D2s v3') - optional
        
    Returns:
        Concise pricing summary with key cost information
        
    Example:
        >>> await get_azure_pricing_summary("Virtual Machines", "eastus")
    """
    logger.info(f"Getting concise pricing summary for {service_name} in {region}")
    
    # Build filters
    filters = {'service_name': service_name}
    if region:
        filters['arm_region_name'] = region
    if sku_filter:
        filters['sku_name'] = sku_filter
    
    try:
        # Fetch limited data for summary
        raw_data = await fetch_azure_pricing_data(filters, top=20)
        
        if not raw_data.get('Items'):
            return {
                'status': 'success',
                'message': f'No pricing data found for {service_name}' + (f' in {region}' if region else ''),
                'suggestions': [
                    'Try a different region',
                    'Check service name spelling',
                    'Use get_service_families to see available services'
                ]
            }
        
        items = raw_data['Items']
        
        # Create concise summary
        popular_skus = {}
        regions_found = set()
        price_range = {'min': float('inf'), 'max': 0}
        
        for item in items:
            sku = item.get('skuName', 'Unknown')
            price = item.get('unitPrice', 0)
            region_name = item.get('location', item.get('armRegionName', 'Unknown'))
            
            regions_found.add(region_name)
            
            if price > 0:
                price_range['min'] = min(price_range['min'], price)
                price_range['max'] = max(price_range['max'], price)
                
                if sku not in popular_skus or popular_skus[sku]['price'] > price:
                    popular_skus[sku] = {
                        'price': price,
                        'monthly_cost': price * 730,
                        'region': region_name,
                        'unit': item.get('unitOfMeasure', '1 Hour')
                    }
        
        # Format response
        top_skus = sorted(popular_skus.items(), key=lambda x: x[1]['price'])[:5]
        
        summary = {
            'service': service_name,
            'region_queried': region or 'All regions',
            'regions_available': len(regions_found),
            'sample_regions': list(regions_found)[:3],
            'price_range': {
                'lowest': f"${price_range['min']:.4f}/hour" if price_range['min'] != float('inf') else 'N/A',
                'highest': f"${price_range['max']:.4f}/hour" if price_range['max'] > 0 else 'N/A'
            },
            'popular_skus': [
                {
                    'sku': sku,
                    'hourly_price': f"${data['price']:.4f}",
                    'monthly_estimate': f"${data['monthly_cost']:.2f}",
                    'region': data['region'],
                    'unit': data['unit']
                }
                for sku, data in top_skus
            ]
        }
        
        return {
            'status': 'success',
            'summary': summary,
            'note': f'Showing {len(top_skus)} most cost-effective options. Use filters for specific SKUs.'
        }
        
    except Exception as e:
        logger.error(f"Error getting pricing summary: {e}")
        return {
            'status': 'error',
            'error': str(e),
            'message': 'Failed to retrieve pricing summary'
        }


    """Get list of Azure service families.
    
    Returns the available Azure service families that can be used for filtering
    pricing queries.
    
    Returns:
        Dictionary containing list of service families
    """
    logger.info("Getting Azure service families")
    
    try:
        families = get_service_families()
        
        return {
            'status': 'success',
            'data': {
                'service_families': families,
                'count': len(families)
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting service families: {e}")
        return {
            'status': 'error',
            'error': str(e),
            'message': 'Failed to retrieve service families'
        }


@mcp.tool(name="get_quick_price")
@log_mcp_tool(logger)
async def get_quick_azure_price(
    service_name: str,
    region: str = "eastus",
    sku_name: Optional[str] = None
) -> Dict[str, Any]:
    """Get quick Azure pricing for immediate cost estimates.
    
    This tool provides the fastest way to get Azure pricing information
    with minimal response data - perfect for quick cost checks.
    
    Args:
        service_name: Azure service name (e.g., 'Virtual Machines')
        region: Azure region (default: eastus)
        sku_name: Specific SKU to price (optional)
        
    Returns:
        Quick pricing information with essential cost data only
    """
    logger.info(f"Getting quick price for {service_name} {sku_name or ''} in {region}")
    
    filters = {
        'service_name': service_name,
        'arm_region_name': region
    }
    if sku_name:
        filters['sku_name'] = sku_name
    
    try:
        raw_data = await fetch_azure_pricing_data(filters, top=5)
        
        if not raw_data.get('Items'):
            return {
                'status': 'not_found',
                'message': f'No pricing found for {service_name}' + (f' {sku_name}' if sku_name else '') + f' in {region}'
            }
        
        item = raw_data['Items'][0]  # Get first/best match
        price = item.get('unitPrice', 0)
        
        return {
            'status': 'success',
            'service': service_name,
            'sku': item.get('skuName', 'N/A'),
            'region': item.get('location', region),
            'pricing': {
                'hourly': f"${price:.4f}",
                'daily': f"${price * 24:.2f}",
                'monthly': f"${price * 730:.2f}",
                'annual': f"${price * 8760:.2f}"
            },
            'unit': item.get('unitOfMeasure', '1 Hour'),
            'type': item.get('type', 'Consumption')
        }
        
    except Exception as e:
        logger.error(f"Error getting quick price: {e}")
        return {
            'status': 'error',
            'message': f'Failed to get pricing for {service_name}'
        }


@mcp.tool(name="get_pricing_web")
@log_mcp_tool(logger)
async def get_azure_pricing_from_web(
    service_name: str
) -> Dict[str, Any]:
    """Get Azure pricing information by scraping official pricing pages.
    
    This tool scrapes Azure's official pricing pages to extract additional
    pricing information, special offers, and free tier details that may
    not be available through the API.
    
    Args:
        service_name: Azure service name (e.g., 'virtual-machines', 'storage')
        
    Returns:
        Dictionary containing scraped pricing information
        
    Example:
        >>> await get_azure_pricing_from_web("virtual-machines")
    """
    logger.info(f"Scraping web pricing for {service_name}")
    
    try:
        # Import here to avoid circular imports
        from .web_scraper import scrape_azure_pricing
        
        result = await scrape_azure_pricing(service_name)
        
        if result['status'] == 'success':
            data = result['data']
            
            # Optimize response for context window
            optimized_response = {
                'status': 'success',
                'service': data['service'],
                'source': 'Azure pricing page',
                'url': data['url'],
                'summary': {
                    'pricing_highlights': data['pricing_summary'][:3],  # Top 3
                    'free_tier': data['free_tier'][:200] if data['free_tier'] else None,  # Truncate
                    'special_offers': data['special_offers'][:2]  # Top 2
                },
                'note': 'Web-scraped data may be less current than API data. Use for supplementary information.'
            }
            
            return optimized_response
        else:
            return result
            
    except Exception as e:
        logger.error(f"Error in web scraping tool: {e}")
        return {
            'status': 'error',
            'message': f'Web scraping failed for {service_name}: {str(e)}',
            'suggestion': 'Try using get_azure_pricing_from_api for real-time pricing data'
        }


@mcp.tool(name="analyze_terraform")
@log_mcp_tool(logger)
async def analyze_terraform_project(
    project_path: str
) -> Dict[str, Any]:
    """Analyze a Terraform project to identify Azure resources and estimate costs.
    
    This tool scans Terraform files (.tf and .tf.json) in a project directory
    to identify Azure resources and map them to Azure services for pricing analysis.
    
    Args:
        project_path: Path to the Terraform project directory
        
    Returns:
        Dictionary containing project analysis and resource mapping
        
    Example:
        >>> await analyze_terraform_project("/path/to/terraform/project")
    """
    logger.info(f"Analyzing Terraform project at {project_path}")
    
    try:
        # Import here to avoid circular imports
        from .infrastructure_analyzer import analyze_terraform_project as analyze_tf
        
        result = await asyncio.get_event_loop().run_in_executor(
            None, analyze_tf, project_path
        )
        
        if result['status'] == 'success':
            analysis = result['analysis']
            
            # Optimize response for context window
            optimized_response = {
                'status': 'success',
                'project_type': 'Terraform',
                'project_path': result['project_path'],
                'summary': {
                    'total_resources': analysis['total_resources'],
                    'total_files': analysis['total_files'],
                    'unique_services': analysis['unique_services']
                },
                'services_found': analysis['service_summary'][:10],  # Top 10 services
                'pricing_recommendations': [
                    f"Use get_quick_azure_price('{service['service']}', 'eastus') for cost estimates"
                    for service in analysis['service_summary'][:5]
                    if service['pricing_available']
                ],
                'note': f'Found {analysis["total_resources"]} Azure resources across {analysis["unique_services"]} services'
            }
            
            return optimized_response
        else:
            return result
            
    except Exception as e:
        logger.error(f"Error analyzing Terraform project: {e}")
        return {
            'status': 'error',
            'message': f'Failed to analyze Terraform project: {str(e)}',
            'suggestion': 'Ensure the path contains valid Terraform files (.tf or .tf.json)'
        }


@mcp.tool(name="analyze_bicep")
@log_mcp_tool(logger)
async def analyze_bicep_project(
    project_path: str
) -> Dict[str, Any]:
    """Analyze a Bicep project to identify Azure resources and estimate costs.
    
    This tool scans Bicep files (.bicep) in a project directory to identify
    Azure resources and map them to Azure services for pricing analysis.
    
    Args:
        project_path: Path to the Bicep project directory
        
    Returns:
        Dictionary containing project analysis and resource mapping
        
    Example:
        >>> await analyze_bicep_project("/path/to/bicep/project")
    """
    logger.info(f"Analyzing Bicep project at {project_path}")
    
    try:
        # Import here to avoid circular imports
        from .infrastructure_analyzer import analyze_bicep_project as analyze_bicep
        
        result = await asyncio.get_event_loop().run_in_executor(
            None, analyze_bicep, project_path
        )
        
        if result['status'] == 'success':
            analysis = result['analysis']
            
            # Optimize response for context window
            optimized_response = {
                'status': 'success',
                'project_type': 'Bicep',
                'project_path': result['project_path'],
                'summary': {
                    'total_resources': analysis['total_resources'],
                    'total_files': analysis['total_files'],
                    'unique_services': analysis['unique_services']
                },
                'services_found': analysis['service_summary'][:10],  # Top 10 services
                'pricing_recommendations': [
                    f"Use get_quick_azure_price('{service['service']}', 'eastus') for cost estimates"
                    for service in analysis['service_summary'][:5]
                    if service['pricing_available']
                ],
                'note': f'Found {analysis["total_resources"]} Azure resources across {analysis["unique_services"]} services'
            }
            
            return optimized_response
        else:
            return result
            
    except Exception as e:
        logger.error(f"Error analyzing Bicep project: {e}")
        return {
            'status': 'error',
            'message': f'Failed to analyze Bicep project: {str(e)}',
            'suggestion': 'Ensure the path contains valid Bicep files (.bicep)'
        }


@mcp.tool(name="generate_report")
@log_mcp_tool(logger)
async def generate_cost_report(
    pricing_data: Dict[str, Any],
    report_format: str = "markdown",
    include_recommendations: bool = True
) -> Dict[str, Any]:
    """Generate a comprehensive Azure cost analysis report.
    
    This tool creates detailed cost analysis reports in markdown or CSV format
    based on pricing data from various sources (API, web scraping, infrastructure analysis).
    
    Args:
        pricing_data: Dictionary containing pricing information from various sources
        report_format: Output format - 'markdown' or 'csv' (default: markdown)
        include_recommendations: Whether to include cost optimization recommendations
        
    Returns:
        Dictionary containing the generated report
        
    Example:
        >>> pricing_data = {
        ...     'services': {
        ...         'Virtual Machines': {
        ...             'pricing': {'hourly': '$0.0688', 'monthly': '$50.22'},
        ...             'sku': 'Standard_B2s',
        ...             'region': 'eastus'
        ...         }
        ...     },
        ...     'summary': {
        ...         'total_services': 1,
        ...         'estimated_monthly_cost': '$50.22'
        ...     }
        ... }
        >>> await generate_cost_report(pricing_data)
    """
    logger.info(f"Generating {report_format} cost report")
    
    try:
        # Import here to avoid circular imports
        from .report_generator import generate_pricing_report
        
        # Generate the report
        report_content = await asyncio.get_event_loop().run_in_executor(
            None, generate_pricing_report, pricing_data, report_format, include_recommendations
        )
        
        # Calculate report statistics
        line_count = len(report_content.split('\n'))
        char_count = len(report_content)
        
        # Optimize response for context window
        # For large reports, provide summary instead of full content
        if char_count > 2000:
            # Provide report summary and first few lines
            lines = report_content.split('\n')
            preview = '\n'.join(lines[:20]) + '\n\n... (report truncated for display) ...'
            
            # Extract sections
            sections = []
            for line in lines:
                if line.startswith('#') and not line.startswith('# Azure Pricing'):
                    sections.append(line.strip('# ').strip())
            
            return {
                'status': 'success',
                'report_format': report_format,
                'report_summary': {
                    'total_lines': line_count,
                    'total_characters': char_count,
                    'includes_recommendations': include_recommendations,
                    'sections': sections[:10]  # Limit to first 10 sections
                },
                'report_preview': preview,
                'full_report_available': True,
                'note': f'Full report ({char_count} chars) available. Preview shown for context window optimization.'
            }
        else:
            # Return full report for smaller reports
            return {
                'status': 'success',
                'report_format': report_format,
                'report_content': report_content,
                'report_stats': {
                    'lines': line_count,
                    'characters': char_count,
                    'includes_recommendations': include_recommendations
                }
            }
            
    except Exception as e:
        logger.error(f"Error generating cost report: {e}")
        return {
            'status': 'error',
            'message': f'Failed to generate cost report: {str(e)}',
            'suggestion': 'Ensure pricing_data contains valid pricing information'
        }


@mcp.tool(name="get_patterns")
@log_mcp_tool(logger)
async def get_azure_patterns(
    pattern_name: Optional[str] = None
) -> Dict[str, Any]:
    """Get Azure architecture patterns with cost considerations.
    
    This tool provides common Azure architecture patterns with detailed
    cost breakdowns and optimization recommendations.
    
    Args:
        pattern_name: Specific pattern to retrieve (optional)
                     Available: web-app-basic, web-app-scalable, microservices,
                               serverless, data-analytics, iot-solution
        
    Returns:
        Dictionary containing architecture patterns and cost information
        
    Example:
        >>> await get_azure_patterns("web-app-basic")
        >>> await get_azure_patterns()  # Get all patterns
    """
    logger.info(f"Getting Azure architecture patterns: {pattern_name or 'all'}")
    
    try:
        # Import here to avoid circular imports
        from .architecture_patterns import get_architecture_patterns
        
        result = await asyncio.get_event_loop().run_in_executor(
            None, get_architecture_patterns, pattern_name
        )
        
        if result['status'] == 'success':
            if pattern_name:
                # Single pattern - optimize for context window
                pattern = result['pattern']
                optimized_response = {
                    'status': 'success',
                    'pattern_name': pattern['name'],
                    'description': pattern['description'],
                    'use_cases': pattern['use_cases'][:3],  # Top 3 use cases
                    'components': [
                        {
                            'service': comp['service'],
                            'sku': comp['sku'],
                            'monthly_cost': comp['estimated_monthly_cost']
                        }
                        for comp in pattern['components'][:5]  # Top 5 components
                    ],
                    'total_cost': pattern['total_estimated_cost'],
                    'optimization_tips': pattern['cost_optimization'][:3],  # Top 3 tips
                    'note': f"Pattern includes {len(pattern['components'])} components with detailed cost breakdown"
                }
                return optimized_response
            else:
                # All patterns - provide summary
                patterns = result['patterns'][:6]  # Limit to 6 patterns
                return {
                    'status': 'success',
                    'total_patterns': result['total_patterns'],
                    'available_patterns': [
                        {
                            'name': p['name'],
                            'key': p['key'],
                            'estimated_cost': p['estimated_cost'],
                            'components': p['components_count']
                        }
                        for p in patterns
                    ],
                    'note': f"Use get_azure_patterns('pattern-key') for detailed information"
                }
        else:
            return result
            
    except Exception as e:
        logger.error(f"Error getting Azure patterns: {e}")
        return {
            'status': 'error',
            'message': f'Failed to get Azure patterns: {str(e)}',
            'available_patterns': ['web-app-basic', 'web-app-scalable', 'microservices', 'serverless', 'data-analytics', 'iot-solution']
        }


@mcp.tool(name="validate_region")
@log_mcp_tool(logger)
async def validate_azure_region(region: str) -> Dict[str, Any]:
    """Validate if a region name is a valid Azure region.
    
    Args:
        region: Azure region name to validate
        
    Returns:
        Dictionary containing validation result
    """
    logger.info(f"Validating Azure region: {region}")
    
    is_valid = validate_region_name(region)
    
    return {
        'status': 'success',
        'data': {
            'region': region,
            'is_valid': is_valid,
            'message': 'Valid Azure region' if is_valid else 'Invalid Azure region name'
        }
    }


def main():
    """Main entry point for the MCP server."""
    # Use stderr for startup messages to avoid interfering with MCP protocol on stdout
    print("Azure Pricing MCP Server: Starting...", file=sys.stderr)
    
    logger.info("Starting Azure Pricing MCP Server")
    
    # Log environment configuration
    logger.log_internal_process("server_startup", {
        'mcp_debug_logging': os.getenv('MCP_DEBUG_LOGGING', 'false'),
        'mcp_log_level': os.getenv('MCP_LOG_LEVEL', 'INFO'),
        'mcp_log_file': os.getenv('MCP_LOG_FILE', 'not_set'),
        'mcp_log_format': os.getenv('MCP_LOG_FORMAT', 'json'),
        'fastmcp_log_level': os.getenv('FASTMCP_LOG_LEVEL', 'INFO'),
        'default_currency': os.getenv('DEFAULT_CURRENCY', 'USD'),
        'default_region': os.getenv('DEFAULT_REGION', 'eastus')
    }, 'INFO')
    
    # Set legacy log level from environment for backward compatibility
    log_level = os.getenv('FASTMCP_LOG_LEVEL', 'INFO').upper()
    logging.getLogger().setLevel(getattr(logging, log_level, logging.INFO))
    
    logger.info("Azure Pricing MCP Server initialized successfully")
    
    print("Azure Pricing MCP Server: Ready to accept MCP requests", file=sys.stderr)
    
    # Run the server
    try:
        mcp.run()
    except Exception as e:
        print(f"Azure Pricing MCP Server: Failed to start: {e}", file=sys.stderr)
        logger.error(f"Failed to start MCP server: {e}", exc_info=True)
        raise


if __name__ == '__main__':
    main()
