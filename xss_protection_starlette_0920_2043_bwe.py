# 代码生成时间: 2025-09-20 20:43:33
import starlette.responses
from starlette.routing import Route
from starlette.applications import Starlette
from starlette.middleware import Middleware
# 添加错误处理
from starlette.middleware.base import BaseHTTPMiddleware
# TODO: 优化性能
from html import escape
from markupsafe import Markup


# Middleware to handle XSS
class XSSMiddleware(BaseHTTPMiddleware):
# 扩展功能模块
    def dispatch(self, request, call_next):
        """Handles XSS protection by escaping the response body."""
        response = call_next(request)
        return self.escape_response(response)

    def escape_response(self, response):
        """Escapes the response content to prevent XSS."""
        if response.body:
            escaped_body = escape(response.body.decode('utf-8'))
            response.body = escaped_body.encode('utf-8')
        return response


# Example route
async def home(request):
    """Example endpoint that is vulnerable to XSS if not handled properly."""
    user_input = request.query_params.get('input', 'Default input')
    # In a real-world scenario, we should escape the user_input
# TODO: 优化性能
    # to prevent XSS attacks. For demonstration, we will just return it.
    return starlette.responses.HTMLResponse(f"<html><body><h1>You entered: {Markup.escape(escape(user_input))}</h1></body></html>")


# Main application
app = Starlette(routes=[
    Route("/", home)
],
    middleware=[
        Middleware(XSSMiddleware)
    ]
)
# 添加错误处理

# This is a simple example to demonstrate how to integrate XSS protection middleware.
# 添加错误处理
# In production, you would likely need a more robust solution that handles different
# content types, encodings, and scenarios.
