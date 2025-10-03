# 代码生成时间: 2025-10-04 00:00:33
# data_masking_app.py

"""
Data Masking Application using Starlette framework

This application provides a simple data masking tool that can be used to mask sensitive data.
"""

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK

# Importing necessary libraries for data masking
import re
import random

# Constants for data masking patterns
PHONE_PATTERN = re.compile(r"\b\d{3}[-\.\s]?\d{3}[-\.\s]?\d{4}\b")
EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b")
CREDIT_CARD_PATTERN = re.compile(r"\b[0-9]{16}\b")

# Function to mask sensitive data
def mask_data(text):
    """
    Mask sensitive data in the given text.
    Supported data types:
    - Phone numbers
    - Email addresses
    - Credit card numbers
    """
    # Mask phone numbers
    masked_text = PHONE_PATTERN.sub("XXX-XXX-XXXX", text)
    # Mask email addresses
    masked_text = EMAIL_PATTERN.sub("XXX@XXX.XXX", masked_text)
    # Mask credit card numbers
    masked_text = CREDIT_CARD_PATTERN.sub("XXXX-XXXX-XXXX-XXXX", masked_text)
    return masked_text

# Data Masking Endpoint
async def mask_data_endpoint(request):
    """
    Endpoint to handle data masking requests.
    It expects a JSON payload with a 'text' key containing the data to be masked.
    """
    try:
        data = await request.json()
        text_to_mask = data.get("text")
        if text_to_mask is None:
            return JSONResponse(
                {
                    "error": "Missing 'text' key in request body."
                },
                status_code=400
            )
        masked_text = mask_data(text_to_mask)
        return JSONResponse(
            {
                "original_text": text_to_mask,
                "masked_text": masked_text
            },
            status_code=HTTP_200_OK
        )
    except ValueError as e:
        return JSONResponse(
            {
                "error": f"Invalid JSON payload: {str(e)}"
            },
            status_code=400
        )

# Define Starlette application routes
routes = [
    Route("/mask", mask_data_endpoint, methods=["POST"]),
]

# Create and run Starlette application
app = Starlette(debug=True, routes=routes)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
