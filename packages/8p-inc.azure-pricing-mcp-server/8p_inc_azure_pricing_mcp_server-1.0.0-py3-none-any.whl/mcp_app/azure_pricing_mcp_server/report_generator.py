"""Report generation functionality for Azure pricing analysis."""

import json
import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class AzurePricingReportGenerator:
    """Generator for Azure pricing analysis reports."""
    
    def __init__(self):
        """Initialize the report generator."""
        self.report_data = {}
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    def generate_cost_report(
        self,
        pricing_data: Dict[str, Any],
        report_format: str = "markdown",
        include_recommendations: bool = True
    ) -> str:
        """Generate a comprehensive cost analysis report.
        
        Args:
            pricing_data: Pricing data from various sources
            report_format: Output format ('markdown' or 'csv')
            include_recommendations: Whether to include optimization recommendations
            
        Returns:
            Generated report as string
        """
        logger.info(f"Generating {report_format} cost report")
        
        if report_format.lower() == "csv":
            return self._generate_csv_report(pricing_data, include_recommendations)
        else:
            return self._generate_markdown_report(pricing_data, include_recommendations)
    
    def _generate_markdown_report(
        self,
        pricing_data: Dict[str, Any],
        include_recommendations: bool
    ) -> str:
        """Generate a markdown format report."""
        
        report_lines = [
            "# Azure Pricing Analysis Report",
            f"*Generated on {self.timestamp}*",
            "",
            "## Executive Summary",
            ""
        ]
        
        # Add executive summary
        if 'summary' in pricing_data:
            summary = pricing_data['summary']
            report_lines.extend([
                f"- **Total Services Analyzed**: {summary.get('total_services', 'N/A')}",
                f"- **Regions Covered**: {summary.get('regions_covered', 'N/A')}",
                f"- **Estimated Monthly Cost**: {summary.get('estimated_monthly_cost', 'N/A')}",
                f"- **Estimated Annual Cost**: {summary.get('estimated_annual_cost', 'N/A')}",
                ""
            ])
        
        # Add pricing details
        if 'services' in pricing_data:
            report_lines.extend([
                "## Service Pricing Details",
                ""
            ])
            
            for service_name, service_data in pricing_data['services'].items():
                report_lines.extend([
                    f"### {service_name}",
                    ""
                ])
                
                if isinstance(service_data, dict):
                    if 'pricing' in service_data:
                        pricing = service_data['pricing']
                        report_lines.extend([
                            f"- **Hourly Rate**: {pricing.get('hourly', 'N/A')}",
                            f"- **Monthly Estimate**: {pricing.get('monthly', 'N/A')}",
                            f"- **Annual Estimate**: {pricing.get('annual', 'N/A')}",
                            f"- **SKU**: {service_data.get('sku', 'N/A')}",
                            f"- **Region**: {service_data.get('region', 'N/A')}",
                            ""
                        ])
                    
                    if 'free_tier' in service_data and service_data['free_tier']:
                        report_lines.extend([
                            "#### Free Tier Information",
                            f"{service_data['free_tier']}",
                            ""
                        ])
        
        # Add regional comparison if available
        if 'regional_comparison' in pricing_data:
            comparison = pricing_data['regional_comparison']
            report_lines.extend([
                "## Regional Price Comparison",
                "",
                "| Region | Average Hourly Rate | Monthly Estimate |",
                "|--------|-------------------|------------------|"
            ])
            
            for region, data in comparison.items():
                if isinstance(data, dict) and 'average_hourly_price' in data:
                    report_lines.append(
                        f"| {region} | {data['average_hourly_price']} | {data.get('average_monthly_cost', 'N/A')} |"
                    )
            
            report_lines.append("")
        
        # Add infrastructure analysis if available
        if 'infrastructure' in pricing_data:
            infra = pricing_data['infrastructure']
            report_lines.extend([
                "## Infrastructure Analysis",
                "",
                f"- **Project Type**: {infra.get('project_type', 'N/A')}",
                f"- **Total Resources**: {infra.get('total_resources', 'N/A')}",
                f"- **Unique Services**: {infra.get('unique_services', 'N/A')}",
                ""
            ])
            
            if 'services_found' in infra:
                report_lines.extend([
                    "### Resources by Service",
                    ""
                ])
                
                for service in infra['services_found']:
                    pricing_status = "✅ Pricing Available" if service.get('pricing_available') else "❌ Pricing Not Available"
                    report_lines.append(f"- **{service['service']}**: {service['resource_count']} resources | {pricing_status}")
                
                report_lines.append("")
        
        # Add recommendations
        if include_recommendations:
            report_lines.extend([
                "## Cost Optimization Recommendations",
                ""
            ])
            
            if 'recommendations' in pricing_data:
                for rec in pricing_data['recommendations']:
                    report_lines.append(f"- {rec}")
            else:
                # Default recommendations
                report_lines.extend([
                    "- Consider using Azure Reserved Instances for predictable workloads",
                    "- Implement auto-scaling to optimize resource utilization",
                    "- Use Azure Spot VMs for non-critical workloads",
                    "- Regularly review and right-size your resources",
                    "- Consider Azure Hybrid Benefit for Windows Server and SQL Server",
                    "- Use Azure Cost Management tools for ongoing monitoring"
                ])
            
            report_lines.append("")
        
        # Add footer
        report_lines.extend([
            "---",
            "",
            "## Report Notes",
            "",
            "- Pricing data is based on current Azure retail prices",
            "- Estimates are for planning purposes and may vary based on actual usage",
            "- Consider additional costs like data transfer, support plans, and third-party services",
            "- Prices are subject to change; verify current pricing on Azure portal",
            "",
            f"*Report generated by Azure Pricing MCP Server on {self.timestamp}*"
        ])
        
        return "\n".join(report_lines)
    
    def _generate_csv_report(
        self,
        pricing_data: Dict[str, Any],
        include_recommendations: bool
    ) -> str:
        """Generate a CSV format report."""
        
        csv_lines = [
            "# Azure Pricing Analysis Report (CSV Format)",
            f"# Generated on {self.timestamp}",
            "",
            "## Service Pricing Data",
            "Service,SKU,Region,Hourly_Rate,Monthly_Estimate,Annual_Estimate,Free_Tier_Available"
        ]
        
        # Add service pricing data
        if 'services' in pricing_data:
            for service_name, service_data in pricing_data['services'].items():
                if isinstance(service_data, dict) and 'pricing' in service_data:
                    pricing = service_data['pricing']
                    hourly = pricing.get('hourly', '').replace('$', '')
                    monthly = pricing.get('monthly', '').replace('$', '')
                    annual = pricing.get('annual', '').replace('$', '')
                    free_tier = 'Yes' if service_data.get('free_tier') else 'No'
                    
                    csv_lines.append(
                        f"{service_name},{service_data.get('sku', 'N/A')},{service_data.get('region', 'N/A')},"
                        f"{hourly},{monthly},{annual},{free_tier}"
                    )
        
        # Add regional comparison data
        if 'regional_comparison' in pricing_data:
            csv_lines.extend([
                "",
                "## Regional Comparison",
                "Region,Average_Hourly_Rate,Monthly_Estimate,Sample_Count"
            ])
            
            comparison = pricing_data['regional_comparison']
            for region, data in comparison.items():
                if isinstance(data, dict) and 'average_hourly_price' in data:
                    hourly = data['average_hourly_price'].replace('$', '')
                    monthly = data.get('average_monthly_cost', '').replace('$', '')
                    sample_count = data.get('sample_count', 'N/A')
                    
                    csv_lines.append(f"{region},{hourly},{monthly},{sample_count}")
        
        # Add infrastructure analysis
        if 'infrastructure' in pricing_data:
            infra = pricing_data['infrastructure']
            csv_lines.extend([
                "",
                "## Infrastructure Analysis",
                "Service,Resource_Count,Pricing_Available"
            ])
            
            if 'services_found' in infra:
                for service in infra['services_found']:
                    pricing_available = 'Yes' if service.get('pricing_available') else 'No'
                    csv_lines.append(f"{service['service']},{service['resource_count']},{pricing_available}")
        
        # Add recommendations as comments
        if include_recommendations:
            csv_lines.extend([
                "",
                "## Cost Optimization Recommendations (Comments)"
            ])
            
            recommendations = pricing_data.get('recommendations', [
                "Consider using Azure Reserved Instances for predictable workloads",
                "Implement auto-scaling to optimize resource utilization",
                "Use Azure Spot VMs for non-critical workloads"
            ])
            
            for i, rec in enumerate(recommendations, 1):
                csv_lines.append(f"# {i}. {rec}")
        
        return "\n".join(csv_lines)


def generate_pricing_report(
    pricing_data: Dict[str, Any],
    report_format: str = "markdown",
    include_recommendations: bool = True
) -> str:
    """Generate a pricing analysis report.
    
    Args:
        pricing_data: Pricing data from various sources
        report_format: Output format ('markdown' or 'csv')
        include_recommendations: Whether to include optimization recommendations
        
    Returns:
        Generated report as string
    """
    generator = AzurePricingReportGenerator()
    return generator.generate_cost_report(pricing_data, report_format, include_recommendations)
