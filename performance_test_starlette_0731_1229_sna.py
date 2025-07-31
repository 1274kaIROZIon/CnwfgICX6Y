# 代码生成时间: 2025-07-31 12:29:19
import asyncio
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import time
import requests
import threading
import concurrent.futures
from typing import Any, List


# Middleware to log request duration
class RequestTimerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        print(f"Request duration: {duration:.2f} seconds")
        return response


# Main application class
class PerformanceTestApp(Starlette):
    def __init__(self):
        routes = [
            Route("/", endpoint=self.home, methods=["GET"]),
            Route("/test", endpoint=self.test, methods=["GET"]),
        ]
        super().__init__(routes=routes, middleware=[RequestTimerMiddleware()])

    async def home(self, request: Request) -> Response:
        return JSONResponse({"message": "Welcome to the Performance Test App"})

    async def test(self, request: Request) -> Response:
        try:
            # Simulate a time-consuming operation
            await asyncio.sleep(1)
            return JSONResponse({"message": "Test endpoint response"})
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)


# Function to perform a single test
def perform_test(url: str) -> None:
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error: {e}")


# Entry point for performance testing
def main() -> None:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_performance_test())

async def run_performance_test() -> None:
    app = PerformanceTestApp()
    host = "localhost"
    port = 8000
    url = f"http://{host}:{port}"
    test_urls = [f"{url}/", f"{url}/test"]
    tasks = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for test_url in test_urls:
            tasks.append(executor.submit(perform_test, test_url))
        for future in concurrent.futures.as_completed(tasks):
            try:
                future.result()
            except Exception as e:
                print(f"Error during test: {e}")

if __name__ == "__main__":
    main()
