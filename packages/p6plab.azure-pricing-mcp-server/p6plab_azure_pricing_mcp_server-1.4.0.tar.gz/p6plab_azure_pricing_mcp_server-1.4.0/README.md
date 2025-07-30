# Azure Pricing MCP Server

A token-optimized, security-audited Model Context Protocol (MCP) server for Azure pricing analysis, developed by P6P Lab.

## 🚀 Key Features

- **Token Efficient**: Responses optimized to use minimal tokens (~60-90% reduction)
- **Concise Data**: Essential information only, no verbose details
- **Smart Limits**: Configurable API calls and data processing limits
- **Fast Responses**: Configurable timeouts and streamlined processing
- **Environment Variables**: Fully configurable via environment variables
- **🔒 Security Certified**: Comprehensive security audit passed - production ready

## 🛠️ Available Tools

- **get_pricing_api**: Fetch concise Azure pricing from Retail Prices API
- **compare_regions**: Compare pricing across Azure regions (configurable limit)
- **get_pricing_summary**: Get ultra-concise pricing summaries
- **generate_report**: Create compact cost analysis reports
- **get_server_config**: Get current server configuration (for debugging)

## 📦 Installation

### From PyPI (Recommended)
```bash
# Install from PyPI
uvx p6plab.azure-pricing-mcp-server@latest
```

### Local Development
```bash
# Build the package
uv build

# Install locally
uvx --from ./dist/p6plab_azure_pricing_mcp_server-1.4.0-py3-none-any.whl p6plab.azure-pricing-mcp-server
```

## 🚀 Usage with Amazon Q CLI

### PyPI Installation (Recommended)

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

### Local Installation (from built wheel)

Add to your `.amazonq/mcp.json`:

```json
{
  "mcpServers": {
    "azure-pricing": {
      "command": "uvx",
      "args": ["--from", "./dist/p6plab_azure_pricing_mcp_server-1.4.0-py3-none-any.whl", "p6plab.azure-pricing-mcp-server"],
      "timeout": 30000
    }
  }
}
```

### With Environment Variables

```json
{
  "mcpServers": {
    "azure-pricing": {
      "command": "uvx",
      "args": ["p6plab.azure-pricing-mcp-server@latest"],
      "timeout": 30000,
      "env": {
        "DEFAULT_REGION": "westeurope",
        "REQUEST_TIMEOUT": "30",
        "MAX_API_RESULTS": "15",
        "MAX_REGIONS_COMPARE": "6"
      }
    }
  }
}
```

## 🎯 Optimization Details

### Token Usage Reduction

| Optimization | Before | After | Savings |
|--------------|--------|-------|---------|
| API Response Limit | 50 items | 5-15 items (configurable) | ~70-85% |
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

**After**:
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

### Configurable Limits

All optimization limits are now configurable via environment variables:
- `MAX_API_RESULTS`: Control API response size (default: 10)
- `MAX_REGIONS_COMPARE`: Limit regional comparisons (default: 4)  
- `REQUEST_TIMEOUT`: Adjust for network conditions (default: 15s)

## Environment Variables

### 🌍 Azure Service Configuration

| Variable | Purpose | Values | Default |
|----------|---------|---------|---------|
| `DEFAULT_REGION` | Default Azure region | `eastus`, `westeurope`, `centralus`, etc. | `eastus` |
| `AZURE_PRICING_API_BASE_URL` | Azure Retail Prices API URL | Valid URL | `https://prices.azure.com/api/retail/prices` |

### ⚡ Performance Configuration

| Variable | Purpose | Values | Default |
|----------|---------|---------|---------|
| `REQUEST_TIMEOUT` | HTTP request timeout in seconds | `10`, `30`, `60`, etc. | `15` |
| `MAX_API_RESULTS` | Maximum results per API call | `5`, `10`, `20`, etc. | `10` |
| `MAX_REGIONS_COMPARE` | Maximum regions for comparison | `2`, `4`, `6`, etc. | `4` |

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

