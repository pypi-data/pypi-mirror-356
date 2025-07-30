"""Azure Pricing MCP Server implementation.

This server provides tools for analyzing Azure service costs with optimized, concise responses.
"""

import httpx
import json
import logging
import os
from mcp.server.fastmcp import Context, FastMCP
from typing import Any, Dict, List, Optional


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Environment variable configuration
class Config:
    """Configuration class for Azure Pricing MCP Server."""
    
    # Azure Service Configuration
    DEFAULT_REGION = os.getenv('DEFAULT_REGION', 'eastus')
    AZURE_PRICING_API_BASE_URL = os.getenv('AZURE_PRICING_API_BASE_URL', 'https://prices.azure.com/api/retail/prices')
    
    # Performance Configuration
    REQUEST_TIMEOUT = float(os.getenv('REQUEST_TIMEOUT', '15'))
    MAX_API_RESULTS = int(os.getenv('MAX_API_RESULTS', '10'))
    MAX_REGIONS_COMPARE = int(os.getenv('MAX_REGIONS_COMPARE', '4'))
    
    @classmethod
    def log_config(cls):
        """Log current configuration values."""
        logger.info(f"Azure Pricing MCP Server Configuration:")
        logger.info(f"  DEFAULT_REGION: {cls.DEFAULT_REGION}")
        logger.info(f"  AZURE_PRICING_API_BASE_URL: {cls.AZURE_PRICING_API_BASE_URL}")
        logger.info(f"  REQUEST_TIMEOUT: {cls.REQUEST_TIMEOUT}s")
        logger.info(f"  MAX_API_RESULTS: {cls.MAX_API_RESULTS}")
        logger.info(f"  MAX_REGIONS_COMPARE: {cls.MAX_REGIONS_COMPARE}")


# Log configuration on startup
Config.log_config()


mcp = FastMCP(
    name='p6plab.azure-pricing-mcp-server',
    instructions="""Use this server for analyzing Azure service costs with concise responses.

    WORKFLOW:
    1. Use get_pricing_api() to fetch Azure pricing data from the Retail Prices API
    2. Use compare_regions() to compare pricing across different Azure regions
    3. Use get_pricing_summary() for concise pricing overviews
    4. Use generate_report() to create comprehensive cost analysis reports
    
    All responses are optimized to minimize token usage while providing essential information.
    """,
)


