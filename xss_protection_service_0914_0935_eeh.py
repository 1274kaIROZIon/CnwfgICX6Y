# 代码生成时间: 2025-09-14 09:35:19
import re
from starlette.requests import Request
from starlette.responses import Response
from starlette.routing import Route
from starlette.applications import Starlette
from starlette.middleware.base import BaseHTTPMiddleware
from html import escape

# Middleware for XSS protection
class XSSMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, allowed_tags=None):
        super().__init__(app)
        self.allowed_tags = allowed_tags or []

    async def dispatch(self, request: Request, call_next):
        # Intercept the response and sanitize content
        response = await call_next(request)
        if response.body:
            # Sanitize the response body
            sanitized_body = self.sanitize_html(response.body.decode())
            response.body = sanitized_body.encode()
        return response

    def sanitize_html(self, html_content):
        # Allow only specific tags and attributes
        for tag in self.allowed_tags:
            # Allow tags like <b>, <i>, etc.
            html_content = re.sub(rf"<{tag}>(.*?)</{tag}>", r"\1", html_content)
        # Remove any other tags
        return re.sub(r"<[^>]*>", "", html_content)

# Application factory function
def xss_protection_app(allowed_tags=None):
    routes = [
        Route("/", endpoint=xss_protection_handler, methods=["GET", "POST"]),
    ]
    middleware = [XSSMiddleware(lambda _: None, allowed_tags)]
    return Starlette(routes=routes, middleware=middleware)

# Handler for XSS protection
async def xss_protection_handler(request: Request):
    try:
        # Get request data
        data = await request.json()
        # Sanitize input data to prevent XSS
        sanitized_data = {key: escape(str(value)) for key, value in data.items()}
        # Return sanitized data
        return Response(content=str(sanitized_data), media_type="application/json")
    except Exception as e:
        # Handle any unexpected errors
        return Response(content=str(e), status_code=500)

# Run the application using Uvicorn if this is the main module
if __name__ == "__main__":
    from uvicorn import run
    run(xss_protection_app(), host="0.0.0.0", port=8000)
