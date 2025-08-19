# 代码生成时间: 2025-08-20 06:30:12
# api_response_formatter.py
# A tool to format API responses using Starlette framework.

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.requests import Request
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from typing import Any, Dict


class APIResponseFormatter:
    """
    A class to format API responses with a specific structure.
    It adds error handling and ensures the response is JSON formatted.
    """
    def __init__(self, app: Starlette):
        self.app = app

    def format_response(self, request: Request, data: Any, status_code: int = HTTP_200_OK) -> JSONResponse:
        """
        Formats the response data into a JSONResponse with a specific structure.
        :param request: The incoming request object.
        :param data: The data to be formatted in the response.
        :param status_code: The HTTP status code of the response.
        :return: A JSONResponse object.
        """
        try:
            # Here we assume 'data' to be a dictionary. If not, it should be converted to a dictionary or handled accordingly.
            if not isinstance(data, dict):
                data = {'error': 'Invalid data type, expected a dictionary.'}
                status_code = HTTP_400_BAD_REQUEST
            # Format the response data
            response_data = {'status': 'success', 'data': data}
            return JSONResponse(response_data, status_code=status_code)
        except Exception as e:
            # Log the exception (not shown here) and return an error response
            error_message = {'status': 'error', 'message': str(e)}
            return JSONResponse(error_message, status_code=HTTP_500_INTERNAL_SERVER_ERROR)


# Create the Starlette application instance
app = Starlette()

# Instantiate the APIResponseFormatter with the app
response_formatter = APIResponseFormatter(app)

# Define an example endpoint that uses the response formatter
@app.route("/example")
async def example(request: Request):
    # Simulate some data retrieval logic
    data = {"message": "Hello, World!"}
    # Use the formatter to create the response
    return response_formatter.format_response(request, data)

# Run the application if this file is executed as the main program
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)