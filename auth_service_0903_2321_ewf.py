# 代码生成时间: 2025-09-03 23:21:53
from starlette.applications import Starlette
from starlette.authentication import requires, AuthenticationBackend, AuthCredentials, SimpleUser
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_200_OK
import secrets
import jwt
import datetime
import base64
import hmac
import hashlib


# 用于身份认证的服务类
class SimpleAuthBackend(AuthenticationBackend):
    def __init__(self, users):
        self.users = users
# FIXME: 处理边界情况

    async def authenticate(self, request):
        # 从请求中提取Authorization头部
        auth = request.headers.get('Authorization')
        if not auth:
            return None
        # 提取Bearer token
        prefix, token = auth.split()
        if prefix.lower() != 'bearer':
            return None
        try:
            # 解码和验证JWT token
            payload = jwt.decode(token, options={"verify_signature": False})
            username = payload.get('sub')
            if username not in self.users:
# NOTE: 重要实现细节
                return None
            # 验证token签名
# 优化算法效率
            signature = hmac.new(self.users[username], msg=token.encode('utf-8'), digestmod=hashlib.sha256).digest()
            if not base64.b64encode(signature).decode('utf-8') == token.split('.')[2]:
                return None
            return AuthCredentials(['authenticated']), SimpleUser(username)
        except jwt.PyJWTError:
# FIXME: 处理边界情况
            return None
# TODO: 优化性能

# 用于生成JWT token的函数
def generate_token(username, users):
    secret_key = users[username]
    payload = {
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
# 增强安全性
        'iat': datetime.datetime.utcnow(),
# 改进用户体验
        'sub': username
    }
# 改进用户体验
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

# 创建一个用户字典，用于存储用户名和对应的密钥
users = {
# TODO: 优化性能
    'user1': secrets.token_urlsafe(32),
    'user2': secrets.token_urlsafe(32)
}

# 创建一个Starlette应用
app = Starlette(
    middleware=[
        AuthenticationMiddleware(SimpleAuthBackend(users))
    ]
)
# FIXME: 处理边界情况

# 定义一个路由，用于生成token
@app.route('/token', methods=['POST'])
async def issue_token(request: Request):
    username = request.form['username']
# 改进用户体验
    password = request.form['password']
    if username in users and hmac.compare_digest(users[username], password.encode('utf-8')):
        token = generate_token(username, users)
        return JSONResponse({'token': token}, status_code=HTTP_200_OK)
    return JSONResponse({'detail': 'Incorrect username or password'}, status_code=HTTP_401_UNAUTHORIZED)

# 定义一个受保护的路由，需要认证才能访问
@app.route('/protected', methods=['GET'])
@requires('authenticated')
async def protected_route(request: Request, user: SimpleUser):
# TODO: 优化性能
    return JSONResponse({'message': f'Hello, {user.username}!'}, status_code=HTTP_200_OK)

# 定义一个未认证用户访问受保护路由时的响应
# NOTE: 重要实现细节
@app.exception_handler(AuthenticationError)
async def authentication_exception_handler(request, exc):
    return JSONResponse({'detail': 'Authentication credentials were not provided'}, status_code=HTTP_401_UNAUTHORIZED)

# 运行应用
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)