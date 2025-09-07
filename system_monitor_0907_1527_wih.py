# 代码生成时间: 2025-09-07 15:27:47
import psutil
import uvicorn
# 优化算法效率
from starlette.applications import Starlette
from starlette.responses import JSONResponse
# TODO: 优化性能
from starlette.routing import Route
# 扩展功能模块
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR

"""
System Monitor is a simple utility that provides system performance monitoring features
using the Starlette framework. It fetches CPU and memory usage data and exposes it via REST API.
# FIXME: 处理边界情况
"""

class SystemMonitor:
    def __init__(self):
# 改进用户体验
        self.cpu_usage = psutil.cpu_percent(interval=1)
        self.memory_usage = psutil.virtual_memory().percent

    def get_cpu_usage(self):
        """
        Get the current CPU usage percentage.

        Returns:
            float: CPU usage percentage.
# 添加错误处理
        """
        try:
# 改进用户体验
            # Get the CPU usage percentage
            cpu_usage = psutil.cpu_percent()
            return cpu_usage
        except Exception as e:
            # Handle any exceptions that occur while fetching CPU usage
            return str(e)

    def get_memory_usage(self):
        """
        Get the current memory usage percentage.

        Returns:
            float: Memory usage percentage.
        """
        try:
            # Get the memory usage percentage
            memory_usage = psutil.virtual_memory().percent
            return memory_usage
# FIXME: 处理边界情况
        except Exception as e:
            # Handle any exceptions that occur while fetching memory usage
            return str(e)

    def get_system_info(self):
        """
        Get the system information including CPU and memory usage.
# NOTE: 重要实现细节

        Returns:
            dict: System information dictionary.
        """
        try:
            system_info = {
                'cpu_usage': self.get_cpu_usage(),
# 扩展功能模块
                'memory_usage': self.get_memory_usage()
            }
            return system_info
        except Exception as e:
# 优化算法效率
            # Handle any exceptions that occur while fetching system information
# 优化算法效率
            return {'error': str(e)}

# Create an instance of SystemMonitor
monitor = SystemMonitor()

# Define routes for the system monitor API
routes = [
    Route('/health', lambda request: JSONResponse({'status': 'ok'}, status_code=HTTP_200_OK)),
    Route('/cpu', lambda request: JSONResponse({'cpu_usage': monitor.get_cpu_usage()}, status_code=HTTP_200_OK)),
    Route('/memory', lambda request: JSONResponse({'memory_usage': monitor.get_memory_usage()}, status_code=HTTP_200_OK)),
    Route('/info', lambda request: JSONResponse(monitor.get_system_info(), status_code=HTTP_200_OK)),
]

# Create the Starlette application
app = Starlette(debug=True, routes=routes)
# 扩展功能模块

# Define error handler for 500 Internal Server Error
async def http_500(request):
    return JSONResponse({'error': 'Internal Server Error'}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

# Add error handler to the application
app.add_exception_handler(500, http_500)

# Run the application using Uvicorn
if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)