@mcp.tool(
    name='get_pricing_api',
    description='Get concise Azure pricing information from the Retail Prices API.',
)
async def get_azure_pricing_from_api(
    service_name: Optional[str] = None,
    region: Optional[str] = None,
    product_name: Optional[str] = None,
    sku_name: Optional[str] = None,
    currency: Optional[str] = None,
    limit: Optional[int] = None,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """Get Azure pricing information with concise response."""
    
    try:
        # Use environment variables for defaults
        currency = currency or "USD"  # Hard-coded default currency
        region = region or Config.DEFAULT_REGION
        limit = limit or Config.MAX_API_RESULTS
        
        # Build API URL using configured base URL
        base_url = Config.AZURE_PRICING_API_BASE_URL
        params = {
            "currencyCode": currency,
            "$top": min(limit, Config.MAX_API_RESULTS)  # Respect max limit from config
        }
        
        # Build filter conditions
        filters = []
        if service_name:
            filters.append(f"serviceName eq '{service_name}'")
        if region:
            filters.append(f"armRegionName eq '{region}'")
        if product_name:
            filters.append(f"contains(productName, '{product_name}')")
        if sku_name:
            filters.append(f"contains(skuName, '{sku_name}')")
        
        if filters:
            params["$filter"] = " and ".join(filters)
        
        # Make API request with configured timeout
        async with httpx.AsyncClient(timeout=Config.REQUEST_TIMEOUT) as client:
            response = await client.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
        
        # Format response - CONCISE VERSION
        items = data.get('Items', [])
        if not items:
            return {
                'status': 'success',
                'summary': f'No pricing found for {service_name or "service"} in {region or "any region"}',
                'count': 0
            }
        
        # Calculate price range
        prices = [item.get('unitPrice', 0) for item in items if item.get('unitPrice', 0) > 0]
        
        # Create concise summary
        result = {
            'status': 'success',
            'service': service_name or 'Multiple services',
            'region': region or 'Multiple regions',
            'currency': currency,
            'price_range': {
                'min': f"{min(prices):.4f}" if prices else "0",
                'max': f"{max(prices):.4f}" if prices else "0",
                'avg': f"{sum(prices)/len(prices):.4f}" if prices else "0"
            },
            'sample_skus': [
                {
                    'name': item.get('skuName', 'N/A')[:50],  # Truncate long names
                    'price': f"{item.get('unitPrice', 0):.4f}",
                    'unit': item.get('unitOfMeasure', 'N/A')[:20]
                }
                for item in items[:3]  # Only top 3
            ],
            'total_found': len(items)
        }
        
        return result
        
    except Exception as e:
        return {
            'status': 'error',
            'error': f"Failed to fetch pricing: {str(e)[:100]}",  # Truncate error
            'service': service_name,
            'region': region
        }


@mcp.tool(
    name='compare_regions',
    description='Compare Azure pricing across regions with concise output.',
)
async def compare_regional_pricing(
    service_name: str,
    regions: List[str],
    product_name: Optional[str] = None,
    sku_name: Optional[str] = None,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """Compare Azure pricing across regions - optimized for low token usage."""
    
    try:
        regional_data = {}
        
        # Limit regions based on configuration
        max_regions = Config.MAX_REGIONS_COMPARE
        limited_regions = regions[:max_regions]
        
        for region in limited_regions:
            pricing_data = await get_azure_pricing_from_api(
                service_name=service_name,
                region=region,
                product_name=product_name,
                sku_name=sku_name,
                currency=None,  # Let function use its own default
                limit=3  # Reduced limit for comparison
            )
            
            if pricing_data['status'] == 'success' and 'price_range' in pricing_data:
                regional_data[region] = {
                    'avg_price': pricing_data['price_range']['avg'],
                    'min_price': pricing_data['price_range']['min'],
                    'currency': pricing_data['currency'],
                    'sku_count': pricing_data['total_found']
                }
            else:
                regional_data[region] = {
                    'avg_price': '0',
                    'min_price': '0',
                    'currency': 'USD',  # Hard-coded default
                    'sku_count': 0
                }
        
        # Find cheapest region
        valid_regions = {k: v for k, v in regional_data.items() 
                        if float(v['avg_price']) > 0}
        
        cheapest = min(valid_regions.keys(), 
                      key=lambda x: float(valid_regions[x]['avg_price'])) if valid_regions else None
        
        result = {
            'status': 'success',
            'service': service_name,
            'comparison': regional_data,
            'cheapest_region': cheapest,
            'regions_compared': len(limited_regions)
        }
        
        # Add warning if regions were limited
        if len(regions) > max_regions:
            result['note'] = f"Limited to {max_regions} regions (MAX_REGIONS_COMPARE={max_regions})"
        
        return result
        
    except Exception as e:
        return {
            'status': 'error',
            'error': f"Comparison failed: {str(e)[:100]}",
            'service': service_name
        }


@mcp.tool(
    name='get_pricing_summary',
    description='Get ultra-concise Azure pricing summary.',
)
async def get_azure_pricing_summary(
    service_name: str,
    region: Optional[str] = None,
    sku_filter: Optional[str] = None,
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """Get ultra-concise pricing summary."""
    
    try:
        # Use configured defaults
        region = region or Config.DEFAULT_REGION
        
        pricing_data = await get_azure_pricing_from_api(
            service_name=service_name,
            region=region,
            sku_name=sku_filter,
            currency=None,  # Let function use its own default
            limit=3  # Very limited
        )
        
        if pricing_data['status'] != 'success':
            return pricing_data
        
        if 'price_range' not in pricing_data:
            return {
                'status': 'success',
                'service': service_name,
                'region': region,
                'message': 'No pricing data available'
            }
        
        return {
            'status': 'success',
            'service': service_name,
            'region': region,
            'pricing': {
                'range': f"{pricing_data['price_range']['min']} - {pricing_data['price_range']['max']} {pricing_data['currency']}",
                'average': f"{pricing_data['price_range']['avg']} {pricing_data['currency']}"
            },
            'skus_found': pricing_data['total_found']
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'error': f"Summary failed: {str(e)[:50]}",
            'service': service_name
        }


@mcp.tool(
    name='generate_report',
    description='Generate concise Azure cost analysis report.',
)
async def generate_cost_report(
    pricing_data: Dict[str, Any],
    report_format: str = "summary",  # Changed default to summary
    include_recommendations: bool = False,  # Disabled by default
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """Generate concise cost analysis report."""
    
    try:
        services = pricing_data.get('services', {})
        
        if report_format.lower() == "summary":
            # Ultra-concise summary format
            report_content = f"# Azure Cost Summary\n\n"
            report_content += f"**Services Analyzed**: {len(services)}\n"
            
            for service_name, service_data in list(services.items())[:5]:  # Limit to 5 services
                pricing = service_data.get('pricing', {})
                report_content += f"- **{service_name}**: {pricing.get('monthly', 'N/A')}\n"
            
            if include_recommendations:
                report_content += f"\n**Key Recommendations**:\n"
                report_content += f"- Review resource sizing\n"
                report_content += f"- Consider reserved capacity\n"
                report_content += f"- Optimize regional placement\n"
        
        else:
            # CSV format - minimal
            report_content = "Service,Monthly Cost\n"
            for service_name, service_data in list(services.items())[:10]:
                pricing = service_data.get('pricing', {})
                report_content += f"{service_name},{pricing.get('monthly', 'N/A')}\n"
        
        return {
            'status': 'success',
            'report': report_content,
            'format': report_format,
            'services_count': len(services)
        }
        
    except Exception as e:
        return {
            'status': 'error',
            'error': f"Report generation failed: {str(e)[:50]}"
        }


@mcp.tool(
    name='get_server_config',
    description='Get current server configuration settings.',
)
async def get_server_config(
    ctx: Optional[Context] = None
) -> Dict[str, Any]:
    """Get current server configuration for debugging."""
    
    return {
        'status': 'success',
        'configuration': {
            'DEFAULT_REGION': Config.DEFAULT_REGION,
            'AZURE_PRICING_API_BASE_URL': Config.AZURE_PRICING_API_BASE_URL,
            'REQUEST_TIMEOUT': Config.REQUEST_TIMEOUT,
            'MAX_API_RESULTS': Config.MAX_API_RESULTS,
            'MAX_REGIONS_COMPARE': Config.MAX_REGIONS_COMPARE
        },
        'environment_variables': {
            'DEFAULT_REGION': os.getenv('DEFAULT_REGION', 'Not set'),
            'REQUEST_TIMEOUT': os.getenv('REQUEST_TIMEOUT', 'Not set'),
            'MAX_API_RESULTS': os.getenv('MAX_API_RESULTS', 'Not set'),
            'MAX_REGIONS_COMPARE': os.getenv('MAX_REGIONS_COMPARE', 'Not set')
        }
    }


def main():
    """Main entry point for the MCP server."""
    logger.info("Starting Azure Pricing MCP Server")
    mcp.run()


if __name__ == '__main__':
    main()
