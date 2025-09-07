# 代码生成时间: 2025-09-08 00:11:29
import math
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import JSONResponse
from starlette.requests import Request
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_200_OK

# Define a simple math toolbox class with various mathematical operations
class MathToolbox:
    def add(self, a, b):
        """Add two numbers.
        Args:
            a (float): The first number.
            b (float): The second number.
        Returns:
            float: The sum of a and b.
        """
        return a + b

    def subtract(self, a, b):
        """Subtract two numbers.
        Args:
            a (float): The first number.
            b (float): The second number.
        Returns:
            float: The difference of a and b.
        """
        return a - b

    def multiply(self, a, b):
        """Multiply two numbers.
        Args:
            a (float): The first number.
            b (float): The second number.
        Returns:
            float: The product of a and b.
        """
        return a * b

    def divide(self, a, b):
        """Divide two numbers.
        Args:
            a (float): The first number.
            b (float): The second number.
        Returns:
            float: The quotient of a and b.
        Raises:
            ZeroDivisionError: If b is zero.
        """
        if b == 0:
            raise ValueError('Cannot divide by zero.')
        return a / b

    def power(self, a, b):
        """Raise a number to the power of another number.
        Args:
            a (float): The base number.
            b (float): The exponent.
        Returns:
            float: The result of a to the power of b.
        """
        return a ** b

    def square_root(self, a):
        """Calculate the square root of a number.
        Args:
            a (float): The number.
        Returns:
            float: The square root of a.
        Raises:
            ValueError: If a is negative.
        """
        if a < 0:
            raise ValueError('Cannot calculate the square root of a negative number.')
        return math.sqrt(a)

# Create an instance of the MathToolbox
math_toolbox = MathToolbox()

# Define routes for the math operations
routes = [
    Route('/', lambda request: JSONResponse({'message': 'Welcome to the Math Toolbox API!'}), methods=['GET']),
    Route('/add', lambda req: add_handler(req, math_toolbox.add), methods=['POST']),
    Route('/subtract', lambda req: subtract_handler(req, math_toolbox.subtract), methods=['POST']),
    Route('/multiply', lambda req: multiply_handler(req, math_toolbox.multiply), methods=['POST']),
    Route('/divide', lambda req: divide_handler(req, math_toolbox.divide), methods=['POST']),
    Route('/power', lambda req: power_handler(req, math_toolbox.power), methods=['POST']),
    Route('/square_root', lambda req: square_root_handler(req, math_toolbox.square_root), methods=['POST']),
]

# Define a function to handle addition requests
def add_handler(request: Request, operation):
    data = request.json()
    try:
        result = operation(data['a'], data['b'])
        return JSONResponse({'result': result}, status_code=HTTP_200_OK)
    except (TypeError, KeyError) as e:
        return JSONResponse({'error': str(e)}, status_code=HTTP_400_BAD_REQUEST)

# Define a function to handle subtraction requests
def subtract_handler(request: Request, operation):
    data = request.json()
    try:
        result = operation(data['a'], data['b'])
        return JSONResponse({'result': result}, status_code=HTTP_200_OK)
    except (TypeError, KeyError) as e:
        return JSONResponse({'error': str(e)}, status_code=HTTP_400_BAD_REQUEST)

# Define a function to handle multiplication requests
def multiply_handler(request: Request, operation):
    data = request.json()
    try:
        result = operation(data['a'], data['b'])
        return JSONResponse({'result': result}, status_code=HTTP_200_OK)
    except (TypeError, KeyError) as e:
        return JSONResponse({'error': str(e)}, status_code=HTTP_400_BAD_REQUEST)

# Define a function to handle division requests
def divide_handler(request: Request, operation):
    data = request.json()
    try:
        result = operation(data['a'], data['b'])
        return JSONResponse({'result': result}, status_code=HTTP_200_OK)
    except ValueError as e:
        return JSONResponse({'error': str(e)}, status_code=HTTP_400_BAD_REQUEST)
    except (TypeError, KeyError) as e:
        return JSONResponse({'error': str(e)}, status_code=HTTP_400_BAD_REQUEST)

# Define a function to handle power requests
def power_handler(request: Request, operation):
    data = request.json()
    try:
        result = operation(data['a'], data['b'])
        return JSONResponse({'result': result}, status_code=HTTP_200_OK)
    except (TypeError, KeyError) as e:
        return JSONResponse({'error': str(e)}, status_code=HTTP_400_BAD_REQUEST)

# Define a function to handle square root requests
def square_root_handler(request: Request, operation):
    data = request.json()
    try:
        result = operation(data['a'])
        return JSONResponse({'result': result}, status_code=HTTP_200_OK)
    except ValueError as e:
        return JSONResponse({'error': str(e)}, status_code=HTTP_400_BAD_REQUEST)
    except (TypeError, KeyError) as e:
        return JSONResponse({'error': str(e)}, status_code=HTTP_400_BAD_REQUEST)

# Create the Starlette application
app = Starlette(debug=True, routes=routes)
