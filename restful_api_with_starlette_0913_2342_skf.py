# 代码生成时间: 2025-09-13 23:42:22
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.exceptions import HTTPException


# 定义一个简单的用户模型
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def to_dict(self):
        return {"name": self.name, "email": self.email}


# 模拟数据库中存储的用户数据
users_db = [User("John Doe", "john.doe@example.com"), User("Jane Doe", "jane.doe@example.com