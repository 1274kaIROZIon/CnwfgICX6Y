# 代码生成时间: 2025-09-18 07:10:22
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import hashlib
import uvicorn


class HashCalculator:
    """ Class to calculate hash values for strings. """

    @staticmethod
    def calculate_hash(value: str, algorithm: str) -> str:
        """
        Calculate the hash value of the given string using the specified algorithm.

        Args:
        value (str): The string to calculate the hash value for.
        algorithm (str): The hashing algorithm to use (e.g., 'md5', 'sha1', 'sha256').

        Returns:
        str: The hash value of the input string.
        """
        try:
            hash_func = getattr(hashlib, algorithm)()
        except AttributeError:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
        hash_func.update(value.encode('utf-8'))
        return hash_func.hexdigest()


async def calculate(request):
    """
    Endpoint to calculate the hash value for a given string.

    Args:
    request: The incoming HTTP request.

    Returns:
    JSONResponse: A JSON response containing the calculated hash value.
    """
    data = await request.json()
    value = data.get('value')
    algorithm = data.get('algorithm')

    if not value or not algorithm:
        return JSONResponse(
            content={"error": "Missing 'value' or 'algorithm' parameter."},
            status_code=400
        )

    hash_value = HashCalculator.calculate_hash(value, algorithm)
    return JSONResponse(content={"hash": hash_value})


routes = [
    Route("/hash", endpoint=calculate, methods=["POST"])
]


app = Starlette(debug=True, routes=routes)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
