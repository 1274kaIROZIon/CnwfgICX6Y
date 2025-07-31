# 代码生成时间: 2025-08-01 00:23:54
import starlette.requests as Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from starlette.routing import Route
from starlette.applications import Starlette
from typing import Dict
import math

"""
Math Toolbox Starlette Application
This application provides a set of mathematical operations via REST API.
"""

# Define a simple class to perform mathematical operations
class MathToolbox:
    def add(self, a: float, b: float) -> float:
        """Add two numbers"""
        return a + b

    def subtract(self, a: float, b: float) -> float:
        """Subtract two numbers"""
        return a - b

    def multiply(self, a: float, b: float) -> float:
        """Multiply two numbers"""
        return a * b

    def divide(self, a: float, b: float) -> float:
        """Divide two numbers"""
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b

    def power(self, a: float, b: float) -> float:
        """Raise a to the power of b"""
        return math.pow(a, b)

# Define routes for the application
routes = [
    Route("/add", endpoint=lambda request: calculate(request, MathToolbox().add), methods=["POST"]),
    Route("/subtract", endpoint=lambda request: calculate(request, MathToolbox().subtract), methods=["POST"]),
    Route("/multiply", endpoint=lambda request: calculate(request, MathToolbox().multiply), methods=["POST"]),
    Route("/divide", endpoint=lambda request: calculate(request, MathToolbox().divide), methods=["POST"]),
    Route("/power", endpoint=lambda request: calculate(request, MathToolbox().power), methods=["POST"])
]

# Define a function to handle the requests and calculate the result
async def calculate(request: Request, operation) -> JSONResponse:
    data: Dict = await request.json()
    try:
        result = operation(**data)
        return JSONResponse(status_code=HTTP_200_OK, content={"result": result})
    except ValueError as e:
        return JSONResponse(status_code=HTTP_400_BAD_REQUEST, content={"error": str(e)})
    except Exception as e:
        return JSONResponse(status_code=HTTP_400_BAD_REQUEST, content={"error": "An unexpected error occurred"})

# Create the Starlette application
app = Starlette(debug=True, routes=routes)

# Run the application with uvicorn
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)