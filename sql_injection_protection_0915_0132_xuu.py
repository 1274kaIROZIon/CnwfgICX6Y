# 代码生成时间: 2025-09-15 01:32:18
import sqlite3
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.requests import Request
from starlette.status import HTTP_400_BAD_REQUEST

# 数据库配置
DATABASE_URL = 'database.db'

# 错误处理装饰器
def error_handling(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except sqlite3.Error as e:
            return JSONResponse({"error": str(e)}, status_code=HTTP_400_BAD_REQUEST)
    return wrapper

# 数据库查询函数
@error_handling
async def query_db(query, params):
    """
    执行数据库查询并防止SQL注入。
    
    参数:
    query (str): SQL查询语句。
    params (tuple): 查询参数。
    
    返回:
    list: 查询结果。
    """
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# 路由和端点
routes = [
    Route("/", endpoint=lambda request: JSONResponse({"message": "Hello, World!"})),
    Route("/users", endpoint=lambda request: JSONResponse([{"name": "Alice", "age": 30}, {"name": "Bob", "age": 25}])),
    Route("/users/{user_id}", endpoint=get_user)
]

# 获取用户信息，防止SQL注入
async def get_user(request: Request):
    """
    根据用户ID获取用户信息。
    
    参数:
    request (Request): HTTP请求对象。
    
    返回:
    JSONResponse: 用户信息。
    """
    user_id = request.path_params['user_id']
    query = "SELECT * FROM users WHERE id = ?"
    params = (user_id,)
    result = await query_db(query, params)
    if not result:
        return JSONResponse({"error": "User not found"}, status_code=HTTP_400_BAD_REQUEST)
    return JSONResponse(result[0])

# 创建Starlette应用
app = Starlette(routes=routes)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)