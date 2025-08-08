# 代码生成时间: 2025-08-08 21:37:54
# starlette_unit_test.py

"""
A simple unit testing framework using Starlette for creating and testing
API endpoints.
"""

from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse
from starlette.testclient import TestClient
import pytest


# Define a simple route
async def test_endpoint(request):
    """
    A simple endpoint that returns a JSON response.
    """
    return JSONResponse({'message': 'Hello, World!'})

# Define the main application
app = Starlette(debug=True, routes=[
    Route('/', test_endpoint),
])

class TestStarletteApp:
    """
    Test class for the Starlette application.
    """
    def setup_class(cls):
        """
        Set up the test client before running tests.
        """
        cls.client = TestClient(app)

    def teardown_class(cls):
        """
        Clean up after all tests have run.
        """
        cls.client.close()

    def test_get_root(self):
        """
        Test the GET request on the root endpoint.
        """
        response = self.client.get('/')
        assert response.status_code == 200
        assert response.json() == {'message': 'Hello, World!'}

    def test_get_nonexistent(self):
        """
        Test a GET request on a nonexistent endpoint.
        """
        response = self.client.get('/nonexistent')
        assert response.status_code == 404


# Run the tests
if __name__ == '__main__':
    pytest.main([__file__])
