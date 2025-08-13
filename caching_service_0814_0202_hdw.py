# 代码生成时间: 2025-08-14 02:02:34
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware import Middleware
from starlette.types import ASGIApp, Receive, Scope, Send
import time
import functools

# Middleware to handle caching
class SimpleCacheMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, cache_timeout: int = 300):
        super().__init__(app)
        self.cache_timeout = cache_timeout
        self.cache = {}

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope['type'] != 'http':
            return await self.next(scope, receive, send)

        # Check if the request path is in the cache
        path = scope['path']
        current_time = time.time()

        # If cached response exists and is not expired, return it
        if path in self.cache and (current_time - self.cache[path]['timestamp'] < self.cache_timeout):
            response = self.cache[path]['response']
            await response(scope, receive, send)
            return

        # Call the next middleware
        await self.next(scope, receive, send)

        # Check if the response is cacheable
        if scope['method'] == 'GET':
            # Create a cached response
            response = await self.cache_response(scope, receive, send)
            # Store the response in the cache
            self.cache[path] = {'timestamp': current_time, 'response': response}

    async def cache_response(self, scope: Scope, receive: Receive, send: Send):
        await self.next(scope, receive, send)
        response = scope['response']
        return response

# Example route for demonstration purposes
async def example_route(request):
    return JSONResponse(content={'message': 'This is a cached response.'}, media_type='application/json')

# Create a Starlette app with the caching middleware
app = Starlette(middleware=[Middleware(SimpleCacheMiddleware, cache_timeout=60)])

app.add_route('/', example_route)

# This is a simple demonstration of a caching service using Starlette.
# The SimpleCacheMiddleware handles caching, storing responses for GET requests for a specified timeout.
# The cache is stored in-memory and is not persistent across server restarts.
# For production use, consider using a more robust caching solution like Redis or Memcached.
