# 代码生成时间: 2025-08-22 03:38:32
import base64
import cryptography.fernet
"""
密码加密解密工具，使用Python和Starlette框架。
"""

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

# 定义加密和解密函数
class PasswordUtility:
    def __init__(self, key):
        self.key = key
        self.cipher_suite = cryptography.fernet.Fernet(key)

    def encrypt(self, plaintext):
        """
        加密明文密码

        :param plaintext: 明文密码
        :return: 加密后的密码
        """
        return self.cipher_suite.encrypt(plaintext.encode()).decode()

    def decrypt(self, ciphertext):
        """
        解密密文密码

        :param ciphertext: 密文密码
        :return: 明文密码
        """
        return self.cipher_suite.decrypt(ciphertext.encode()).decode()

# 定义Starlette路由和应用
routes = [
    Route('/', endpoint=PasswordUtility, methods=['GET', 'POST']),
]

# 初始化密钥
key = base64.urlsafe_b64encode(cryptography.fernet.Fernet.generate_key()).decode()

# 创建Starlette应用
app = Starlette(debug=True, routes=routes)

# 实现处理请求的函数
async def password_utility(request):
    if request.method == 'POST':
        try:
            data = await request.json()
            plaintext = data.get('plaintext')
            ciphertext = data.get('ciphertext')
            if plaintext:
                utility = PasswordUtility(key)
                encrypted_password = utility.encrypt(plaintext)
                return JSONResponse({'encrypted_password': encrypted_password})
            elif ciphertext:
                utility = PasswordUtility(key)
                decrypted_password = utility.decrypt(ciphertext)
                return JSONResponse({'decrypted_password': decrypted_password})
            else:
                return JSONResponse({'error': 'Invalid request'}, status_code=400)
        except Exception as e:
            return JSONResponse({'error': str(e)}, status_code=500)
    else:
        return JSONResponse({'error': 'Invalid method'}, status_code=405)

# 更新路由函数
routes[0].endpoint = password_utility
