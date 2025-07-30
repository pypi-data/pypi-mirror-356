#!/usr/bin/env python3
"""Test infrastructure analysis functionality."""

import asyncio
import tempfile
import os
from pathlib import Path
from mcp_app.azure_pricing_mcp_server.server import analyze_terraform_project, analyze_bicep_project

async def test_infrastructure_analysis():
    """Test infrastructure analysis tools."""
    print("Testing Azure infrastructure analysis...\n")
    
    # Create temporary test projects
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Test Terraform analysis
        print("1. Testing Terraform project analysis...")
        tf_project = temp_path / "terraform_test"
        tf_project.mkdir()
        
        # Create sample Terraform file
        tf_file = tf_project / "main.tf"
        tf_content = '''
resource "azurerm_resource_group" "main" {
  name     = "rg-test"
  location = "East US"
}

resource "azurerm_linux_virtual_machine" "web" {
  name                = "vm-web"
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  size                = "Standard_B2s"
}

resource "azurerm_storage_account" "main" {
  name                     = "storagetest"
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_app_service_plan" "main" {
  name                = "asp-test"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  
  sku {
    tier = "Standard"
    size = "S1"
  }
}
'''
        tf_file.write_text(tf_content)
        
        # Test Terraform analysis
        tf_result = await analyze_terraform_project(str(tf_project))
        print(f"Terraform Status: {tf_result.get('status')}")
        print(f"Response size: {len(str(tf_result))} characters")
        
        if tf_result.get('status') == 'success':
            summary = tf_result.get('summary', {})
            print(f"  Total resources: {summary.get('total_resources')}")
            print(f"  Unique services: {summary.get('unique_services')}")
            print(f"  Services found: {len(tf_result.get('services_found', []))}")
            print(f"  Pricing recommendations: {len(tf_result.get('pricing_recommendations', []))}")
        
        # Test Bicep analysis
        print("\n2. Testing Bicep project analysis...")
        bicep_project = temp_path / "bicep_test"
        bicep_project.mkdir()
        
        # Create sample Bicep file
        bicep_file = bicep_project / "main.bicep"
        bicep_content = '''
resource rg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: 'rg-test'
  location: 'eastus'
}

resource vm 'Microsoft.Compute/virtualMachines@2021-03-01' = {
  name: 'vm-web'
  location: rg.location
  properties: {
    hardwareProfile: {
      vmSize: 'Standard_B2s'
    }
  }
}

resource storage 'Microsoft.Storage/storageAccounts@2021-04-01' = {
  name: 'storagetest'
  location: rg.location
  kind: 'StorageV2'
  sku: {
    name: 'Standard_LRS'
  }
}

resource appServicePlan 'Microsoft.Web/serverfarms@2021-02-01' = {
  name: 'asp-test'
  location: rg.location
  sku: {
    name: 'S1'
    tier: 'Standard'
  }
}
'''
        bicep_file.write_text(bicep_content)
        
        # Test Bicep analysis
        bicep_result = await analyze_bicep_project(str(bicep_project))
        print(f"Bicep Status: {bicep_result.get('status')}")
        print(f"Response size: {len(str(bicep_result))} characters")
        
        if bicep_result.get('status') == 'success':
            summary = bicep_result.get('summary', {})
            print(f"  Total resources: {summary.get('total_resources')}")
            print(f"  Unique services: {summary.get('unique_services')}")
            print(f"  Services found: {len(bicep_result.get('services_found', []))}")
            print(f"  Pricing recommendations: {len(bicep_result.get('pricing_recommendations', []))}")
        
        # Test error handling
        print("\n3. Testing error handling...")
        empty_project = temp_path / "empty_test"
        empty_project.mkdir()
        
        empty_result = await analyze_terraform_project(str(empty_project))
        print(f"Empty project status: {empty_result.get('status')}")
        print(f"Error message: {empty_result.get('message', 'No error message')}")
    
    print("\n✅ Infrastructure analysis test completed!")

if __name__ == '__main__':
    asyncio.run(test_infrastructure_analysis())