### Custom Azure Configuration
```json
{
  "mcpServers": {
    "azure-pricing": {
      "command": "uvx",
      "args": ["p6plab.azure-pricing-mcp-server@latest"],
      "timeout": 30000,
      "env": {
        "DEFAULT_REGION": "westeurope",
        "REQUEST_TIMEOUT": "30",
        "MAX_API_RESULTS": "15",
        "MAX_REGIONS_COMPARE": "6"
      }
    }
  }
}
```

### Performance Optimized Configuration
```json
{
  "mcpServers": {
    "azure-pricing": {
      "command": "uvx",
      "args": ["p6plab.azure-pricing-mcp-server@latest"],
      "timeout": 45000,
      "env": {
        "REQUEST_TIMEOUT": "45",
        "MAX_API_RESULTS": "20",
        "MAX_REGIONS_COMPARE": "8",
        "AZURE_PRICING_API_BASE_URL": "https://prices.azure.com/api/retail/prices"
      }
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
        "DEFAULT_REGION": "eastus",
        "REQUEST_TIMEOUT": "60",
        "MAX_API_RESULTS": "5"
      }
    }
  }
}
```

### Environment Variables Usage Examples

#### Set via Shell (for testing)
```bash
# Azure Service Configuration
export DEFAULT_REGION=westeurope
export AZURE_PRICING_API_BASE_URL=https://prices.azure.com/api/retail/prices

# Performance Configuration  
export REQUEST_TIMEOUT=30
export MAX_API_RESULTS=15
export MAX_REGIONS_COMPARE=6

# Start Q CLI
q chat
```

#### Set via MCP Configuration (recommended)
Use the JSON configuration examples above to set environment variables through the MCP server configuration.

## Implemented Environment Variables Details

### 🌍 Azure Service Configuration

- **`DEFAULT_REGION`**: Sets the default Azure region when none is specified. Use Azure region names like `eastus`, `westeurope`, `centralus`
- **`AZURE_PRICING_API_BASE_URL`**: Allows overriding the Azure Pricing API endpoint (useful for testing or alternative endpoints)

### ⚡ Performance Configuration

- **`REQUEST_TIMEOUT`**: HTTP timeout in seconds for Azure API calls. Higher values for slower connections
- **`MAX_API_RESULTS`**: Maximum number of results returned per API call. Lower values for faster responses
- **`MAX_REGIONS_COMPARE`**: Maximum number of regions that can be compared simultaneously. Prevents excessive API calls

### Configuration Validation

The server logs all configuration values on startup:
```
Azure Pricing MCP Server Configuration:
  DEFAULT_CURRENCY: EUR
  DEFAULT_REGION: westeurope  
  AZURE_PRICING_API_BASE_URL: https://prices.azure.com/api/retail/prices
  REQUEST_TIMEOUT: 30.0s
  MAX_API_RESULTS: 15
  MAX_REGIONS_COMPARE: 6
```

## Example Queries

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

## 🚀 Performance Tips

1. **Use Specific Queries**: Target specific services rather than broad searches
2. **Configure Limits**: Adjust `MAX_REGIONS_COMPARE` and `MAX_API_RESULTS` based on your needs
3. **Optimize Timeout**: Set `REQUEST_TIMEOUT` based on your network conditions
4. **Use Summary Tools**: Prefer `get_pricing_summary` over `get_pricing_api` for quick overviews
5. **Fresh Sessions**: Start new chat sessions for complex analyses
6. **Regional Defaults**: Set `DEFAULT_REGION` to your primary region to avoid specifying it repeatedly

### Performance Configuration Examples

**Fast & Minimal** (for quick queries):
```json
"env": {
  "MAX_API_RESULTS": "5",
  "MAX_REGIONS_COMPARE": "2", 
  "REQUEST_TIMEOUT": "10"
}
```

**Comprehensive** (for detailed analysis):
```json
"env": {
  "MAX_API_RESULTS": "20",
  "MAX_REGIONS_COMPARE": "8",
  "REQUEST_TIMEOUT": "45"
}
```

