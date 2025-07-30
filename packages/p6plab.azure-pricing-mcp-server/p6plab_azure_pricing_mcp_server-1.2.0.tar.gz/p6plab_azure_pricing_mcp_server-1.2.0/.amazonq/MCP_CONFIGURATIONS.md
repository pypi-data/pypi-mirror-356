# Azure Pricing MCP Server - Configuration Examples

This document explains the different MCP server configurations available in `mcp-logging.json`.

## Available Configurations

### 1. `azure-pricing-mcp-server-debug` 🔍
**Purpose**: Development and debugging with comprehensive logging

```json
{
  "command": "uvx",
  "args": ["8p-inc.azure-pricing-mcp-server@latest"],
  "env": {
    "MCP_DEBUG_LOGGING": "true",
    "MCP_LOG_LEVEL": "DEBUG", 
    "MCP_LOG_FORMAT": "json",
    "MCP_LOG_FILE": "./logs/azure-pricing-mcp-debug.log"
  },
  "timeout": 120000
}
```

**Features**:
- ✅ Logs all requests, responses, and internal processes
- ✅ Structured JSON format for analysis
- ✅ File logging with rotation
- ✅ Extended timeout for debugging
- ✅ Full stack traces for errors
- ✅ Uses `uvx` for automatic package management

**Use Cases**:
- Developing new features
- Debugging API issues
- Performance analysis
- Understanding data flow

---

### 2. `azure-pricing-mcp-server-production` 🚀
**Purpose**: Production deployment with balanced logging

```json
{
  "command": "uvx",
  "args": ["8p-inc.azure-pricing-mcp-server@latest"],
  "env": {
    "MCP_DEBUG_LOGGING": "false",
    "MCP_LOG_LEVEL": "INFO",
    "MCP_LOG_FORMAT": "json", 
    "MCP_LOG_FILE": "./logs/azure-pricing-mcp-production.log"
  },
  "timeout": 60000
}
```

**Features**:
- ✅ Essential logging without debug overhead
- ✅ Structured JSON for log analysis tools
- ✅ File logging for audit trails
- ✅ Standard timeout values
- ✅ Error tracking without verbose details
- ✅ Automatic package updates with `uvx`

**Use Cases**:
- Production environments
- Monitoring and alerting
- Performance optimization
- Audit compliance

---

### 3. `azure-pricing-mcp-server-troubleshoot` 🛠️
**Purpose**: Intensive troubleshooting with human-readable logs

```json
{
  "command": "uvx",
  "args": ["8p-inc.azure-pricing-mcp-server@latest"],
  "env": {
    "MCP_DEBUG_LOGGING": "true",
    "MCP_LOG_LEVEL": "DEBUG",
    "MCP_LOG_FORMAT": "plain",
    "MCP_LOG_FILE": "./logs/azure-pricing-mcp-troubleshoot.log"
  },
  "timeout": 180000
}
```

**Features**:
- ✅ Maximum logging detail
- ✅ Human-readable plain text format
- ✅ Extended timeout for complex operations
- ✅ Additional Azure API configuration
- ✅ Custom cache and request settings
- ✅ Latest package version via `uvx`

**Use Cases**:
- Investigating specific issues
- Customer support scenarios
- API connectivity problems
- Performance bottlenecks

---

### 4. `azure-pricing-mcp-server-console-only` 💻
**Purpose**: Development with console-only output

```json
{
  "command": "uvx",
  "args": ["8p-inc.azure-pricing-mcp-server@latest"],
  "env": {
    "MCP_DEBUG_LOGGING": "false",
    "MCP_LOG_LEVEL": "INFO",
    "MCP_LOG_FORMAT": "plain",
    "DEFAULT_CURRENCY": "EUR",
    "DEFAULT_REGION": "westeurope"
  }
}
```

**Features**:
- ✅ Console output only (no file logging)
- ✅ Human-readable format
- ✅ European defaults (EUR, West Europe)
- ✅ Minimal performance impact
- ✅ Quick startup and testing
- ✅ Always latest version with `uvx`

**Use Cases**:
- Local development
- Quick testing
- European region focus
- Minimal resource usage

---

### 5. `azure-pricing-mcp-server-minimal` ⚡
**Purpose**: Minimal logging for high-performance scenarios

```json
{
  "command": "uvx",
  "args": ["8p-inc.azure-pricing-mcp-server@latest"],
  "env": {
    "MCP_DEBUG_LOGGING": "false",
    "MCP_LOG_LEVEL": "WARNING",
    "MCP_LOG_FORMAT": "json",
    "MCP_LOG_FILE": "./logs/azure-pricing-mcp-minimal.log"
  },
  "timeout": 30000
}
```

