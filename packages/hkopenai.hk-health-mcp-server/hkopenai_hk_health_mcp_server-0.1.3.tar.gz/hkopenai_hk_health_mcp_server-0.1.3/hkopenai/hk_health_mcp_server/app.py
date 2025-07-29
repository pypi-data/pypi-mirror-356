import argparse
from fastmcp import FastMCP
from hkopenai.hk_health_mcp_server import tool_aed_waiting, tool_specialist_waiting_time_by_cluster
from typing import Dict, Annotated, Optional
from pydantic import Field

def create_mcp_server():
    """Create and configure the MCP server"""
    mcp = FastMCP(name="HK OpenAI Health Server")

    @mcp.tool(
        description="Get current Accident and Emergency Department waiting times by hospital in Hong Kong"
    )
    def get_aed_waiting_times(
        lang: Annotated[Optional[str], Field(description="Language (en/tc/sc) English, Traditional Chinese, Simplified Chinese. Default English", enum=["en", "tc", "sc"])] = 'en'
    ) -> Dict:
        return tool_aed_waiting.get_aed_waiting_times(lang)

    @mcp.tool(
        description="Get current waiting times for new case bookings for specialist outpatient services by specialty and cluster in Hong Kong"
    )
    def get_specialist_waiting_times(
        lang: Annotated[Optional[str], Field(description="Language (en/tc/sc) English, Traditional Chinese, Simplified Chinese. Default English", enum=["en", "tc", "sc"])] = 'en'
    ) -> Dict:
        return tool_specialist_waiting_time_by_cluster.get_specialist_waiting_times(lang)

    return mcp
def main():
    parser = argparse.ArgumentParser(description='HKO MCP Server')
    parser.add_argument('-s', '--sse', action='store_true',
                       help='Run in SSE mode instead of stdio')
    args = parser.parse_args()

    server = create_mcp_server()
    
    if args.sse:
        server.run(transport="streamable-http")
        print("HKO MCP Server running in SSE mode on port 8000")
    else:
        server.run()
        print("HKO MCP Server running in stdio mode")

if __name__ == "__main__":
    main()
