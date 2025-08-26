# 代码生成时间: 2025-08-26 09:20:24
import logging
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.requests import Request
from starlette.routing import Route, Router
from starlette.exceptions import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.exceptions import ExceptionMiddleware
import datetime
import traceback

# 配置日志
logging.basicConfig(level=logging.ERROR, filename='error.log', filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class ErrorLogCollectorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as exc:
            # 记录错误信息到日志文件
            self.log_error(exc)
            # 重新抛出异常以便 ExceptionMiddleware 处理
            raise

    def log_error(self, exc):
        error_message = f"Error occurred: {str(exc)}
{traceback.format_exc()}
"
        logger.error(error_message)


async def log_error_middleware(request: Request, exc: HTTPException):
    logger.error(f"HTTPException: {exc.detail}")
    return JSONResponse(
        content={"detail": exc.detail}, status_code=exc.status_code
    )


# 定义路由
routes = [
    Route("/error", endpoint=lambda request: "This will trigger an error", methods=["GET"]),
    # 添加其他路由
]

# 添加错误日志中间件
middleware = [
    ErrorLogCollectorMiddleware(),
    ExceptionMiddleware(),  # 默认的错误处理中间件
    ExceptionMiddleware(error_handling={404: log_error_middleware}),  # 定制404错误处理
]

# 创建Starlette应用
app = Starlette(routes=routes, middleware=middleware)


# 运行应用（在实际部署中，你可能需要使用 Uvicorn 或其他 ASGI 服务器）
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
