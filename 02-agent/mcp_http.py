from mcp.server.fastmcp import FastMCP

# Create the MCP server
mcp = FastMCP("Demo Server")


@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b


@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b


@mcp.tool()
def greet(name: str) -> str:
    """Greet a person by name."""
    return f"Hello, {name}! Welcome to the MCP server."


@mcp.tool()
def get_weather(city: str) -> dict:
    """Get the current weather for a city (mock data)."""
    # Mock weather data for demonstration
    weather_data = {
        "New York": {"temp": 22, "condition": "Sunny", "humidity": 45},
        "London": {"temp": 15, "condition": "Cloudy", "humidity": 72},
        "Tokyo": {"temp": 28, "condition": "Partly Cloudy", "humidity": 60},
    }
    data = weather_data.get(city, {"temp": 20, "condition": "Unknown", "humidity": 50})
    return {"city": city, **data}


if __name__ == "__main__":
    # Run the server with SSE transport on port 8000
    mcp.run(transport="sse")