"""Azure architecture patterns with cost considerations."""

import logging
from typing import Any, Dict, List

logger = logging.getLogger(__name__)

# Azure architecture patterns with cost information
AZURE_PATTERNS = {
    "web-app-basic": {
        "name": "Basic Web Application",
        "description": "Simple web application with App Service and SQL Database",
        "use_cases": [
            "Small business websites",
            "Personal portfolios",
            "Simple web applications"
        ],
        "components": [
            {
                "service": "App Service",
                "sku": "B1 Basic",
                "purpose": "Web application hosting",
                "estimated_monthly_cost": "$13.14"
            },
            {
                "service": "SQL Database",
                "sku": "Basic (5 DTU)",
                "purpose": "Application database",
                "estimated_monthly_cost": "$4.90"
            }
        ],
        "total_estimated_cost": "$18.04/month",
        "cost_optimization": [
            "Use F1 Free tier for development/testing",
            "Consider Azure Database for MySQL/PostgreSQL for lower costs",
            "Implement auto-scaling for variable workloads"
        ]
    },
    
    "web-app-scalable": {
        "name": "Scalable Web Application",
        "description": "Production web application with load balancing and caching",
        "use_cases": [
            "E-commerce websites",
            "SaaS applications",
            "High-traffic web applications"
        ],
        "components": [
            {
                "service": "App Service",
                "sku": "S2 Standard",
                "purpose": "Web application hosting with auto-scaling",
                "estimated_monthly_cost": "$146.00"
            },
            {
                "service": "SQL Database",
                "sku": "S2 Standard (50 DTU)",
                "purpose": "Application database",
                "estimated_monthly_cost": "$30.00"
            },
            {
                "service": "Azure Cache for Redis",
                "sku": "C1 Basic",
                "purpose": "Application caching",
                "estimated_monthly_cost": "$16.06"
            },
            {
                "service": "Application Gateway",
                "sku": "Standard_v2",
                "purpose": "Load balancing and SSL termination",
                "estimated_monthly_cost": "$22.63"
            }
        ],
        "total_estimated_cost": "$214.69/month",
        "cost_optimization": [
            "Use Azure Reserved Instances for predictable workloads",
            "Implement CDN for static content delivery",
            "Consider Azure Functions for event-driven components"
        ]
    },
    
    "microservices": {
        "name": "Microservices Architecture",
        "description": "Container-based microservices with Kubernetes",
        "use_cases": [
            "Large enterprise applications",
            "Cloud-native applications",
            "DevOps-focused organizations"
        ],
        "components": [
            {
                "service": "Kubernetes Service",
                "sku": "Standard cluster",
                "purpose": "Container orchestration",
                "estimated_monthly_cost": "$73.00"
            },
            {
                "service": "Virtual Machines",
                "sku": "Standard_D2s_v3 (3 nodes)",
                "purpose": "Kubernetes worker nodes",
                "estimated_monthly_cost": "$210.00"
            },
            {
                "service": "Container Registry",
                "sku": "Basic",
                "purpose": "Container image storage",
                "estimated_monthly_cost": "$5.00"
            },
            {
                "service": "Cosmos DB",
                "sku": "400 RU/s",
                "purpose": "NoSQL database",
                "estimated_monthly_cost": "$23.36"
            }
        ],
        "total_estimated_cost": "$311.36/month",
        "cost_optimization": [
            "Use Spot instances for non-critical workloads",
            "Implement horizontal pod autoscaling",
            "Consider Azure Container Instances for burst workloads"
        ]
    },
    
    "serverless": {
        "name": "Serverless Architecture",
        "description": "Event-driven serverless application with Functions and Logic Apps",
        "use_cases": [
            "Event processing",
            "API backends",
            "Data processing pipelines"
        ],
        "components": [
            {
                "service": "Azure Functions",
                "sku": "Consumption plan",
                "purpose": "Serverless compute",
                "estimated_monthly_cost": "$0.20 per million executions"
            },
            {
                "service": "Logic Apps",
                "sku": "Consumption",
                "purpose": "Workflow orchestration",
                "estimated_monthly_cost": "$0.000025 per action"
            },
            {
                "service": "Cosmos DB",
                "sku": "Serverless",
                "purpose": "NoSQL database",
                "estimated_monthly_cost": "$0.25 per million RUs"
            },
            {
                "service": "Service Bus",
                "sku": "Basic",
                "purpose": "Message queuing",
                "estimated_monthly_cost": "$0.05 per million operations"
            }
        ],
        "total_estimated_cost": "Pay-per-use (typically $10-50/month for small workloads)",
        "cost_optimization": [
            "Monitor function execution times to avoid timeouts",
            "Use durable functions for long-running processes",
            "Implement efficient data access patterns"
        ]
    },
    
    "data-analytics": {
        "name": "Data Analytics Platform",
        "description": "Big data processing and analytics with Azure Data services",
        "use_cases": [
            "Business intelligence",
            "Data warehousing",
            "Real-time analytics"
        ],
        "components": [
            {
                "service": "Azure Synapse Analytics",
                "sku": "DW100c",
                "purpose": "Data warehouse",
                "estimated_monthly_cost": "$1,200.00"
            },
            {
                "service": "Azure Data Factory",
                "sku": "Standard",
                "purpose": "Data integration",
                "estimated_monthly_cost": "$500.00"
            },
            {
                "service": "Storage",
                "sku": "Standard_LRS (1TB)",
                "purpose": "Data lake storage",
                "estimated_monthly_cost": "$20.48"
            },
            {
                "service": "Power BI",
                "sku": "Pro",
                "purpose": "Data visualization",
                "estimated_monthly_cost": "$10.00 per user"
            }
        ],
        "total_estimated_cost": "$1,730.48/month + $10/user",
        "cost_optimization": [
            "Use pause/resume for Synapse Analytics during off-hours",
            "Implement data lifecycle management",
            "Consider Azure Data Lake Analytics for ad-hoc queries"
        ]
    },
    
    "iot-solution": {
        "name": "IoT Solution",
        "description": "Internet of Things platform with device management and analytics",
        "use_cases": [
            "Smart city solutions",
            "Industrial IoT",
            "Connected devices"
        ],
        "components": [
            {
                "service": "IoT Hub",
                "sku": "S1 Standard",
                "purpose": "Device connectivity",
                "estimated_monthly_cost": "$25.00"
            },
            {
                "service": "Stream Analytics",
                "sku": "1 SU",
                "purpose": "Real-time data processing",
                "estimated_monthly_cost": "$80.30"
            },
            {
                "service": "Cosmos DB",
                "sku": "400 RU/s",
                "purpose": "Device data storage",
                "estimated_monthly_cost": "$23.36"
            },
            {
                "service": "Time Series Insights",
                "sku": "S1",
                "purpose": "Time series analytics",
                "estimated_monthly_cost": "$150.00"
            }
        ],
        "total_estimated_cost": "$278.66/month",
        "cost_optimization": [
            "Use device-to-cloud message batching",
            "Implement data retention policies",
            "Consider Azure Digital Twins for complex scenarios"
        ]
    }
}


