"""Tests for helper functions."""

import pytest
from unittest.mock import AsyncMock, patch

from mcp_app.azure_pricing_mcp_server.helpers import (
    parse_odata_filter,
    calculate_monthly_cost,
    calculate_annual_cost,
    validate_region_name,
    format_pricing_data,
    _snake_to_camel
)


class TestHelperFunctions:
    """Test helper functions."""
    
    def test_snake_to_camel(self):
        """Test snake_case to camelCase conversion."""
        assert _snake_to_camel('service_name') == 'serviceName'
        assert _snake_to_camel('arm_region_name') == 'armRegionName'
        assert _snake_to_camel('product_name') == 'productName'
        assert _snake_to_camel('simple') == 'simple'
    
    def test_parse_odata_filter(self):
        """Test OData filter parsing."""
        # Test empty filter
        assert parse_odata_filter({}) == ''
        assert parse_odata_filter(None) == ''
        
        # Test single string filter
        result = parse_odata_filter({'service_name': 'Virtual Machines'})
        assert result == "serviceName eq 'Virtual Machines'"
        
        # Test multiple filters
        result = parse_odata_filter({
            'service_name': 'Virtual Machines',
            'arm_region_name': 'eastus'
        })
        assert "serviceName eq 'Virtual Machines'" in result
        assert "armRegionName eq 'eastus'" in result
        assert ' and ' in result
        
        # Test numeric filter
        result = parse_odata_filter({'tier_minimum_units': 0})
        assert result == "tierMinimumUnits eq 0"
        
        # Test list filter
        result = parse_odata_filter({'arm_region_name': ['eastus', 'westus']})
        expected = "(armRegionName eq 'eastus' or armRegionName eq 'westus')"
        assert result == expected
    
    def test_calculate_monthly_cost(self):
        """Test monthly cost calculation."""
        assert calculate_monthly_cost(0.096) == 0.096 * 730
        assert calculate_monthly_cost(0.096, 744) == 0.096 * 744
        assert calculate_monthly_cost(0) == 0
    
    def test_calculate_annual_cost(self):
        """Test annual cost calculation."""
        assert calculate_annual_cost(0.096) == 0.096 * 8760
        assert calculate_annual_cost(0.096, 8784) == 0.096 * 8784
        assert calculate_annual_cost(0) == 0
    
    def test_validate_region_name(self):
        """Test region name validation."""
        # Valid regions
        assert validate_region_name('eastus') is True
        assert validate_region_name('westeurope') is True
        assert validate_region_name('EASTUS') is True  # Case insensitive
        
        # Invalid regions
        assert validate_region_name('invalid-region') is False
        assert validate_region_name('') is False
        assert validate_region_name('mars-central') is False
    
    def test_format_pricing_data(self):
        """Test pricing data formatting."""
        # Test empty data
        result = format_pricing_data({})
        assert result == {'items': [], 'summary': {}}
        
        result = format_pricing_data({'Items': []})
        expected_summary = {
            'total_items': 0,
            'unique_services': 0,
            'unique_regions': 0,
            'currency': 'USD',
            'price_range': {'min': 0, 'max': 0}
        }
        assert result['summary'] == expected_summary
        
        # Test with sample data
        sample_data = {
            'Items': [
                {
                    'serviceName': 'Virtual Machines',
                    'productName': 'Virtual Machines Dv3 Series',
                    'skuName': 'D2s v3',
                    'meterName': 'D2s v3',
                    'location': 'US East',
                    'armRegionName': 'eastus',
                    'unitPrice': 0.096,
                    'retailPrice': 0.096,
                    'currencyCode': 'USD',
                    'unitOfMeasure': '1 Hour',
                    'serviceFamily': 'Compute',
                    'type': 'Consumption',
                    'effectiveStartDate': '2023-01-01T00:00:00Z'
                }
            ],
            'BillingCurrency': 'USD',
            'CustomerEntityType': 'Retail',
            'Count': 1
        }
        
        result = format_pricing_data(sample_data)
        
        assert len(result['items']) == 1
        assert result['items'][0]['service_name'] == 'Virtual Machines'
        assert result['items'][0]['unit_price'] == 0.096
        assert result['items'][0]['monthly_cost'] == 0.096 * 730
        assert result['summary']['total_items'] == 1
        assert result['summary']['unique_services'] == 1
        assert result['metadata']['billing_currency'] == 'USD'


@pytest.mark.asyncio
class TestAsyncHelpers:
    """Test async helper functions."""
    
    @patch('mcp_app.azure_pricing_mcp_server.helpers.httpx.AsyncClient')
    async def test_fetch_azure_pricing_data_success(self, mock_client):
        """Test successful API data fetch."""
        # Mock response
        mock_response = AsyncMock()
        mock_response.json.return_value = {
            'Items': [{'serviceName': 'Virtual Machines'}],
            'Count': 1
        }
        mock_response.raise_for_status.return_value = None
        
        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response
        mock_client.return_value.__aenter__.return_value = mock_client_instance
        
        from mcp_app.azure_pricing_mcp_server.helpers import fetch_azure_pricing_data
        
        result = await fetch_azure_pricing_data({'service_name': 'Virtual Machines'})
        
        assert result['Count'] == 1
        assert len(result['Items']) == 1
        mock_client_instance.get.assert_called_once()
    
    @patch('mcp_app.azure_pricing_mcp_server.helpers.httpx.AsyncClient')
    async def test_fetch_azure_pricing_data_http_error(self, mock_client):
        """Test API HTTP error handling."""
        import httpx
        
        # Mock HTTP error
        mock_response = AsyncMock()
        mock_response.status_code = 404
        mock_response.text = 'Not Found'
        
        mock_client_instance = AsyncMock()
        mock_client_instance.get.side_effect = httpx.HTTPStatusError(
            'Not Found', request=AsyncMock(), response=mock_response
        )
        mock_client.return_value.__aenter__.return_value = mock_client_instance
        
        from mcp_app.azure_pricing_mcp_server.helpers import fetch_azure_pricing_data
        
        with pytest.raises(httpx.HTTPStatusError):
            await fetch_azure_pricing_data({'service_name': 'Invalid'})


if __name__ == '__main__':
    pytest.main([__file__])
