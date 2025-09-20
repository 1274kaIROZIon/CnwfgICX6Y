# 代码生成时间: 2025-09-20 13:15:07
# integration_test_starlette.py

"""
An example of an integration test using Starlette framework.
This script demonstrates how to create an integration test for a Starlette application.
"""

import pytest
from starlette.testclient import TestClient
from starlette import status
from starlette.responses import JSONResponse


# Assuming we have an example application 'app.py' that we want to test
# from app import app as starlette_app


# Define a test function with pytest
def test_root_endpoint():
    # Create a TestClient instance for our Starlette application
    with TestClient(starlette_app) as client:
        # Make a GET request to the root endpoint
        response = client.get('/')
        # Check the status code
        assert response.status_code == status.HTTP_200_OK
        # Check the response content
        assert response.json() == {'message': 'Hello World'}

    # Alternatively, you can test with a POST request
    response = client.post('/data', json={'key': 'value'})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'key': 'value'}


# You can add more test functions for different endpoints
def test_nonexistent_endpoint():
    with TestClient(starlette_app) as client:
        response = client.get('/nonexistent')
        assert response.status_code == status.HTTP_404_NOT_FOUND


# You can also test error handling
def test_error_handling():
    with TestClient(starlette_app) as client:
        response = client.get('/error')
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert 'error' in response.json()


# To run these tests, use pytest from the command line:
# pytest integration_test_starlette.py

# Note: Replace 'starlette_app' with the actual app instance from your Starlette application.
