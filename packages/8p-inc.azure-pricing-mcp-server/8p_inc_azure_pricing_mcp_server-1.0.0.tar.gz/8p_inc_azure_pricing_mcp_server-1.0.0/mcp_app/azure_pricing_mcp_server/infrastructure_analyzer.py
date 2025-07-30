"""Infrastructure analysis functionality for Terraform and Bicep projects."""

import json
import logging
import os
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

logger = logging.getLogger(__name__)

# Azure resource type to service name mapping
AZURE_RESOURCE_MAPPING = {
    # Virtual Machines
    'azurerm_linux_virtual_machine': 'Virtual Machines',
    'azurerm_windows_virtual_machine': 'Virtual Machines',
    'azurerm_virtual_machine': 'Virtual Machines',
    
    # Storage
    'azurerm_storage_account': 'Storage',
    'azurerm_storage_blob': 'Storage',
    'azurerm_storage_container': 'Storage',
    
    # App Service
    'azurerm_app_service': 'App Service',
    'azurerm_app_service_plan': 'App Service',
    'azurerm_linux_web_app': 'App Service',
    'azurerm_windows_web_app': 'App Service',
    
    # SQL Database
    'azurerm_sql_server': 'SQL Database',
    'azurerm_sql_database': 'SQL Database',
    'azurerm_mssql_server': 'SQL Database',
    'azurerm_mssql_database': 'SQL Database',
    
    # Functions
    'azurerm_function_app': 'Azure Functions',
    'azurerm_linux_function_app': 'Azure Functions',
    'azurerm_windows_function_app': 'Azure Functions',
    
    # Kubernetes
    'azurerm_kubernetes_cluster': 'Kubernetes Service',
    
    # Container Instances
    'azurerm_container_group': 'Container Instances',
    
    # Cosmos DB
    'azurerm_cosmosdb_account': 'Cosmos DB',
    'azurerm_cosmosdb_sql_database': 'Cosmos DB',
    
    # Redis Cache
    'azurerm_redis_cache': 'Azure Cache for Redis',
    
    # Service Bus
    'azurerm_servicebus_namespace': 'Service Bus',
    'azurerm_servicebus_queue': 'Service Bus',
    
    # Application Gateway
    'azurerm_application_gateway': 'Application Gateway',
    
    # Load Balancer
    'azurerm_lb': 'Load Balancer',
    
    # Virtual Network
    'azurerm_virtual_network': 'Virtual Network',
    'azurerm_subnet': 'Virtual Network',
    
    # Key Vault
    'azurerm_key_vault': 'Key Vault',
    
    # Monitor
    'azurerm_log_analytics_workspace': 'Azure Monitor',
    'azurerm_application_insights': 'Application Insights'
}

