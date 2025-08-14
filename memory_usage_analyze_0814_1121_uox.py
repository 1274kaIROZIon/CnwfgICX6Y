# 代码生成时间: 2025-08-14 11:21:05
import psutil
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK

"""
A simple Starlette application that provides a route to analyze and report
memory usage.
"""

# Define the memory usage route
routes = [
    Route("/memory", endpoint=MemoryUsageHandler),
]


class MemoryUsageHandler:
    """
    A Starlette request handler that returns memory usage information.
    """
    def __init__(self):
        # Initialize any necessary attributes
        pass

    async def __call__(self, request):
        """
        Handles a GET request to the /memory endpoint.
        Returns a JSON response with memory usage statistics.
        """
        try:
            # Fetch memory usage statistics
            memory_stats = psutil.virtual_memory()

            # Prepare the response data
            response_data = {
                "total": memory_stats.total,
                "available": memory_stats.available,
                "used": memory_stats.used,
                "free": memory_stats.free,
                "used_percent": memory_stats.percent,
            }

            # Return a JSON response with the memory usage statistics
            return JSONResponse(response_data, status_code=HTTP_200_OK)
        except Exception as e:
            # Handle unexpected errors
            error_message = {"error": str(e)}
            return JSONResponse(error_message, status_code=HTTP_500_INTERNAL_SERVER_ERROR)


# Create and run the Starlette application
app = Starlette(debug=True, routes=routes)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
