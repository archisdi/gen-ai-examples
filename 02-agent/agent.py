import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# 1. Define how to start the server we wrote earlier
server_params = StdioServerParameters(
    command="python",
    args=["mcp_log_server.py"], # The file we created in the last step
)

async def run_agent_workflow():
    # 2. Start the server process and establish the STDIO pipe
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            
            # --- REGISTRATION / DISCOVERY ---
            # This triggers the 'initialize' and gets the tools list
            await session.initialize()
            tools = await session.list_tools()
            print(f"Discovered Tools: {[t.name for t in tools.tools]}")

            # --- INVOCATION ---
            # Imagine the LLM decided to call this tool
            print("\nInvoking fetch_detailed_logs...")
            result = await session.call_tool(
                "fetch_detailed_logs", 
                arguments={"service_name": "api-service"}
            )
            
            # This 'result' is now the "Grounded" data for the AI
            print(f"Result from OpenSearch: {result.content[0].text}")

if __name__ == "__main__":
    asyncio.run(run_agent_workflow())