import random
from fastmcp import FastMCP

# create an instance of FastMCP
mcp = FastMCP(name="Demo Server")

@mcp.tool
def roll_dice(n_dice: int = 1 ) -> list[int]:
    """Rolls a n_dice 6 sided dice and returns the results."""
    return [random.randint(1, 6) for _ in range(n_dice)]

@mcp.tool
def add_numbers(a: int, b: int) -> int:
    """Adds two numbers and returns the result."""
    return a + b

if __name__ == "__main__":
    # run the FastMCP server
    mcp.run() 