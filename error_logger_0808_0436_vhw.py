# 代码生成时间: 2025-08-08 04:36:47
import logging
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.errors import ServerErrorMiddleware


# 设置日志配置
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class ErrorLoggerMiddleware(BaseHTTPMiddleware):
    """
    中间件用于捕获并记录所有异常错误日志。
    """
    async def dispatch(self, request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            logger.error(f'Error: {exc}')
            if isinstance(exc, HTTPException):
                return JSONResponse({'detail': exc.detail}, status_code=exc.status_code)
            else:
                return ServerErrorMiddleware().dispatch(request, exc)


class ErrorHandler:
    """
    错误处理器，用于处理不同类型错误并返回适当的响应。
    """
    async def __call__(self, request, exc):
        if isinstance(exc, HTTPException):
            return JSONResponse({'detail': exc.detail}, status_code=exc.status_code)
        else:
            logger.error(f'Unhandled Error: {exc}')
            return JSONResponse({'detail': 'An unexpected error occurred'}, status_code=500)


# 创建 Starlette 应用
app = Starlette(middleware=[
    ErrorLoggerMiddleware(),
    ServerErrorMiddleware(handler=ErrorHandler())
])


# 定义路由
@app.route('/test', methods=['GET'])
async def test(request):
    """
    测试路由，模拟抛出异常。
    """
    raise ValueError('Test error occurred.')


# 启动应用
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