## 🔧 Troubleshooting

### Common Issues

#### 1. "No pricing found" responses
- **Cause**: Service names in Azure API may differ from display names
- **Solution**: Try variations like "Virtual Machines" vs "Compute" vs "Microsoft.Compute"
- **Alternative**: Use product name filtering instead of service name

#### 2. Timeout errors
- **Cause**: Network latency or Azure API slowness
- **Solution**: Increase `REQUEST_TIMEOUT` environment variable
```json
"env": {
  "REQUEST_TIMEOUT": "60"
}
```

#### 3. Empty results for specific regions
- **Cause**: Service may not be available in that region
- **Solution**: Try common regions like `eastus`, `westeurope`, `centralus`

#### 4. MCP server not loading
- **Check**: Verify the server is listed in `q mcp list`
- **Check**: Verify the server status with `q mcp status --name azure-pricing`
- **Solution**: Ensure package is installed: `uvx p6plab.azure-pricing-mcp-server@latest --help`

### Debugging Tools

#### Check Current Configuration
Use the built-in debugging tool to verify your environment variables are working:

**Query**: "Show me the current server configuration"

This will return:
```json
{
  "status": "success",
  "configuration": {
    "DEFAULT_REGION": "eastus",
    "REQUEST_TIMEOUT": 15.0,
    "MAX_API_RESULTS": 10,
    "MAX_REGIONS_COMPARE": 4
  },
  "environment_variables": {
    "DEFAULT_REGION": "Not set",
    "REQUEST_TIMEOUT": "Not set"
  }
}
```

### Debug Configuration

Enable verbose logging to troubleshoot issues:

```json
{
  "mcpServers": {
    "azure-pricing": {
      "command": "uvx",
      "args": ["p6plab.azure-pricing-mcp-server@latest"],
      "timeout": 60000,
      "env": {
        "REQUEST_TIMEOUT": "60",
        "MAX_API_RESULTS": "5"
      }
    }
  }
}
```

### Verify Configuration

The server logs all configuration on startup. Check the logs to verify your environment variables are being applied:

```
Azure Pricing MCP Server Configuration:
  DEFAULT_CURRENCY: EUR
  DEFAULT_REGION: westeurope
  AZURE_PRICING_API_BASE_URL: https://prices.azure.com/api/retail/prices
  REQUEST_TIMEOUT: 30.0s
  MAX_API_RESULTS: 15
  MAX_REGIONS_COMPARE: 6
```

## 🔒 Security

### Security Audit Status: ✅ **PASSED**

The Azure Pricing MCP Server has undergone comprehensive security analysis:

- **✅ No Medium or High Risk Vulnerabilities**: Comprehensive scan completed
- **✅ Production Ready**: Approved for production deployment
- **✅ Secure Dependencies**: All dependencies are well-maintained and secure
- **✅ Limited Attack Surface**: Read-only operations to public Azure API only
- **✅ No Sensitive Data**: No hardcoded secrets, credentials, or API keys
- **✅ Proper Error Handling**: Secure error messages without information disclosure

### Security Features

- **HTTPS Only**: All API communications use secure HTTPS
- **Input Validation**: Proper type checking and parameter validation
- **Timeout Protection**: Configurable timeouts prevent hanging requests
- **No File Operations**: No file system access or manipulation
- **No Command Execution**: No subprocess or system calls
- **Environment Variable Configuration**: Secure configuration management

For detailed security analysis, see the [Security Audit Report](SECURITY.md).

## 📋 Version History

- **v1.4.0**: Security audit and production readiness certification
- **v1.3.0**: Environment variables implementation for Azure Service and Performance Configuration
- **v1.2.0**: Major optimization for token efficiency  
- **v1.1.0**: P6P Lab branding and improvements
- **v1.0.0**: Initial release

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🏷️ Keywords

Azure, Pricing, MCP, Model Context Protocol, Cost Analysis, Cloud Computing, P6P Lab, Security Certified, Production Ready
