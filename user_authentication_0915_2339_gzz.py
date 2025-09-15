# 代码生成时间: 2025-09-15 23:39:28
import starlette.authentication
import starlette.requests
import starlette.responses
import starlette.status
from starlette.authentication import SimpleUser, AuthenticationBackend, AuthenticationError
from starlette.middleware import Middleware
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.types import ASGIApp

# 定义一个简单的用户模型
class SimpleUserWithScopes(SimpleUser):
    def __init__(self, username, scopes=None):
        super().__init__(username)
        self.scopes = scopes or []

# 定义用户认证后端
class MyAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):
        # 这里使用一个简单的示例，实际应用中应该使用更安全的身份验证机制
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        # 假设auth_header的格式是'Bearer TOKEN'
        try:
            scheme, credentials = auth_header.split()
        except ValueError:
            return None

        if scheme.lower() != 'bearer':
            return None
        if credentials != 'your_secret_token':
            return None

        # 返回用户信息和作用域
        return SimpleUserWithScopes(username='admin', scopes=['admin:read', 'admin:write'])

# 创建一个中间件用于处理身份验证
middleware = AuthenticationMiddleware(app=ASGIApp(), backend=MyAuthBackend(), dispatch_func=lambda request: request)

# 创建一个路由处理函数，检查用户是否具有特定作用域
async def requires_admin_write(request: starlette.requests.Request) -> starlette.responses.Response:
    # 尝试获取用户对象
    user = await request.user

    # 如果用户没有admin:write作用域，则返回401错误
    if not (user and 'admin:write' in user.scopes):
        return starlette.responses.Response(
            "Insufficient permissions", status_code=starlette.status.HTTP_401_UNAUTHORIZED
        )

    # 如果用户具有admin:write作用域，继续处理请求
    return starlette.responses.Response(
        "Admin user with 'admin:write' scope", status_code=starlette.status.HTTP_200_OK
    )

# 创建一个简单的Starlette应用
def app(scope):
    return starlette.Starlette(
        debug=True,
        routes=[
            ("/", starlette.routing.RouteHandler(requires_admin_write)),
        ],
        middleware=[middleware],
    )

# 运行应用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)