# 代码生成时间: 2025-09-12 05:18:42
import psutil
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

"""
Memory Usage Analyzer
====================

This Starlette application provides an endpoint to analyze the memory usage of the system.
It uses the psutil library to gather memory information and returns it as a JSON response.
"""

# Define the root route for the application
routes = [
    Route("/memory", endpoint=memory_usage_endpoint),
]

class MemoryUsageAnalyzer(Starlette):
    def __init__(self):
        super().__init__(routes=routes)

async def memory_usage_endpoint(request):
    """
    Endpoint to analyze memory usage of the system.

    Args:
        request (Request): The incoming HTTP request.

    Returns:
        Response: A JSON response containing the memory usage information.
    """
    try:
        # Get the memory usage statistics from psutil
        mem = psutil.virtual_memory()
        # Create a dictionary to store the memory usage information
        mem_info = {
            "total": mem.total,
            "available": mem.available,
            "used": mem.used,
            "free": mem.free,
            "percent": mem.percent,
        }
        # Return the memory usage information as a JSON response
        return JSONResponse(mem_info)
    except Exception as e:
        # Handle any exceptions that occur during memory usage analysis
        error_message = {"error": f"Failed to retrieve memory usage: {str(e)}"}
        return JSONResponse(error_message, status_code=500)

# Run the application if this script is executed directly
if __name__ == "__main__":
    MemoryUsageAnalyzer().run(host="0.0.0.0", port=8000)