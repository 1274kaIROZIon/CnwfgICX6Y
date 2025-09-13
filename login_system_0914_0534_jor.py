# 代码生成时间: 2025-09-14 05:34:48
from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED

import uvicorn
import bcrypt

# 这里模拟一个简单的用户数据库，实际应用中应使用数据库存储用户信息
fake_db = {
    'user1': bcrypt.hashpw("password1".encode('utf-8'), bcrypt.gensalt())
}

class LoginSystem:
    async def login(self, request):
        # 获取请求体中的用户名和密码
        username = request.query_params.get('username')
        password = request.query_params.get('password')

        # 验证用户名和密码是否提供
        if not username or not password:
            return JSONResponse(
                {"error": "Missing username or password"}, status_code=HTTP_401_UNAUTHORIZED
            )

        # 检查用户名是否存在于数据库中
        if username not in fake_db:
            return JSONResponse(
                {"error": "Invalid username or password"}, status_code=HTTP_401_UNAUTHORIZED
            )

        # 验证密码
        if bcrypt.checkpw(password.encode('utf-8'), fake_db[username]):
            return JSONResponse({"message": "Login successful"}, status_code=HTTP_200_OK)
        else:
            return JSONResponse(
                {"error": "Invalid username or password"}, status_code=HTTP_401_UNAUTHORIZED
            )

# 创建一个Starlette应用
app = Starlette(debug=True, routes=[
    Route("/login", endpoint=LoginSystem().login, methods=["GET"])
])

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
