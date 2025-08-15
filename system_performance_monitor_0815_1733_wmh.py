# 代码生成时间: 2025-08-15 17:33:38
import psutil
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR

"""
A Starlette application for monitoring system performance.
"""

class SystemPerformanceMonitor:
    def __init__(self):
        """Initialize the SystemPerformanceMonitor instance."""
        self.app = Starlette(debug=True)
        self.routes = [
            Route("/monitor", self.monitor_system, methods=["GET"]),
        ]
        self.app.add_routes(self.routes)

    def monitor_system(self, request):
        """
        Monitor system performance metrics.

        Returns a JSON response containing CPU, memory, and disk usage.
        """
        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory_usage = psutil.virtual_memory().percent
            disk_usage = psutil.disk_usage('/').percent
            data = {
                "cpu_usage": cpu_usage,
                "memory_usage": memory_usage,
                "disk_usage": disk_usage
            }
            return JSONResponse(status_code=HTTP_200_OK, content=data)
        except Exception as e:
            """
            Error handling mechanism to catch and log unexpected exceptions.
            """
            return JSONResponse(
                status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                content={"error": str(e)}
            )

    def run(self, host="0.0.0.0", port=8000):
        """
        Run the Starlette application on the specified host and port.
        """
        self.app.run(host=host, port=port)

# Create an instance of SystemPerformanceMonitor and run the application
if __name__ == "__main__":
    monitor = SystemPerformanceMonitor()
    monitor.run()