class TerraformAnalyzer:
    """Analyzer for Terraform projects."""
    
    def __init__(self, project_path: str):
        """Initialize the analyzer.
        
        Args:
            project_path: Path to the Terraform project
        """
        self.project_path = Path(project_path)
        self.terraform_files = []
        self.resources = []
        
    def analyze(self) -> Dict[str, Any]:
        """Analyze the Terraform project.
        
        Returns:
            Analysis results
        """
        logger.info(f"Analyzing Terraform project at {self.project_path}")
        
        try:
            # Find Terraform files
            self._find_terraform_files()
            
            if not self.terraform_files:
                return {
                    'status': 'error',
                    'message': 'No Terraform files found in the project',
                    'path': str(self.project_path)
                }
            
            # Parse Terraform files
            self._parse_terraform_files()
            
            # Analyze resources
            analysis = self._analyze_resources()
            
            return {
                'status': 'success',
                'project_path': str(self.project_path),
                'analysis': analysis
            }
            
        except Exception as e:
            logger.error(f"Error analyzing Terraform project: {e}")
            return {
                'status': 'error',
                'message': f'Analysis failed: {str(e)}',
                'path': str(self.project_path)
            }
    
    def _find_terraform_files(self):
        """Find all Terraform files in the project."""
        terraform_extensions = ['.tf', '.tf.json']
        
        for ext in terraform_extensions:
            self.terraform_files.extend(
                self.project_path.rglob(f'*{ext}')
            )
        
        logger.info(f"Found {len(self.terraform_files)} Terraform files")
    
    def _parse_terraform_files(self):
        """Parse Terraform files to extract resources."""
        for tf_file in self.terraform_files:
            try:
                if tf_file.suffix == '.tf':
                    self._parse_hcl_file(tf_file)
                elif tf_file.suffix == '.json':
                    self._parse_json_file(tf_file)
            except Exception as e:
                logger.warning(f"Error parsing {tf_file}: {e}")
                continue
    
    def _parse_hcl_file(self, file_path: Path):
        """Parse HCL Terraform file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Simple regex-based parsing for resource blocks
        resource_pattern = r'resource\s+"([^"]+)"\s+"([^"]+)"\s*\{'
        matches = re.findall(resource_pattern, content)
        
        for resource_type, resource_name in matches:
            self.resources.append({
                'type': resource_type,
                'name': resource_name,
                'file': str(file_path.relative_to(self.project_path)),
                'service': AZURE_RESOURCE_MAPPING.get(resource_type, 'Unknown Service')
            })
    
    def _parse_json_file(self, file_path: Path):
        """Parse JSON Terraform file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'resource' in data:
            for resource_type, resources in data['resource'].items():
                for resource_name in resources.keys():
                    self.resources.append({
                        'type': resource_type,
                        'name': resource_name,
                        'file': str(file_path.relative_to(self.project_path)),
                        'service': AZURE_RESOURCE_MAPPING.get(resource_type, 'Unknown Service')
                    })
    
    def _analyze_resources(self) -> Dict[str, Any]:
        """Analyze the extracted resources."""
        if not self.resources:
            return {
                'total_resources': 0,
                'services': {},
                'message': 'No Azure resources found in Terraform files'
            }
        
        # Group resources by service
        services = {}
        for resource in self.resources:
            service = resource['service']
            if service not in services:
                services[service] = {
                    'count': 0,
                    'resources': []
                }
            
            services[service]['count'] += 1
            services[service]['resources'].append({
                'type': resource['type'],
                'name': resource['name'],
                'file': resource['file']
            })
        
        # Create summary
        analysis = {
            'total_resources': len(self.resources),
            'total_files': len(self.terraform_files),
            'unique_services': len(services),
            'services': services,
            'service_summary': [
                {
                    'service': service,
                    'resource_count': data['count'],
                    'pricing_available': service in ['Virtual Machines', 'Storage', 'App Service', 'SQL Database', 'Azure Functions']
                }
                for service, data in services.items()
            ]
        }
        
        return analysis


