# Azure Pricing MCP Server (Optimized)

A token-optimized Model Context Protocol (MCP) server for Azure pricing analysis, developed by P6P Lab.

## 🚀 Optimization Features

- **Token Efficient**: Responses optimized to use minimal tokens
- **Concise Data**: Essential information only, no verbose details
- **Smart Limits**: Reduced API calls and data processing
- **Fast Responses**: Shorter timeouts and streamlined processing

## Features

- **get_pricing_api**: Fetch concise Azure pricing from Retail Prices API
- **compare_regions**: Compare pricing across Azure regions (up to 4 regions)
- **get_pricing_summary**: Get ultra-concise pricing summaries
- **generate_report**: Create compact cost analysis reports

## Installation

```bash
# Build the package
uv build

# Install locally
uvx --from ./dist/p6plab_azure_pricing_mcp_server-1.2.0-py3-none-any.whl p6plab.azure-pricing-mcp-server
```

## Usage with Amazon Q CLI

### Local Installation (from built wheel)

Add to your `.amazonq/mcp.json`:

```json
{
  "mcpServers": {
    "azure-pricing": {
      "command": "uvx",
      "args": ["--from", "./dist/p6plab_azure_pricing_mcp_server-1.2.0-py3-none-any.whl", "p6plab.azure-pricing-mcp-server"],
      "timeout": 30000
    }
  }
}
```

### PyPI Installation (from published package)

Add to your `.amazonq/mcp.json`:

```json
{
  "mcpServers": {
    "azure-pricing": {
      "command": "uvx",
      "args": ["p6plab.azure-pricing-mcp-server@latest"],
      "timeout": 30000
    }
  }
}
```

## Optimization Details

### Token Usage Reduction

| Optimization | Before | After | Savings |
|--------------|--------|-------|---------|
| API Response Limit | 50 items | 5-10 items | ~80% |
| Sample SKUs | 3 full objects | 3 truncated objects | ~60% |
| Error Messages | Full stack traces | Truncated (100 chars) | ~90% |
| Regional Comparison | Full data per region | Summary stats only | ~75% |
| Report Generation | Verbose markdown | Concise summary | ~70% |

### Response Structure Changes

**Before (Verbose)**:
```json
{
  "status": "success",
  "data": {
    "items": [
      {
        "service_name": "Very Long Service Name Here",
        "product_name": "Very Long Product Name Here",
        "sku_name": "Very Long SKU Name Here",
        "region": "eastus",
        "unit_price": 0.0688,
        "currency": "USD",
        "unit_of_measure": "1 Hour",
        "type": "Consumption",
        "tier_minimum_units": 0
      }
      // ... many more items
    ],
    "count": 50,
    "currency": "USD",
    "filters_applied": { /* ... */ }
  }
}
```

**After (Optimized)**:
```json
{
  "status": "success",
  "service": "Virtual Machines",
  "region": "eastus",
  "currency": "USD",
  "price_range": {
    "min": "0.0068",
    "max": "2.4160",
    "avg": "0.3420"
  },
  "sample_skus": [
    {
      "name": "Standard_B1s",
      "price": "0.0068",
      "unit": "1 Hour"
    }
  ],
  "total_found": 15
}
```

## Environment Variables

### 🔧 MCP Framework Configuration

| Variable | Purpose | Values | Default |
|----------|---------|---------|---------|
| `MCP_DEBUG_LOGGING` | Enable/disable debug logging | `true`, `false` | `false` |
| `MCP_LOG_LEVEL` | Set logging level | `DEBUG`, `INFO`, `WARNING`, `ERROR` | `INFO` |
| `MCP_LOG_FORMAT` | Log output format | `json`, `plain` | `json` |
| `MCP_LOG_FILE` | Log file path | File path | None (console only) |
| `FASTMCP_LOG_LEVEL` | FastMCP framework log level | `DEBUG`, `INFO`, `WARNING`, `ERROR` | `INFO` |

### 🌍 Azure Service Configuration

| Variable | Purpose | Values | Default |
|----------|---------|---------|---------|
| `DEFAULT_CURRENCY` | Default currency for pricing | `USD`, `EUR`, etc. | `USD` |
| `DEFAULT_REGION` | Default Azure region | `eastus`, `westeurope`, etc. | `eastus` |
| `AZURE_PRICING_API_BASE_URL` | Azure Retail Prices API URL | URL | `https://prices.azure.com/api/retail/prices` |

