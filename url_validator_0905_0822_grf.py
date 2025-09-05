# 代码生成时间: 2025-09-05 08:22:52
import aiohttp
from starlette.applications import Starlette
from starlette.exceptions import HTTPException
from starlette.middleware import Middleware
from starlette.responses import JSONResponse, Response
from starlette.routing import Route
from urllib.parse import urlparse, parse_qs


# URL验证中间件
class URLValidatorMiddleware:
    async def __call__(self, scope, receive, send):
        if scope['type'] == 'http':
            url = urlparse(scope['path'])
            if not url.scheme or not url.netloc:
                raise HTTPException(status_code=400, detail="Invalid URL")
            # 可以在这里添加额外的URL验证逻辑
            # 例如检查URL是否指向有效的HTTP/HTTPS地址
            if url.scheme not in ['http', 'https']:
                raise HTTPException(status_code=400, detail="Unsupported protocol")
        await self.next(scope, receive, send)


# URL验证函数
async def validate_url(request):
    # 获取URL参数
    url = request.query_params.get('url')
    if not url:
        return JSONResponse({'error': 'URL parameter is missing'}, status_code=400)
    
    try:
        # 使用aiohttp传递HEAD请求以验证URL
        async with aiohttp.ClientSession() as session:
            async with session.head(url) as response:
                if response.status >= 400:
                    return JSONResponse({'error': 'URL is invalid or not reachable'}, status_code=400)
                return JSONResponse({'message': 'URL is valid'}, status_code=200)
    except aiohttp.ClientError as e:
        return JSONResponse({'error': 'Failed to validate URL'}, status_code=500)


# 创建Starlette应用
app = Starlette(
    middleware=[
        Middleware(URLValidatorMiddleware),
    ],
    routes=[
        Route('/api/validate_url', validate_url, methods=['GET']),
    ]
)

# 运行应用
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)