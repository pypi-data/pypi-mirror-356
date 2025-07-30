"""Helper functions for Azure pricing data retrieval and processing."""

import asyncio
import logging
import os
from typing import Any, Dict, List, Optional
from urllib.parse import quote

import httpx
from pydantic import BaseModel, Field

from .logging_config import mcp_logger


# Set up logging - use the enhanced MCP logger
logger = mcp_logger

# Configuration
AZURE_PRICING_API_BASE_URL = os.getenv(
    'AZURE_PRICING_API_BASE_URL', 
    'https://prices.azure.com/api/retail/prices'
)
DEFAULT_CURRENCY = os.getenv('DEFAULT_CURRENCY', 'USD')
DEFAULT_REGION = os.getenv('DEFAULT_REGION', 'eastus')
CACHE_TTL_SECONDS = int(os.getenv('CACHE_TTL_SECONDS', '3600'))
REQUEST_TIMEOUT = 30
MAX_RETRIES = 3
RETRY_DELAY = 1


class AzurePricingFilter(BaseModel):
    """Filter model for Azure pricing queries."""
    
    service_name: Optional[str] = Field(None, description="Azure service name")
    location: Optional[str] = Field(None, description="Azure location")
    arm_region_name: Optional[str] = Field(None, description="ARM region name")
    product_name: Optional[str] = Field(None, description="Product name")
    sku_name: Optional[str] = Field(None, description="SKU name")
    meter_name: Optional[str] = Field(None, description="Meter name")
    currency_code: Optional[str] = Field(DEFAULT_CURRENCY, description="Currency code")


class AzurePricingItem(BaseModel):
    """Model for Azure pricing item."""
    
    currency_code: str = Field(..., alias='currencyCode')
    tier_minimum_units: float = Field(..., alias='tierMinimumUnits')
    retail_price: float = Field(..., alias='retailPrice')
    unit_price: float = Field(..., alias='unitPrice')
    arm_region_name: str = Field(..., alias='armRegionName')
    location: str
    effective_start_date: str = Field(..., alias='effectiveStartDate')
    meter_id: str = Field(..., alias='meterId')
    meter_name: str = Field(..., alias='meterName')
    product_id: str = Field(..., alias='productId')
    sku_id: str = Field(..., alias='skuId')
    product_name: str = Field(..., alias='productName')
    sku_name: str = Field(..., alias='skuName')
    service_name: str = Field(..., alias='serviceName')
    service_id: str = Field(..., alias='serviceId')
    service_family: str = Field(..., alias='serviceFamily')
    unit_of_measure: str = Field(..., alias='unitOfMeasure')
    type: str
    
    class Config:
        """Pydantic configuration."""
        populate_by_name = True


class AzurePricingResponse(BaseModel):
    """Model for Azure pricing API response."""
    
    billing_currency: str = Field(..., alias='BillingCurrency')
    customer_entity_id: str = Field(..., alias='CustomerEntityId')
    customer_entity_type: str = Field(..., alias='CustomerEntityType')
    items: List[AzurePricingItem] = Field(..., alias='Items')
    next_page_link: Optional[str] = Field(None, alias='NextPageLink')
    count: int = Field(..., alias='Count')
    
    class Config:
        """Pydantic configuration."""
        populate_by_name = True


def parse_odata_filter(filter_dict: Dict[str, Any]) -> str:
    """Convert Python dict filters to OData filter expressions.
    
    Args:
        filter_dict: Dictionary containing filter criteria
        
    Returns:
        OData filter string
        
    Example:
        >>> parse_odata_filter({'serviceName': 'Virtual Machines', 'armRegionName': 'eastus'})
        "serviceName eq 'Virtual Machines' and armRegionName eq 'eastus'"
    """
    if not filter_dict:
        return ''
    
    filter_parts = []
    
    for key, value in filter_dict.items():
        if value is not None:
            # Convert snake_case to camelCase for API compatibility
            api_key = _snake_to_camel(key)
            
            if isinstance(value, str):
                filter_parts.append(f"{api_key} eq '{value}'")
            elif isinstance(value, (int, float)):
                filter_parts.append(f"{api_key} eq {value}")
            elif isinstance(value, list):
                # Handle list of values with 'or' operator
                list_filters = [f"{api_key} eq '{v}'" if isinstance(v, str) else f"{api_key} eq {v}" 
                               for v in value]
                filter_parts.append(f"({' or '.join(list_filters)})")
    
    return ' and '.join(filter_parts)


