# 代码生成时间: 2025-09-08 09:54:00
from starlette.responses import JSONResponse
from starlette.requests import Request
from pydantic import BaseModel

# 数据模型
class User(BaseModel):
    id: int
    username: str
    email: str

# 服务类，处理请求
class UserDataService:
    def __init__(self):
        self.users = []

    def add_user(self, request: Request, user_data: User):
        """添加新用户"""
        if not user_data.username or not user_data.email:
            raise ValueError("用户名和邮箱不能为空")
        self.users.append(user_data)
        return JSONResponse(content={"message": "用户添加成功"}, status_code=201)

    def get_user(self, user_id: int):
        """根据ID获取用户信息"""
        for user in self.users:
            if user.id == user_id:
                return JSONResponse(content=user.dict())
        return JSONResponse(content={"error": "用户未找到"}, status_code=404)

# 路由和逻辑处理
async def add_user_route(request: Request):
    user_service = UserDataService()
    try:
        user_data = await User(**request.json())
        return user_service.add_user(request, user_data)
    except ValueError as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

async def get_user_route(request: Request, user_id: int):
    user_service = UserDataService()
    return user_service.get_user(user_id)

# 路由配置
routes = [
    {"path": "/users", "endpoint": add_user_route, "methods": ["POST"]},
    {"path": "/users/{user_id}", "endpoint": get_user_route, "methods": ["GET"]},
]
