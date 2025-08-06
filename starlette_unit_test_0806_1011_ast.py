# 代码生成时间: 2025-08-06 10:11:21
import pytest
from starlette.testclient import TestClient
from starlette import status
from starlette.responses import JSONResponse
from your_starlette_app import app  # Import your Starlette app module

# Unit test class
class TestStarletteUnit:
    """
    Unit tests for Starlette app.
    """
    def test_root_route(self):
        """
        Test the root route of the app.
        """
        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "Hello World"}

    def test_nonexistent_route(self):
        """
        Test a route that does not exist.
        """
        client = TestClient(app)
        response = client.get("/nonexistent")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_error_handling(self):
        """
        Test that error responses are correctly handled.
        """
        client = TestClient(app)
        # Simulate an internal server error
        response = client.get("/error")
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert isinstance(response.json(), dict)

    def test_json_response(self):
        """
        Test that JSON responses are correctly formatted.
        """
        client = TestClient(app)
        response = client.get("/json")
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), dict)

# Run the tests
if __name__ == "__main__":
    pytest.main(["-v", __file__])
