# 代码生成时间: 2025-08-15 07:03:02
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import random
import uuid
"""
Random Number Generator API using Starlette framework.
This API provides an endpoint to generate a random number between
specified minimum and maximum values.
"""

class RandomNumberGenerator:
    def __init__(self, min_value: int, max_value: int):
        self.min_value = min_value
        self.max_value = max_value

    def generate_random_number(self) -> int:
        """
        Generate a random number between min_value and max_value.
        """
        if self.min_value > self.max_value:
            raise ValueError("Minimum value cannot be greater than maximum value.")
        return random.randint(self.min_value, self.max_value)

    def to_dict(self) -> dict:
        """
        Convert random number generator state to a dictionary.
        """
        return {"min_value": self.min_value, "max_value": self.max_value}

async def generate_random_number_endpoint(request):
    """
    Endpoint to generate a random number between min and max values.
    """
    min_value = request.query_params.get("min", 1, type=int)
    max_value = request.query_params.get("max", 100, type=int)
    try:
        generator = RandomNumberGenerator(min_value, max_value)
        random_number = generator.generate_random_number()
        return JSONResponse(
            content={
                "random_number": random_number,
                "generator_info": generator.to_dict(),
            }
        )
    except ValueError as e:
        return JSONResponse(
            content={
                "error": str(e),
            }, status_code=400
        )

# Define routes for the application
routes = [
    Route("/generate", endpoint=generate_random_number_endpoint),
]

# Create the Starlette application
app = Starlette(debug=True, routes=routes)
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)