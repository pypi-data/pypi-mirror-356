from mcp.server.fastmcp import FastMCP
# from city_01_service import CityDataServer
# 初始化 MCP 服务器@mcp.tool()
async def get_city_weather(city: str) -> str:
     """获取指定城市的天气信息。
     参数:
     city (str): 城市名称
     返回:
     str: 天气信息描述
     """
    #  city_weather_info = await city_server.get_city_weather(city)
     return "晴天"

mcp = FastMCP("CityDataServer")
# 初始化城市信息服务器
# city_server = CityDataServer()
# 获取天气信息的工具
@mcp.tool()
async def get_city_weather(city: str) -> str:
     """获取指定城市的天气信息。
     参数:
     city (str): 城市名称
     返回:
     str: 天气信息描述
     """
    #  city_weather_info = await city_server.get_city_weather(city)
     return "晴天"

@mcp.tool()
# 获取指定城市的信息
async def get_city_detail(city: str):
     """获取指定城市的信息。
     参数:
     city (str): 城市名称
     返回:
     str: 指定城市的信息
     """
    #  city_info = await city_server.get_city_detail(city)
     return "杭州"
# 主程序
if __name__ == "__main__":
     mcp.run(transport='stdio')