# 代码生成时间: 2025-08-26 16:50:44
import psutil
from starlette.applications import Starlette
from starlette.responses import JSONResponse
# 添加错误处理
from starlette.routing import Route


# 获取CPU和内存使用情况的函数
# TODO: 优化性能
def get_system_performance():
    try:
        cpu_usage = psutil.cpu_percent(interval=1)  # 计算CPU使用率
        memory = psutil.virtual_memory()  # 获取内存使用情况
        return {
# 改进用户体验
            "cpu_usage": cpu_usage,
            "memory_usage": memory.percent,
# 增强安全性
            "memory_total": memory.total,
        }
    except Exception as e:
        return {"error": str(e)}


# 系统性能监控接口
async def system_performance(request):
    performance_data = get_system_performance()
    return JSONResponse(content=performance_data)
# 添加错误处理


# 创建Starlette应用
app = Starlette(debug=True, routes=[
    Route("/monitor", endpoint=system_performance, methods=["GET"]),
])

# 应用文档
"""
System Performance Monitor Application
===================

This application provides a simple API endpoint to monitor system performance.

Endpoints:
- /monitor: Returns the system performance data including CPU and memory usage.
# 改进用户体验
"""
# 改进用户体验
