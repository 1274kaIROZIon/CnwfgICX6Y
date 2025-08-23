# 代码生成时间: 2025-08-23 14:12:31
import starlette.applications
import starlette.responses
import starlette.routing
import starlette.requests
import uuid

# 数据生成器类
class TestDataGenerator:
    """用于生成随机测试数据的类"""
    def __init__(self, data_size=100):
        """初始化方法
        Args:
            data_size (int): 生成的数据大小
        """
        self.data_size = data_size

    def generate_data(self):
        """生成随机测试数据
        Returns:
            list: 包含随机数据的列表
        """
        data = []
        for _ in range(self.data_size):
            data.append({
                'id': str(uuid.uuid4()),
                'name': f"User{_+1}",
                'email': f"user{_+1}@example.com",
                'is_active': True
            })
        return data

# Starlette应用
app = starlette.applications.Starlette(debug=True)

# 路由列表
routes = [
    starlette.routing.Route(
        path='/generate-data',
        endpoint=TestDataGenerator().generate_data,
        name='generate_data'
    )
]

# 添加路由
app.routes.extend(routes)

# 错误处理
@app.exception_handler(404)
async def not_found(request: starlette.requests.Request, exc: Exception):
    """404错误处理"""
    return starlette.responses.JSONResponse(
        content={'message': 'Resource not found'},
        status_code=404
    )

# 健康检查端点
@app.route('/health')
async def health_check(request: starlette.requests.Request):
    """健康检查端点"""
    return starlette.responses.JSONResponse(
        content={'status': 'ok'},
        status_code=200
    )
