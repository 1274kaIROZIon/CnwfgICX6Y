# 代码生成时间: 2025-08-17 04:43:56
# json_converter_starlette.py
#
# This is a Starlette application that acts as a JSON data format converter.

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.requests import Request
import json


# A simple error handler function that returns a JSON response with an error message.
async def error_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Error handler that returns a JSON response with an error message.
    """
    return JSONResponse({'error': str(exc)}, status_code=400)


# The main JSON converter handler function.
async def json_converter(request: Request) -> JSONResponse:
    """
    This function takes the incoming JSON data,
    attempts to parse it and formats it back into JSON.
    It handles errors gracefully and returns a JSON response.
    """
    try:
        # Attempt to parse the incoming JSON data.
        data = await request.json()
        # Return the parsed and formatted JSON data.
        return JSONResponse(data)
    except json.JSONDecodeError as e:
        # Return an error response if JSON is invalid.
        return JSONResponse({'error': 'Invalid JSON'}, status_code=400)
    except Exception as e:
        # Generic error handling.
        return JSONResponse({'error': 'An unexpected error occurred'}, status_code=500)

# Define the routes for the application.
routes = [
    Route('/', json_converter),
]

# Create the Starlette application with the defined routes and error handler.
app = Starlette(routes=routes, exception_handlers={Exception: error_handler})

# The below code is for running the application in this script file.
# It is not required for the application to function as a module.
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
