from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="hello_mcp", stateless_http=True)


@mcp.tool()
# search anything online
def search_online(query:str) ->str:
    return f"results for {query}"

@mcp.tool()
async def get_weather(city:str) ->str:
    return f"weather for {city}" 

mcp_app = mcp.streamable_http_app() 

