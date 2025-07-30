## Steps to Publish:

### 1. Get TestPyPI Credentials
- Go to https://test.pypi.org/account/register/ (create account if needed)
- Go to https://test.pypi.org/manage/account/token/
- Create a new API token with scope "Entire account"
- Copy the token (starts with pypi-)

### 2. Publish using one of these methods:

Method A: Environment Variable
``` bash
cd ./mcp-azure-pricing/azure-pricing-mcp-server
export UV_PUBLISH_TOKEN="pypi-your-token-here"
uv publish --publish-url https://test.pypi.org/legacy/
```

Method B: Command Line
``` bash
cd ./mcp-azure-pricing/azure-pricing-mcp-server
uv publish --publish-url https://test.pypi.org/legacy/ --token "pypi-your-token-here"
```

### 3. After successful upload, you can test install:
``` bash
# Test installation from TestPyPI
uvx --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ p6plab.azure-pricing-mcp-server@latest
```

### 4. Update your MCP configuration to use TestPyPI version:
``` json
{
  "mcpServers": {
    "azure-pricing": {
      "command": "uvx",
      "args": ["--index-url", "https://test.pypi.org/simple/", "--extra-index-url", "https://pypi.org/simple/", "p6plab.azure-pricing-mcp-server@latest"],
      "timeout": 30000
    }
  }
}
```