def _snake_to_camel(snake_str: str) -> str:
    """Convert snake_case to camelCase."""
    components = snake_str.split('_')
    return components[0] + ''.join(word.capitalize() for word in components[1:])


async def fetch_azure_pricing_data(
    filters: Optional[Dict[str, Any]] = None,
    skip: int = 0,
    top: int = 100
) -> Dict[str, Any]:
    """Fetch pricing data from Azure Retail Prices API.
    
    Args:
        filters: Dictionary of filters to apply
        skip: Number of items to skip (pagination)
        top: Number of items to return (max 1000)
        
    Returns:
        Dictionary containing pricing data
        
    Raises:
        httpx.HTTPError: If API request fails
        ValueError: If response data is invalid
    """
    logger.log_internal_process("azure_api_request_start", {
        "filters": filters,
        "skip": skip,
        "top": top,
        "api_url": AZURE_PRICING_API_BASE_URL
    })
    
    logger.info(f"Fetching Azure pricing data with filters: {filters}, skip: {skip}, top: {top}")
    
    # Build query parameters
    params = {}
    
    if filters:
        odata_filter = parse_odata_filter(filters)
        if odata_filter:
            params['$filter'] = odata_filter
            logger.log_internal_process("odata_filter_built", {
                "original_filters": filters,
                "odata_filter": odata_filter
            })
    
    if skip > 0:
        params['$skip'] = skip
    
    if top != 100:  # Only add if different from default
        params['$top'] = min(top, 1000)  # API limit is 1000
    
    logger.log_internal_process("api_request_params", {
        "params": params,
        "url": AZURE_PRICING_API_BASE_URL
    })
    
    # Make API request with retry logic
    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        for attempt in range(MAX_RETRIES):
            try:
                logger.debug(f"Making API request (attempt {attempt + 1}): {AZURE_PRICING_API_BASE_URL}")
                logger.debug(f"Parameters: {params}")
                
                logger.log_internal_process("api_request_attempt", {
                    "attempt": attempt + 1,
                    "max_retries": MAX_RETRIES,
                    "url": AZURE_PRICING_API_BASE_URL,
                    "params": params
                })
                
                response = await client.get(AZURE_PRICING_API_BASE_URL, params=params)
                response.raise_for_status()
                
                data = response.json()
                
                logger.log_internal_process("api_request_success", {
                    "attempt": attempt + 1,
                    "items_count": data.get('Count', 0),
                    "has_next_page": 'NextPageLink' in data,
                    "response_size_bytes": len(response.content)
                })
                
                logger.info(f"Successfully fetched {data.get('Count', 0)} pricing items")
                
                return data
                
            except httpx.HTTPStatusError as e:
                logger.log_internal_process("api_request_http_error", {
                    "attempt": attempt + 1,
                    "status_code": e.response.status_code,
                    "error_message": str(e)
                }, "WARNING")
                
                if e.response.status_code == 429:  # Rate limited
                    if attempt < MAX_RETRIES - 1:
                        wait_time = RETRY_DELAY * (2 ** attempt)  # Exponential backoff
                        logger.warning(f"Rate limited, waiting {wait_time}s before retry")
                        await asyncio.sleep(wait_time)
                        continue
                logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
                raise
            except httpx.RequestError as e:
                if attempt < MAX_RETRIES - 1:
                    wait_time = RETRY_DELAY * (2 ** attempt)
                    logger.warning(f"Request error, waiting {wait_time}s before retry: {e}")
                    await asyncio.sleep(wait_time)
                    continue
                logger.error(f"Request error: {e}")
                raise
    
    raise Exception(f"Failed to fetch data after {MAX_RETRIES} attempts")


def calculate_monthly_cost(hourly_rate: float, hours_per_month: int = 730) -> float:
    """Calculate monthly cost from hourly rate.
    
    Args:
        hourly_rate: Hourly rate in currency units
        hours_per_month: Number of hours per month (default: 730)
        
    Returns:
        Monthly cost
    """
    return hourly_rate * hours_per_month


def calculate_annual_cost(hourly_rate: float, hours_per_year: int = 8760) -> float:
    """Calculate annual cost from hourly rate.
    
    Args:
        hourly_rate: Hourly rate in currency units
        hours_per_year: Number of hours per year (default: 8760)
        
    Returns:
        Annual cost
    """
    return hourly_rate * hours_per_year