**Features**:
- ✅ Only warnings and errors logged
- ✅ Minimal performance overhead
- ✅ Short timeout for fast responses
- ✅ Essential error tracking
- ✅ Structured format for alerts
- ✅ Automatic updates via `uvx`

**Use Cases**:
- High-throughput scenarios
- Resource-constrained environments
- Error-only monitoring
- Fast response requirements

## Benefits of Using `uvx`

### 🚀 **Automatic Package Management**
- **No local installation required** - `uvx` downloads and runs the package automatically
- **Always latest version** - Uses `@latest` to get the most recent version
- **Isolated environment** - Each run uses a clean Python environment
- **No dependency conflicts** - Avoids conflicts with local Python packages

### 🔧 **Simplified Configuration**
```json
{
  "command": "uvx",
  "args": ["8p-inc.azure-pricing-mcp-server@latest"]
}
```

Instead of:
```json
{
  "command": "./tools/start_server.sh",
  "args": []
}
```

### 📦 **Version Management**
- **Specific versions**: `8p-inc.azure-pricing-mcp-server@1.0.0`
- **Latest version**: `8p-inc.azure-pricing-mcp-server@latest`
- **Development versions**: `8p-inc.azure-pricing-mcp-server@dev`

## How to Use These Configurations

### Option 1: Copy to Main Configuration
```bash
# Copy the desired configuration to your main mcp.json
cp .amazonq/mcp-logging.json .amazonq/mcp.json

# Edit to keep only the configuration you want
nano .amazonq/mcp.json
```

### Option 2: Use Specific Configuration
```bash
# Use a specific configuration by name
q chat --mcp-config .amazonq/mcp-logging.json --mcp-server azure-pricing-mcp-server-debug
```

### Option 3: Environment Override
```bash
# Override specific settings via environment variables
export MCP_DEBUG_LOGGING=true
export MCP_LOG_LEVEL=DEBUG
q chat
```

## Log File Locations

All configurations create logs in the `./logs/` directory:

```
azure-pricing-mcp-server/
├── logs/
│   ├── azure-pricing-mcp-debug.log
│   ├── azure-pricing-mcp-production.log
│   ├── azure-pricing-mcp-troubleshoot.log
│   └── azure-pricing-mcp-minimal.log
└── .amazonq/
    ├── mcp.json
    └── mcp-logging.json
```

## Monitoring Commands

### View Logs in Real-Time
```bash
# Debug logs (JSON format)
tail -f ./logs/azure-pricing-mcp-debug.log | jq '.'

# Troubleshoot logs (plain format)
tail -f ./logs/azure-pricing-mcp-troubleshoot.log

# Production logs (JSON format)
tail -f ./logs/azure-pricing-mcp-production.log | jq 'select(.level == "ERROR")'
```

### Analyze Logs
```bash
# Count requests by tool
cat ./logs/azure-pricing-mcp-debug.log | jq -r 'select(.mcp_context.tool) | .mcp_context.tool' | sort | uniq -c

# Find slow operations (>2 seconds)
cat ./logs/azure-pricing-mcp-debug.log | jq 'select(.execution_time_ms > 2000)'

# Show only errors
cat ./logs/azure-pricing-mcp-production.log | jq 'select(.level == "ERROR")'
```

## Performance Comparison

| Configuration | Startup Time | Memory Usage | Log Volume | Response Time | Package Management |
|---------------|--------------|--------------|------------|---------------|-------------------|
| Debug         | Medium       | High         | Very High  | Slower        | Automatic (uvx)   |
| Production    | Fast         | Medium       | Medium     | Normal        | Automatic (uvx)   |
| Troubleshoot  | Medium       | High         | Very High  | Slower        | Automatic (uvx)   |
| Console Only  | Very Fast    | Low          | Low        | Fast          | Automatic (uvx)   |
| Minimal       | Very Fast    | Very Low     | Very Low   | Very Fast     | Automatic (uvx)   |

## Recommendations

- **Development**: Use `debug` or `troubleshoot`
- **Testing**: Use `console-only` or `production`
- **Production**: Use `production` or `minimal`
- **Debugging Issues**: Use `troubleshoot`
- **High Performance**: Use `minimal`

## Security Notes

- Log files may contain sensitive pricing data
- Ensure proper file permissions in production
- Consider log rotation and retention policies
- Debug logs contain full request/response data
- Use minimal logging in security-sensitive environments
- `uvx` automatically manages package security updates