def get_architecture_patterns(pattern_name: str = None) -> Dict[str, Any]:
    """Get Azure architecture patterns with cost information.
    
    Args:
        pattern_name: Specific pattern name to retrieve (optional)
        
    Returns:
        Dictionary containing architecture patterns
    """
    logger.info(f"Getting architecture patterns: {pattern_name or 'all'}")
    
    if pattern_name:
        pattern_key = pattern_name.lower().replace(' ', '-').replace('_', '-')
        if pattern_key in AZURE_PATTERNS:
            return {
                'status': 'success',
                'pattern': AZURE_PATTERNS[pattern_key],
                'pattern_name': pattern_name
            }
        else:
            return {
                'status': 'error',
                'message': f'Pattern not found: {pattern_name}',
                'available_patterns': list(AZURE_PATTERNS.keys())
            }
    else:
        # Return all patterns with summary
        patterns_summary = []
        for key, pattern in AZURE_PATTERNS.items():
            patterns_summary.append({
                'key': key,
                'name': pattern['name'],
                'description': pattern['description'],
                'estimated_cost': pattern['total_estimated_cost'],
                'components_count': len(pattern['components'])
            })
        
        return {
            'status': 'success',
            'total_patterns': len(AZURE_PATTERNS),
            'patterns': patterns_summary
        }


def get_pattern_cost_breakdown(pattern_name: str) -> Dict[str, Any]:
    """Get detailed cost breakdown for a specific pattern.
    
    Args:
        pattern_name: Name of the architecture pattern
        
    Returns:
        Dictionary containing detailed cost breakdown
    """
    logger.info(f"Getting cost breakdown for pattern: {pattern_name}")
    
    pattern_key = pattern_name.lower().replace(' ', '-').replace('_', '-')
    
    if pattern_key not in AZURE_PATTERNS:
        return {
            'status': 'error',
            'message': f'Pattern not found: {pattern_name}',
            'available_patterns': list(AZURE_PATTERNS.keys())
        }
    
    pattern = AZURE_PATTERNS[pattern_key]
    
    # Calculate cost breakdown
    total_monthly = 0
    component_costs = []
    
    for component in pattern['components']:
        cost_str = component.get('estimated_monthly_cost', '$0')
        # Extract numeric value from cost string
        try:
            if 'per' in cost_str.lower():
                # Usage-based pricing
                cost_value = 0
            else:
                cost_value = float(cost_str.replace('$', '').replace(',', '').split('/')[0])
                total_monthly += cost_value
        except (ValueError, AttributeError):
            cost_value = 0
        
        component_costs.append({
            'service': component['service'],
            'sku': component['sku'],
            'purpose': component['purpose'],
            'monthly_cost': cost_str,
            'numeric_cost': cost_value
        })
    
    return {
        'status': 'success',
        'pattern_name': pattern['name'],
        'total_monthly_cost': f"${total_monthly:.2f}",
        'total_annual_cost': f"${total_monthly * 12:.2f}",
        'component_breakdown': component_costs,
        'cost_optimization_tips': pattern['cost_optimization']
    }
