# 代码生成时间: 2025-08-11 05:05:00
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND
import uvicorn


# 定义路由
routes = [
    Route('/', endpoint='RootHandler'),
    Route('/users/', endpoint='UsersHandler', methods=['GET']),
    Route('/users/{user_id}', endpoint='UserHandler', methods=['GET', 'POST', 'PUT', 'DELETE'])
]


# 根路由处理器
class RootHandler:
    async def __call__(self, request):
        return JSONResponse({'message': 'Welcome to the RESTful API'}, status_code=HTTP_200_OK)


# 用户列表处理器
class UsersHandler:
    async def __call__(self, request):
        return JSONResponse({'message': 'List of users'}, status_code=HTTP_200_OK)


# 单个用户处理器
class UserHandler:
    async def __call__(self, request):
        user_id = request.path_params['user_id']
        # 这里应该是数据库查询逻辑，为了示例，我们返回一个假的用户信息
        user = {'id': user_id, 'name': 'John Doe', 'email': 'johndoe@example.com'}
        return JSONResponse(user, status_code=HTTP_200_OK)


# 错误处理器
async def not_found(request, exc):
    return JSONResponse({'detail': 'Not found.'}, status_code=HTTP_404_NOT_FOUND)


# 创建Starlette应用
app = Starlette(debug=True, routes=routes, on_startup=[], on_shutdown=[], exception_handlers={'NotFound': not_found})

# 运行服务器
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)


# 注意：
# 1. 实际应用中，你需要替换UserHandler中的数据库查询逻辑。
# 2. 错误处理可以根据需要添加更多的异常处理器。
# 3. 这个例子中没有包含身份验证和授权逻辑，这些在生产环境中通常是必需的。