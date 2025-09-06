# 代码生成时间: 2025-09-07 01:03:51
import starlette.responses as responses
import starlette.routing as routing
import starlette.requests as requests
import starlette.status as status
from starlette.application import Starlette
import random

class RandomNumberGenerator:
    """
    A class to handle random number generation.
    Provides an endpoint to generate a random number between a specified range.
    """

    def __init__(self, min_value=0, max_value=100):
        self.min_value = min_value
        self.max_value = max_value

    def generate_random_number(self):
        """
        Generates a random number between the specified range.
        """
        try:
            return random.randint(self.min_value, self.max_value)
        except ValueError:
            # Handle the case where the min_value is greater than max_value
            raise ValueError("Min value cannot be greater than max value")

    async def get_random_number(self, request: requests.Request):
        """
        Handles GET requests to generate a random number.
        Returns a JSON response with the random number.
        """
        try:
            random_number = self.generate_random_number()
            return responses.JSONResponse(
                content={"random_number": random_number},
                status_code=status.HTTP_200_OK
            )
        except ValueError as e:
            return responses.JSONResponse(
                content={"error": str(e)},
                status_code=status.HTTP_400_BAD_REQUEST
            )

    async def get_random_number_with_range(self, request: requests.Request, min_value: int, max_value: int):
        """
        Handles GET requests to generate a random number within a specified range.
        Returns a JSON response with the random number.
        """
        self.min_value = min_value
        self.max_value = max_value
        try:
            random_number = self.generate_random_number()
            return responses.JSONResponse(
                content={"random_number": random_number},
                status_code=status.HTTP_200_OK
            )
        except ValueError as e:
            return responses.JSONResponse(
                content={"error": str(e)},
                status_code=status.HTTP_400_BAD_REQUEST
            )

app = Starlette(
    routes=[
        routing.Route("/random", endpoint=RandomNumberGenerator().get_random_number, methods=["GET"]),
        routing.Route("/random/{min_value}/{max_value}", endpoint=RandomNumberGenerator().get_random_number_with_range, methods=["GET"]),
    ],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)