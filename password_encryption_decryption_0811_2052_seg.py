# 代码生成时间: 2025-08-11 20:52:24
import os
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from cryptography.fernet import Fernet

"""
密码加密解密工具
"""

# 密码加密/解密工具
class PasswordTool:
    def __init__(self, key=None):
        # 如果没有提供密钥，则生成一个新的密钥
        self.key = key or self.generate_key()
        self.cipher_suite = Fernet(self.key)

    def generate_key(self):
        # 生成一个密钥并返回
        return Fernet.generate_key()

    def encrypt(self, plaintext):
        # 加密给定的明文
        return self.cipher_suite.encrypt(plaintext.encode()).decode()

    def decrypt(self, ciphertext):
        # 解密给定的密文
        try:
            return self.cipher_suite.decrypt(ciphertext.encode()).decode()
        except Exception as e:
            raise ValueError("Invalid encryption key or corrupted data.") from e


# Starlette 应用
class PasswordToolApp(Starlette):
    def __init__(self):
        super().__init__(
            routes=[
                Route("/encrypt", self.encrypt, methods=["POST"]),
                Route("/decrypt", self.decrypt, methods=["POST"]),
            ]
        )
        self.password_tool = PasswordTool()

    async def encrypt(self, request):
        # 加密请求
        data = await request.json()
        plaintext = data.get("plaintext")
        if not plaintext:
            return JSONResponse({"error": "Missing plaintext."}, status_code=400)
        ciphertext = self.password_tool.encrypt(plaintext)
        return JSONResponse({"ciphertext": ciphertext})

    async def decrypt(self, request):
        # 解密请求
        data = await request.json()
        ciphertext = data.get("ciphertext")
        if not ciphertext:
            return JSONResponse({"error": "Missing ciphertext."}, status_code=400)
        try:
            plaintext = self.password_tool.decrypt(ciphertext)
            return JSONResponse({"plaintext": plaintext})
        except ValueError as e:
            return JSONResponse({"error": str(e)}, status_code=400)

# 主函数
def main():
    # 运行应用
    PasswordToolApp().run(host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()