### ⚡ Performance Configuration

| Variable | Purpose | Values | Default |
|----------|---------|---------|---------|
| `CACHE_TTL_SECONDS` | Cache time-to-live in seconds | `300`, `1800`, etc. | Not implemented |
| `REQUEST_TIMEOUT` | HTTP request timeout in seconds | `30`, `45`, etc. | `15` (optimized) |

### 🐍 Python Configuration

| Variable | Purpose | Values | Default |
|----------|---------|---------|---------|
| `PYTHONUNBUFFERED` | Disable Python output buffering | `1` | Not set |

## Configuration Examples

### Minimal Configuration (Recommended)
```json
{
  "mcpServers": {
    "azure-pricing": {
      "command": "uvx",
      "args": ["p6plab.azure-pricing-mcp-server@latest"],
      "timeout": 30000
    }
  }
}
```

### Debug Configuration
```json
{
  "mcpServers": {
    "azure-pricing": {
      "command": "uvx",
      "args": ["p6plab.azure-pricing-mcp-server@latest"],
      "timeout": 60000,
      "env": {
        "MCP_LOG_LEVEL": "DEBUG",
        "MCP_LOG_FORMAT": "plain"
      }
    }
  }
}
```

## Example Queries (Optimized)

### Basic Pricing Queries
- "Get Azure Virtual Machines pricing summary for East US"
- "What's the price range for Azure Functions in West Europe?"
- "Show me Azure SQL Database pricing for eastus region"
- "Get Azure Storage pricing summary"
- "What are the costs for Azure App Service in Central US?"

### Regional Comparison Queries
- "Compare Azure Storage costs between eastus and westeurope"
- "Compare Virtual Machines pricing across eastus, westus, and centralus"
- "Which region is cheapest for Azure Functions?"
- "Compare Azure SQL Database costs between North Europe and West Europe"
- "Show pricing differences for Azure Container Instances across 3 regions"

### Service-Specific Queries
- "Get pricing for Standard_B2s virtual machine instances"
- "What's the cost of Azure Blob Storage hot tier?"
- "Show me Azure Kubernetes Service pricing details"
- "Get Azure Cosmos DB pricing for SQL API"
- "What are the rates for Azure Application Gateway?"

### SKU and Product Filtering
- "Find pricing for Standard tier Azure App Service plans"
- "Get costs for Premium SSD managed disks"
- "Show me pricing for General Purpose v2 storage accounts"
- "What's the cost of Standard Load Balancer?"
- "Get pricing for Basic tier Azure Database for MySQL"

### Cost Analysis and Reporting
- "Generate a cost summary report for Azure compute services"
- "Create a pricing comparison report for storage services"
- "Show me a cost analysis for serverless services"
- "Generate pricing report for database services in East US"

### Multi-Service Queries
- "Compare costs of Azure Functions vs App Service for small workloads"
- "What's cheaper: Azure SQL Database or MySQL for basic usage?"
- "Show pricing for a typical web application stack in Azure"
- "Compare container hosting options: ACI vs AKS vs App Service"

### Budget Planning Queries
- "What's the monthly cost estimate for a Standard_D2s_v3 VM running 24/7?"
- "Show me the most cost-effective storage options for archival data"
- "What are the cheapest compute options for development environments?"
- "Find the most economical database solution for small applications"

### Advanced Filtering Examples
- "Get pricing for all compute services in East US under $0.10 per hour"
- "Show me storage services with pay-as-you-go pricing model"
- "Find all database services available in West Europe region"
- "Get pricing for services with 'Standard' in the SKU name"

## Performance Tips

1. **Use Specific Queries**: Target specific services rather than broad searches
2. **Limit Regions**: Compare max 4 regions at once
3. **Use Summary Tools**: Prefer `get_pricing_summary` over `get_pricing_api`
4. **Fresh Sessions**: Start new chat sessions for complex analyses

## Version History

- **v1.2.0**: Major optimization for token efficiency
- **v1.1.0**: P6P Lab branding and improvements  
- **v1.0.0**: Initial release
