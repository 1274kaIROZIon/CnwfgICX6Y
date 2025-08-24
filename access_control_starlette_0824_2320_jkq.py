# 代码生成时间: 2025-08-24 23:20:10
import starlette.status as status
from starlette.responses import JSONResponse
from starlette.authentication import requires, AuthenticationBackend, AuthCredentials, SimpleUser
from starlette.requests import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from starlette.utils import is_async_callable

# 定义一个简单的认证后端
class SimpleAuthBackend(AuthenticationBackend):
    def authenticate(self, request: Request):
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            # 这里假设验证逻辑是检查一个简单的用户名和密码
            if auth_header == 'Bearer secret_token':
                return AuthCredentials(['authenticated'])
        return None

# 创建一个中间件来处理访问控制
class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 通过认证中间件获取用户信息
        auth = await self.auth_backend.authenticate(request)
        if auth is None:
            # 如果认证失败，返回401 Unauthorized
            return JSONResponse(
                {'detail': 'Authentication credentials were not provided.'},
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        # 如果认证成功，添加用户信息到请求中
        request.user = SimpleUser(**auth)
        return await call_next(request)

# 创建一个路由保护函数
def require_authorization(func):
    @requires('authenticated', status=401)
    def wrapper(request: Request, *args, **kwargs):
        return await func(request, *args, **kwargs)
    return wrapper

# 一个受保护的视图函数
@require_authorization
async def protected_view(request: Request):
    return JSONResponse(
        content={"message": "Hello from protected view"},
        status_code=status.HTTP_200_OK
    )

# 应用工厂函数，返回ASGI应用
def create_app():
    # 创建AuthMiddleware实例
    auth_middleware = AuthMiddleware(SimpleAuthBackend())
    # 创建Starlette应用
    from starlette.applications import Starlette
    app = Starlette(debug=True)
    # 添加路由
    app.add_route("/protected", protected_view)
    # 添加中间件
    app.add_middleware(AuthMiddleware, backend=SimpleAuthBackend())
    return app

# 以下是运行应用的代码（通常这部分代码会放在一个单独的文件中，如main.py）
# if __name__ == "__main__":
#     from starlette.applications import Starlette
#     app = Starlette(debug=True)
#     app.add_route("/protected", protected_view)
#     app.add_middleware(AuthMiddleware, backend=SimpleAuthBackend())
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)