# 代码生成时间: 2025-09-24 05:29:11
import psutil
import starlette.status as status
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

"""
System Performance Monitor

A simple Starlette application to monitor system performance metrics.
"""

class SystemMonitor:
    def __init__(self):
        self.cpu = psutil.cpu_percent(interval=1)
        self.memory = psutil.virtual_memory().percent
        self.disk = psutil.disk_usage('/').percent

    def get_cpu_usage(self):
        """
        Get the current CPU usage percentage.
        """
        return self.cpu

    def get_memory_usage(self):
        """
        Get the current memory usage percentage.
        """
        return self.memory

    def get_disk_usage(self):
        """
        Get the current disk usage percentage.
        """
        return self.disk

    async def get_performance_data(self):
        """
        Get the current system performance data.
        """
        try:
            cpu = self.get_cpu_usage()
            memory = self.get_memory_usage()
            disk = self.get_disk_usage()
            return JSONResponse(
                content={
                    'cpu_usage': cpu,
                    'memory_usage': memory,
                    'disk_usage': disk
                },
                status_code=status.HTTP_200_OK
            )
        except Exception as e:
            return JSONResponse(
                content={
                    'error': str(e)
                },
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

def main():
    monitor = SystemMonitor()
    app = Starlette(debug=True)
    app.add_route("/", monitor.get_performance_data, methods=["GET"])
    app.run(host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
