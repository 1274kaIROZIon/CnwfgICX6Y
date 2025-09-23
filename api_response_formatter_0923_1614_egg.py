# 代码生成时间: 2025-09-23 16:14:40
import starlette.responses
from starlette.requests import Request
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR

class ApiResponseFormatter:
    def __init__(self):
        """
        Initializes the ApiResponseFormatter instance.
        This class is responsible for formatting API responses.
        """
        pass

    def format_response(self, request: Request, data: dict, status_code: int = HTTP_200_OK):
        """
        Formats the API response with the given data and status code.

        Args:
            request (Request): The incoming request object.
            data (dict): The data to be included in the response.
            status_code (int): The HTTP status code for the response.

        Returns:
            JSONResponse: A JSON response object with the formatted data.
        """
        response_data = {
            "status": "success" if status_code < 400 else "error",
            "data": data,
            "message": "Data retrieved successfully" if status_code == HTTP_200_OK else "Bad request",
            "code": status_code,
        }
        return starlette.responses.JSONResponse(response_data, status_code=status_code)

    def handle_error(self, request: Request, exc: Exception):
        """
        Handles errors by formatting an error response.

        Args:
            request (Request): The incoming request object.
            exc (Exception): The exception that occurred.

        Returns:
            JSONResponse: A JSON response object with the error details.
        """
        error_message = f"An error occurred: {str(exc)}"
        return starlette.responses.JSONResponse(
            {
                "status": "error",
                "data": None,
                "message": error_message,
                "code": HTTP_500_INTERNAL_SERVER_ERROR,
            },
            status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        )

# Example usage of the ApiResponseFormatter
# async def example_endpoint(request: Request):
#     try:
#         # Perform some operation
#         # ...
#         return ApiResponseFormatter().format_response(request, {"key": "value"})
#     except Exception as e:
#         return ApiResponseFormatter().handle_error(request, e)