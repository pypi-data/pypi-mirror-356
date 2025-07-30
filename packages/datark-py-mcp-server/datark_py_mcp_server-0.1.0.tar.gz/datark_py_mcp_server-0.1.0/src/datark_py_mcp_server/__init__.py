
import mcp
from mcp.server.fastmcp import FastMCP


mcp = FastMCP("WeatherServer")

async def fetch_weather(city: str) -> dict[str, str]:
    return {city: '下雨'}


@mcp.tool()
async def query_weather(city: str) -> dict[str, str]:
    """
    输入指定城市的中文名称，返回今日的天气查询结果
    :param city: 城市名称(需要使用中文名字)
    :return: 格式化后的天气
    """
    return await fetch_weather(city)

def main() -> None:
    # 以标准IO方式运行MCP服务器
    mcp.run(transport='stdio')