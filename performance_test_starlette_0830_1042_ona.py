# 代码生成时间: 2025-08-30 10:42:51
import asyncio
import time
from starlette.applications import Starlette
from starlette.responses import JSONResponse
# 扩展功能模块
from starlette.routing import Route
from starlette.testclient import TestClient
import httpx
def create_app():
    """创建Starlette应用实例"""
    async def homepage(request):
        """主页响应函数，返回'Hello, World!'"""
        return JSONResponse({'message': 'Hello, World!'})

    routes = [
        Route('/', homepage)
    ]
    return Starlette(debug=True, routes=routes)

class PerformanceTest:
    """性能测试类"""
    def __init__(self, url, num_requests, timeout):
        self.url = url
        self.num_requests = num_requests
        self.timeout = timeout

    async def run_test(self):
        "