async def get_regional_pricing(
    service_name: str, 
    regions: List[str],
    product_name: Optional[str] = None,
    sku_name: Optional[str] = None
) -> Dict[str, List[Dict[str, Any]]]:
    """Compare pricing across multiple Azure regions.
    
    Args:
        service_name: Name of the Azure service
        regions: List of region names to compare
        product_name: Optional product name filter
        sku_name: Optional SKU name filter
        
    Returns:
        Dictionary with region names as keys and pricing data as values
    """
    logger.info(f"Comparing pricing for {service_name} across regions: {regions}")
    
    regional_pricing = {}
    
    for region in regions:
        filters = {
            'service_name': service_name,
            'arm_region_name': region
        }
        
        if product_name:
            filters['product_name'] = product_name
        if sku_name:
            filters['sku_name'] = sku_name
        
        try:
            data = await fetch_azure_pricing_data(filters)
            regional_pricing[region] = data.get('Items', [])
        except Exception as e:
            logger.error(f"Failed to fetch pricing for region {region}: {e}")
            regional_pricing[region] = []
    
    return regional_pricing


def format_pricing_data(raw_data: Dict[str, Any]) -> Dict[str, Any]:
    """Clean and structure pricing data for reports.
    
    Args:
        raw_data: Raw pricing data from API
        
    Returns:
        Formatted pricing data with additional calculated fields (optimized for readability)
    """
    if not raw_data or 'Items' not in raw_data:
        return {'items': [], 'summary': {}}
    
    items = raw_data['Items']
    formatted_items = []
    
    for item in items:
        formatted_item = {
            'service_name': item.get('serviceName', ''),
            'product_name': item.get('productName', ''),
            'sku_name': item.get('skuName', ''),
            'meter_name': item.get('meterName', ''),
            'location': item.get('location', ''),
            'arm_region_name': item.get('armRegionName', ''),
            'unit_price': item.get('unitPrice', 0),
            'retail_price': item.get('retailPrice', 0),
            'currency_code': item.get('currencyCode', DEFAULT_CURRENCY),
            'unit_of_measure': item.get('unitOfMeasure', ''),
            'service_family': item.get('serviceFamily', ''),
            'type': item.get('type', ''),
            'effective_start_date': item.get('effectiveStartDate', ''),
            # Calculated fields
            'monthly_cost': calculate_monthly_cost(item.get('unitPrice', 0)),
            'annual_cost': calculate_annual_cost(item.get('unitPrice', 0))
        }
        formatted_items.append(formatted_item)
    
    # Generate summary (simplified)
    summary = {
        'total_items': len(formatted_items),
        'unique_services': len(set(item['service_name'] for item in formatted_items)),
        'unique_regions': len(set(item['arm_region_name'] for item in formatted_items)),
        'currency': formatted_items[0]['currency_code'] if formatted_items else DEFAULT_CURRENCY,
        'price_range': {
            'min': min((item['unit_price'] for item in formatted_items), default=0),
            'max': max((item['unit_price'] for item in formatted_items), default=0)
        }
    }
    
    return {
        'items': formatted_items,
        'summary': summary
    }


def validate_region_name(region: str) -> bool:
    """Validate if a region name is valid Azure region.
    
    Args:
        region: Region name to validate
        
    Returns:
        True if valid, False otherwise
    """
    # Common Azure regions - this could be expanded or fetched from API
    valid_regions = {
        'eastus', 'eastus2', 'westus', 'westus2', 'westus3', 'centralus',
        'northcentralus', 'southcentralus', 'westcentralus',
        'northeurope', 'westeurope', 'uksouth', 'ukwest',
        'eastasia', 'southeastasia', 'japaneast', 'japanwest',
        'australiaeast', 'australiasoutheast', 'australiacentral',
        'brazilsouth', 'canadacentral', 'canadaeast',
        'francecentral', 'germanywestcentral', 'norwayeast',
        'switzerlandnorth', 'uaenorth', 'southafricanorth'
    }
    
    return region.lower() in valid_regions


def get_service_families() -> List[str]:
    """Get list of Azure service families.
    
    Returns:
        List of service family names
    """
    return [
        'Compute',
        'Storage',
        'Databases',
        'Networking',
        'Web',
        'Mobile',
        'Containers',
        'Analytics',
        'AI + Machine Learning',
        'Internet of Things',
        'Integration',
        'Security',
        'DevOps',
        'Management and Governance',
        'Migration'
    ]
