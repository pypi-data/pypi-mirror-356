# Hong Kong Health Data MCP Server

[![GitHub Repository](https://img.shields.io/badge/GitHub-Repository-blue.svg)](https://github.com/hkopenai/hk-health-mcp-server)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This is an MCP server that provides access to health related data in Hong Kong through a FastMCP interface.

## Features

1. Get current Accident and Emergency Department waiting times by hospital in Hong Kong
2. Get current waiting times for new case bookings for specialist outpatient services by specialty and cluster in Hong Kong


## Examples

* As a news reporter, you are interested in knowing the current waiting times at hospitals in Hong Kong. Please remind the audience not to abuse the service. Report in Chinese.
* As a healthcare professional, you need to check the current waiting times for specialist outpatient services in different clusters to advise patients on the best options for timely care.

## Data Source

* Hong Kong Hospital Authority

## Setup

1. Clone this repository
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   python app.py
   ```

### Running Options

- Default stdio mode: `python app.py`
- SSE mode (port 8000): `python app.py --sse`

## Cline Integration

To connect this MCP server to Cline using stdio:

1. Add this configuration to your Cline MCP settings (cline_mcp_settings.json):
```json
{
  "hk-health": {
    "disabled": false,
    "timeout": 3,
    "type": "stdio",
    "command": "uvx",
    "args": [
      "hkopenai.hk-health-mcp-server"
    ]
  }
}
```

## Testing

Tests are available in the `tests/` directory. Run with:
```bash
pytest
```
