# 代码生成时间: 2025-08-09 20:27:28
# api_response_formatter.py
# This module provides an API response formatter utility using Starlette framework.

from starlette.responses import JSONResponse
from starlette.requests import Request
from starlette.exceptions import HTTPException as StarletteHTTPException
import json


def api_response(
    request: Request, status_code: int, data: dict, message: str = ""
) -> JSONResponse:
    """
    Creates a standardized JSON response for APIs.
    
    Args:
        request (Request): The Starlette Request object.
        status_code (int): The HTTP status code for the response.
        data (dict): The data to be returned in the response.
        message (str): An optional message to include in the response.

    Returns:
        JSONResponse: A JSON formatted response.
    """
    response_data = {
        "status": status_code,
        "data": data,
    }
    if message:
        response_data["message"] = message
    
    try:
        return JSONResponse(response_data, status_code=status_code)
    except Exception as e:
        # Handle unexpected errors when creating the response
        return JSONResponse(
            {
                "status": 500,
                "message": "Internal Server Error",
                "error": str(e),
            },
            status_code=500,
        )


def error_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Error handler middleware for Starlette applications.
    
    Args:
        request (Request): The Starlette Request object.
        exc (Exception): The exception raised during request processing.

    Returns:
        JSONResponse: A JSON formatted response with error details.
    """
    if isinstance(exc, StarletteHTTPException):
        return JSONResponse(
            {
                "status": exc.status_code,
                "message": exc.detail,
            },
            status_code=exc.status_code,
        )
    else:
        return JSONResponse(
            {
                "status": 500,
                "message": "An unexpected error occurred.",
                "error": str(exc),
            },
            status_code=500,
        )

# Example usage of the api_response function
# from starlette.app import Starlette
# from starlette.routing import Route
#
# app = Starlette(debug=True)
#
# @app.route("/example", methods=["GET"])
# async def example(request: Request):
#     try:
#         return api_response(request, 200, {"key": "value"}, "Success")
#     except Exception as e:
#         return error_handler(request, e)
