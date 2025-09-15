# 代码生成时间: 2025-09-16 03:31:55
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR
import json
import random
import string

"""
Test Data Generator is a simple REST API that generates random test data.
It is built using the Starlette framework.

The API has a single endpoint that returns a JSON response with a list of random data.
Each item in the list is a dictionary with a random string key and a random string value.
"""

def generate_random_data(num_items=10):
    """
    Generate a list of random data.
    Each item is a dictionary with a random string key and a random string value.
    :param num_items: The number of items to generate (default is 10).
    :return: A list of random data.
    """
    random_data = []
    for _ in range(num_items):
        key = ''.join(random.choice(string.ascii_letters) for _ in range(8))
        value = ''.join(random.choice(string.ascii_letters) for _ in range(8))
        random_data.append({'key': key, 'value': value})
    return random_data

async def random_data_endpoint(request):
    """
    The endpoint that returns a JSON response with a list of random data.
    :param request: The incoming HTTP request.
    :return: A JSON response with a list of random data.
    """
    try:
        num_items = request.query_params.get('num_items', 10)
        if not isinstance(num_items, int) or num_items <= 0:
            raise ValueError('Invalid num_items parameter')
        random_data = generate_random_data(num_items)
        return JSONResponse(random_data, status_code=HTTP_200_OK)
    except Exception as e:
        return JSONResponse({'error': str(e)}, status_code=HTTP_500_INTERNAL_SERVER_ERROR)

def create_app():
    """
    Create the Starlette application.
    :return: The Starlette application.
    """
    app = Starlette(debug=True)
    app.add_route('/random-data', random_data_endpoint)
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
