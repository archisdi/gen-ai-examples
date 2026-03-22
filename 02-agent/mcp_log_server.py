from mcp.server.fastmcp import FastMCP
import httpx

# Initialize the MCP server
mcp = FastMCP("LogInvestigator")

# 1. Define a Resource (Reading context)
@mcp.resource("opensearch://error-logs/summary")
def get_error_summary() -> str:
    """Returns a high-level summary of the last 10 errors in OpenSearch."""
    # In a real app, you'd call the OpenSearch API here
    return "Found 3 'Connection Timeout' errors and 7 '500 Internal Server Error' in 'api-service'."

# 2. Define a Tool (Taking action)
@mcp.tool()
async def fetch_detailed_logs(service_name: str, limit: int = 5) -> str:
    """Fetches the latest detailed logs for a specific service from OpenSearch."""
    print(f"--- Agent is calling fetch_detailed_logs for {service_name} ---")
    
    # Mocking a call to your OpenSearch stack
    return f"LOGS for {service_name}: [14:02:01] ERROR: Database connection failed at 10.0.0.5."

# Start the server using the STDIO transport (standard for local agents)
if __name__ == "__main__":
    mcp.run()