class BicepAnalyzer:
    """Analyzer for Bicep projects."""
    
    def __init__(self, project_path: str):
        """Initialize the analyzer.
        
        Args:
            project_path: Path to the Bicep project
        """
        self.project_path = Path(project_path)
        self.bicep_files = []
        self.resources = []
    
    def analyze(self) -> Dict[str, Any]:
        """Analyze the Bicep project.
        
        Returns:
            Analysis results
        """
        logger.info(f"Analyzing Bicep project at {self.project_path}")
        
        try:
            # Find Bicep files
            self._find_bicep_files()
            
            if not self.bicep_files:
                return {
                    'status': 'error',
                    'message': 'No Bicep files found in the project',
                    'path': str(self.project_path)
                }
            
            # Parse Bicep files
            self._parse_bicep_files()
            
            # Analyze resources
            analysis = self._analyze_resources()
            
            return {
                'status': 'success',
                'project_path': str(self.project_path),
                'analysis': analysis
            }
            
        except Exception as e:
            logger.error(f"Error analyzing Bicep project: {e}")
            return {
                'status': 'error',
                'message': f'Analysis failed: {str(e)}',
                'path': str(self.project_path)
            }
    
    def _find_bicep_files(self):
        """Find all Bicep files in the project."""
        self.bicep_files.extend(self.project_path.rglob('*.bicep'))
        logger.info(f"Found {len(self.bicep_files)} Bicep files")
    
    def _parse_bicep_files(self):
        """Parse Bicep files to extract resources."""
        for bicep_file in self.bicep_files:
            try:
                self._parse_bicep_file(bicep_file)
            except Exception as e:
                logger.warning(f"Error parsing {bicep_file}: {e}")
                continue
    
    def _parse_bicep_file(self, file_path: Path):
        """Parse a single Bicep file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse resource declarations
        resource_pattern = r'resource\s+(\w+)\s+\'([^\']+)\'\s*='
        matches = re.findall(resource_pattern, content)
        
        for resource_name, resource_type in matches:
            # Convert ARM resource type to service
            service = self._arm_type_to_service(resource_type)
            
            self.resources.append({
                'type': resource_type,
                'name': resource_name,
                'file': str(file_path.relative_to(self.project_path)),
                'service': service
            })
    
    def _arm_type_to_service(self, arm_type: str) -> str:
        """Convert ARM resource type to Azure service name."""
        # Remove API version from ARM type (e.g., Microsoft.Compute/virtualMachines@2021-03-01)
        clean_type = arm_type.split('@')[0] if '@' in arm_type else arm_type
        
        # ARM resource types are like Microsoft.Compute/virtualMachines
        type_mapping = {
            'Microsoft.Compute/virtualMachines': 'Virtual Machines',
            'Microsoft.Storage/storageAccounts': 'Storage',
            'Microsoft.Web/sites': 'App Service',
            'Microsoft.Web/serverfarms': 'App Service',
            'Microsoft.Sql/servers': 'SQL Database',
            'Microsoft.Sql/servers/databases': 'SQL Database',
            'Microsoft.Web/sites/functions': 'Azure Functions',
            'Microsoft.ContainerService/managedClusters': 'Kubernetes Service',
            'Microsoft.ContainerInstance/containerGroups': 'Container Instances',
            'Microsoft.DocumentDB/databaseAccounts': 'Cosmos DB',
            'Microsoft.Cache/Redis': 'Azure Cache for Redis',
            'Microsoft.ServiceBus/namespaces': 'Service Bus',
            'Microsoft.Network/applicationGateways': 'Application Gateway',
            'Microsoft.Network/loadBalancers': 'Load Balancer',
            'Microsoft.Network/virtualNetworks': 'Virtual Network',
            'Microsoft.KeyVault/vaults': 'Key Vault',
            'Microsoft.OperationalInsights/workspaces': 'Azure Monitor',
            'Microsoft.Insights/components': 'Application Insights'
        }
        
        return type_mapping.get(clean_type, f'Unknown Service ({clean_type})')
    
    def _analyze_resources(self) -> Dict[str, Any]:
        """Analyze the extracted resources."""
        if not self.resources:
            return {
                'total_resources': 0,
                'services': {},
                'message': 'No Azure resources found in Bicep files'
            }
        
        # Group resources by service
        services = {}
        for resource in self.resources:
            service = resource['service']
            if service not in services:
                services[service] = {
                    'count': 0,
                    'resources': []
                }
            
            services[service]['count'] += 1
            services[service]['resources'].append({
                'type': resource['type'],
                'name': resource['name'],
                'file': resource['file']
            })
        
        # Create summary
        analysis = {
            'total_resources': len(self.resources),
            'total_files': len(self.bicep_files),
            'unique_services': len(services),
            'services': services,
            'service_summary': [
                {
                    'service': service,
                    'resource_count': data['count'],
                    'pricing_available': service in ['Virtual Machines', 'Storage', 'App Service', 'SQL Database', 'Azure Functions']
                }
                for service, data in services.items()
            ]
        }
        
        return analysis


def analyze_terraform_project(project_path: str) -> Dict[str, Any]:
    """Analyze a Terraform project for Azure resources.
    
    Args:
        project_path: Path to the Terraform project
        
    Returns:
        Analysis results
    """
    analyzer = TerraformAnalyzer(project_path)
    return analyzer.analyze()


def analyze_bicep_project(project_path: str) -> Dict[str, Any]:
    """Analyze a Bicep project for Azure resources.
    
    Args:
        project_path: Path to the Bicep project
        
    Returns:
        Analysis results
    """
    analyzer = BicepAnalyzer(project_path)
    return analyzer.analyze()
