from mcp.server.fastmcp import FastMCP
import os
from mcp.types import TextContent
import httpx
import logging
import json



# 创建MCP服务器实例
mcp = FastMCP(
    name="dataeyes-mcp-server",
    version="0.1.0",
    instructions="This is a MCP server for Dataeyes."
)


"""

获取环境变量中的 API 密钥, 用于调用数眼智能 API
环境变量名为: DATAEYES_API_KEY
获取方式请访问: https://shuyanai.com 

"""

api_key = os.getenv('DATAEYES_API_KEY')
# api_key = "sk-WEqKb5gdY84MAbTj3rHYZ1nvUhB3ogkC"
api_url = "https://api.shuyanai.com"


@mcp.tool(description="读取网页内容并返回大模型友好的 Markdown 格式")
async def reader(url: str, timeout: int = 30) -> str:

    """
    读取网页内容并返回大模型友好的 Markdown 格式

    Args:
        url (str): 要读取的网页链接.
        timeout (int): 页面加载超时时间，单位为秒（1-60）.

    Returns:
        str: 返回包含网页内容的 Markdown 格式.

    """


    try:
        if not api_key:
            raise ValueError("请设置环境变量 DATAEYES_API_KEY, 获取方式请访问: https://shuyanai.com")
        reader_url = f"{api_url}/v1/reader"

        # 参数设置
        params = {
            "url": url,
            "timeout": timeout,
        }

        # 请求头设置
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(reader_url, params=params, headers=headers)
            response.raise_for_status()
            result = response.json()

            # 检查返回码是否成功
            if result.get("code") == 0 and "data" in result:
                
                return json.dumps(result["data"], ensure_ascii=False, indent=2)
            else:
                # 如果 code 不为 0 或 data 不存在，返回错误信息
                error_msg = result.get("msg", "Unknown error from API")
                return f"API Error: {error_msg}"


    except httpx.HTTPError as e:
        raise Exception(f"HTTP request failed: {str(e)}") from e
    except Exception as e:
        logging.error(f"An unexpected error occurred in reader tool: {str(e)}")
        return f"An unexpected error occurred: {str(e)}"



if __name__ == "__main__":
    mcp.run(transport="stdio")
