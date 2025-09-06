# 代码生成时间: 2025-09-06 09:19:52
# test_data_generator.py"""
A simple test data generator using Starlette framework.
"""
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK
import random
import string


# Define constants for data generation
MIN_LENGTH = 5
MAX_LENGTH = 20

class TestDataGenerator:
    def __init__(self):
        self.data_store = []

    def generate_random_string(self, length):
        """
        Generates a random string of a given length.
        Args:
            length (int): The length of the string to generate.
        Returns:
            str: A random string.
        """
        if not isinstance(length, int) or length < MIN_LENGTH or length > MAX_LENGTH:
            raise ValueError("Length must be an integer between {} and {}".format(MIN_LENGTH, MAX_LENGTH))
        return ''.join(random.choice(string.ascii_letters) for _ in range(length))

    def generate_test_data(self):
        """
        Generates test data and stores it in the data store.
        Returns:
            list: A list of test data.
        """
        self.data_store.append(self.generate_random_string(random.randint(MIN_LENGTH, MAX_LENGTH)))
        return self.data_store


# Create an instance of the TestDataGenerator
test_data_generator = TestDataGenerator()

# Define routes
routes = [
    Route("/test-data", endpoint=lambda request: JSONResponse(test_data_generator.generate_test_data()), methods=["GET"]),
]

# Create a Starlette application
app = Starlette(debug=True, routes=routes)

# Entry point for the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
