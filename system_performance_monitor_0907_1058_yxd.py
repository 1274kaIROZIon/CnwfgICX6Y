# 代码生成时间: 2025-09-07 10:58:16
import os
import psutil
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route


# 获取系统信息的函数
def get_system_info():
    """
    返回系统的基本信息，包括CPU和内存使用情况。
    """
    system_info = {"cpu_usage": psutil.cpu_percent(),
                   "memory_usage": psutil.virtual_memory().percent}
    return system_info


# Starlette应用
class SystemPerformanceMonitor(Starlette):
    def __init__(self):
        super().__init__(routes=[
            Route("/", endpoint=self.index, methods=["GET"]),
            Route("/info", endpoint=self.get_system_info, methods=["GET"]),
        ])

    async def index(self, request):
        """
        首页路由，返回欢迎信息。
        """
        return JSONResponse("Welcome to the System Performance Monitor!")

    async def get_system_info(self, request):
        """
        返回系统性能监控信息。
        """
        try:
            system_info = get_system_info()
            return JSONResponse(system_info)
        except Exception as e:
            # 错误处理，返回错误信息
            return JSONResponse({"error": str(e)})


# 运行服务器
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(SystemPerformanceMonitor(), host='0.0.0.0', port=8000)