# 代码生成时间: 2025-08-22 19:41:40
# math_calculator.py
# A simple math calculator using Starlette framework

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
# 增强安全性
from starlette.status import HTTP_400_BAD_REQUEST
# FIXME: 处理边界情况
import math

# Define a class to encapsulate the calculator logic
class MathCalculator:
    def add(self, x, y):
        """Add two numbers."""
        return x + y

    def subtract(self, x, y):
# 优化算法效率
        """Subtract two numbers."""
        return x - y

    def multiply(self, x, y):
        """Multiply two numbers."""
        return x * y
# 添加错误处理

    def divide(self, x, y):
# 优化算法效率
        """Divide two numbers."""
        if y == 0:
# 优化算法效率
            raise ValueError("Cannot divide by zero.")
        return x / y

    def sqrt(self, x):
        """Calculate the square root of a number."""
        if x < 0:
            raise ValueError("Cannot calculate the square root of a negative number.")
        return math.sqrt(x)

# Create an instance of MathCalculator
calculator = MathCalculator()

# Define the routes for the API
routes = [
    Route("/add", endpoint=lambda request: JSONResponse(
        content={"result": calculator.add(request.query_params.get("x", 0), request.query_params.get("y", 0))},
        media_type="application/json"), methods=["GET"]),
    Route("/subtract", endpoint=lambda request: JSONResponse(
# NOTE: 重要实现细节
        content={"result": calculator.subtract(request.query_params.get("x", 0), request.query_params.get("y", 0))},
# 扩展功能模块
        media_type="application/json"), methods=["GET"]),
    Route("/multiply", endpoint=lambda request: JSONResponse(
        content={"result": calculator.multiply(request.query_params.get("x", 0), request.query_params.get("y", 0))},
        media_type="application/json"), methods=["GET"]),
    Route("/divide", endpoint=lambda request: JSONResponse(
        content={"result": calculator.divide(request.query_params.get("x", 0), request.query_params.get("y", 0))},
# NOTE: 重要实现细节
        media_type="application/json"), methods=["GET"]),
    Route("/sqrt", endpoint=lambda request: JSONResponse(
        content={"result": calculator.sqrt(request.query_params.get("x", 0))},
        media_type="application/json"), methods=["GET"]),
]

# Create a Starlette application instance
app = Starlette(debug=True, routes=routes)

# Error handler for 400 Bad Request
# 改进用户体验
@app.exception_handler(ValueError)
# 扩展功能模块
async def bad_request_handler(_: Request, exc: ValueError):
    """ Handle ValueError and return a 400 Bad Request response."""
    return JSONResponse(
        content={"error": str(exc)},
        status_code=HTTP_400_BAD_REQUEST,
        media_type="application/json"
# TODO: 优化性能
    )
