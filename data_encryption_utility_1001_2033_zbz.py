# 代码生成时间: 2025-10-01 20:33:49
# data_encryption_utility.py
# A utility for encrypting and decrypting data using Starlette framework

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from cryptography.fernet import Fernet
import base64

# Generate a key for encryption and decryption
# This key should be kept secret in a real-world application
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Function to encrypt data
def encrypt_data(data: str) -> str:
    """Encrypts the provided plaintext data using Fernet.

    Args:
        data (str): The plaintext data to encrypt.

    Returns:
        str: The encrypted data in a base64-encoded string.
    """
    try:
        # Encrypt the data and encode it in base64 to ensure it's safe for transmission
        encrypted_data = cipher_suite.encrypt(data.encode())
        return base64.b64encode(encrypted_data).decode()
    except Exception as e:
        raise ValueError("Encryption failed: " + str(e))

# Function to decrypt data
def decrypt_data(data: str) -> str:
    """Decrypts the provided encrypted data using Fernet.

    Args:
        data (str): The encrypted data in a base64-encoded string.

    Returns:
        str: The decrypted plaintext data.
    """
    try:
        # Decode the base64 data and decrypt it
        encrypted_data = base64.b64decode(data)
        decrypted_data = cipher_suite.decrypt(encrypted_data)
        return decrypted_data.decode()
    except Exception as e:
        raise ValueError("Decryption failed: " + str(e))

# Endpoint to handle encryption requests
async def encrypt_endpoint(request):
    """Handles POST requests to encrypt data."""
    data = await request.body()
    try:
        encrypted = encrypt_data(data.decode())
        return JSONResponse({'encrypted_data': encrypted})
    except ValueError as e:
        return JSONResponse({'error': str(e)}, status_code=400)

# Endpoint to handle decryption requests
async def decrypt_endpoint(request):
    """Handles POST requests to decrypt data."""
    data = await request.body()
    try:
        decrypted = decrypt_data(data.decode())
        return JSONResponse({'decrypted_data': decrypted})
    except ValueError as e:
        return JSONResponse({'error': str(e)}, status_code=400)

# Create a Starlette application with the encryption and decryption endpoints
app = Starlette(
    routes=[
        Route("/encrypt", encrypt_endpoint, methods=["POST"]),
        Route("/decrypt", decrypt_endpoint, methods=["POST"]),
    ]
)

# If running this script directly, run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)