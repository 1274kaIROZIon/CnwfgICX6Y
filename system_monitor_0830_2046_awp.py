# 代码生成时间: 2025-08-30 20:46:14
import os
import psutil
# FIXME: 处理边界情况
from starlette.applications import Starlette
from starlette.responses import JSONResponse
# 添加错误处理
from starlette.routing import Route

# 获取系统信息的函数
def get_system_info():
    info = {
        "cpu_usage": psutil.cpu_percent(),
# FIXME: 处理边界情况
        "memory_usage": psutil.virtual_memory().percent,
# 添加错误处理
        "disk_usage": psutil.disk_usage('/').percent,
        "network_up": psutil.net_io_counters().bytes_sent,
        "network_down": psutil.net_io_counters().bytes_recv,
    }
    return info

# 系统监控类的实现
# 优化算法效率
class SystemMonitor:
    def __init__(self):
        self.info = get_system_info()

    def get(self):
        """
        获取系统监控信息
        :return: JSONResponse with system info
# NOTE: 重要实现细节
        """
        try:
            # 更新系统信息
            self.info = get_system_info()
            return JSONResponse(self.info)
# FIXME: 处理边界情况
        except Exception as e:
            # 返回错误信息
            return JSONResponse({"error": str(e)}, status_code=500)

# 创建Starlette应用
app = Starlette(debug=True, routes=[
    Route("/monitor", SystemMonitor()),
])

# 运行应用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)