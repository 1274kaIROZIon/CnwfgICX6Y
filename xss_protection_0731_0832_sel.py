# 代码生成时间: 2025-07-31 08:32:45
from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.wsgi import WSGIMiddleware
from starlette.responses import HTMLResponse
from starlette.routing import Route
from starlette.types import Receive, Scope, Send
import bleach
from urllib.parse import urlparse, urlunparse


# XSS protection middleware
class XSSProtectionMiddleware:
    def __init__(self, app):
        self.app = app
    
    def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope['type'] == 'http':
            scope['headers'].append(("Content-Security-Policy", "default-src 'self'; script-src 'self' 'unsafe-inline'; img-src 'self' data:; connect-src 'self'; frame-ancestors 'none';"))
        
        async def call_next() -> None:
            await self.app(scope, receive, send)
        await call_next()

# Middleware configuration
middleware = [
    Middleware(XSSProtectionMiddleware, app=Starlette(debug=True))
]

# Endpoint to demonstrate XSS protection
async def homepage(request):
    user_input = request.query_params.get('input', '')
    # Sanitize user input to prevent XSS attacks
    sanitized_input = bleach.clean(user_input, tags=[], strip=True)
    # Construct the response HTML with sanitized input
    return HTMLResponse(
        f"<html><body><h1>XSS Protection</h1><p>You entered: {sanitized_input}</p></body></html>"
    )

# Routes
routes = [
    Route('/', homepage)
]

# Main application
app = Starlette(middleware=middleware, routes=routes)

# Command to run the application using uvicorn
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
