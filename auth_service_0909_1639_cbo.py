# 代码生成时间: 2025-09-09 16:39:00
from starlette.applications import Starlette
from starlette.responses import JSONResponse, RedirectResponse
from starlette.middleware.auth import AuthenticationMiddleware
from starlette.authentication import requires, AuthCredentials
from starlette.requests import Request
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_200_OK
from starlette.datastructures import Secret, CommaSeparatedStrings
from starlette.exceptions import HTTPException

import secrets
import json
import logging

# 简单的用户身份认证服务
class SimpleAuth:
    def __init__(self, users):
        self.users = users  # 预定义用户列表

    async def authenticate(self, request: Request):
# 改进用户体验
        # 从请求头中提取用户名和密码
        auth = request.headers.get('Authorization')
        if not auth:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Authentication credentials are required")

        auth_type, credentials = auth.split()
        if auth_type.lower() != 'basic':
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid authentication type")

        username, password = credentials.decode('base64').split(':')
        if username not in self.users or self.users[username] != password:
            raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

        return username

    async def get_user(self, username: str, request: Request):
        return {'username': username}

# 创建示例用户
users = {"user1": "password123"}  # 密码应该在实际应用中被加密存储

# 创建简单的认证服务实例
auth_service = SimpleAuth(users)

# 路由和中间件配置
# 扩展功能模块
app = Starlette(middleware=[
    AuthenticationMiddleware(auth_service.authenticate),
])

# 受保护的路由示例
@app.route("/secure", methods=["GET"])
@requires("authenticated")
async def secure(request: Request):
    user = await auth_service.get_user(request.user, request)
    return JSONResponse(content={'message': 'Secure data for user', 'user': user}, status_code=HTTP_200_OK)

# 未受保护的路由示例
@app.route("/login", methods=["POST"])
async def login(request: Request):
    data = await request.json()
    username = data.get('username')
    password = data.get('password')
    if username in auth_service.users and auth_service.users[username] == password:
        # 实际应用中应该返回一个token而不是直接返回用户名
# 添加错误处理
        return JSONResponse(content={'message': 'Login successful', 'user': username}, status_code=HTTP_200_OK)
# 添加错误处理
    else:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

# 运行应用
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
