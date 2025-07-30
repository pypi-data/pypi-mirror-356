import json
import httpx
import argparse
from typing import Any
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather-Server")

@mcp.tool()
async def get_weather(city: str) -> dict[str,Any] | None:
    """
    输入指定的城市名称,返回城市的温度信息。
    """
    import random
    tmp = int(random.random()*50)
    res = f"{city}的温度是:{tmp}"
    return res

def main():
    mcp.run(transport="sse")

if __name__ == "__main__":
    main()
