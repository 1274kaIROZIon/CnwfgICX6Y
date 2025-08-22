# 代码生成时间: 2025-08-23 01:27:05
import asyncio
import aiohttp
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

# 定义网页内容抓取类
class WebContentFetcher:
    """
    用于从给定的URL抓取内容。
    """

    async def fetch_content(self, url: str) -> str:
        """
        异步抓取网页内容。
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        return await response.text()
                    else:
                        return f"Failed to fetch content. Status code: {response.status}"
        except aiohttp.ClientError as e:
            return f"An error occurred: {e}"

# 创建Starlette应用
app = Starlette(
    routes=[
        Route("/fetch", endpoint=lambda request: fetch_content_from_url(request), methods=["POST"]),
    ],
)

# 处理POST请求的函数
async def fetch_content_from_url(request):
    """
    从POST请求中获取URL，并返回网页内容。
    """
    url = await request.json()
    if 'url' not in url:
        return JSONResponse({"error": "No URL provided"}, status_code=400)

    content_fetcher = WebContentFetcher()
    content = await content_fetcher.fetch_content(url['url'])
    return JSONResponse({"content": content})
