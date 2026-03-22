from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama

# Initialize the LLM using local Ollama
llm = ChatOllama(model="qwen3:8b", base_url="http://localhost:11434")


async def main():
    # Connect to the MCP server via SSE
    client = MultiServerMCPClient(
        {
            "demo_server": {
                "url": "http://localhost:8000/sse",
                "transport": "sse",
            }
        }
    )

    # Get tools exposed by the MCP server
    tools = await client.get_tools()
    print(f"Discovered {len(tools)} tools: {[t.name for t in tools]}\n")

    # Create a ReAct agent
    agent = create_react_agent(llm, tools)

    # Example queries
    queries = [
        "What's 42 + 58?",
        "Multiply 7 by 13",
        "Greet Alice",
        "What's the weather in Tokyo?",
    ]

    for query in queries:
        print(f"Q: {query}")
        result = await agent.ainvoke(
            {"messages": [{"role": "user", "content": query}]}
        )
        print(f"A: {result['messages'][-1].content}\n")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())