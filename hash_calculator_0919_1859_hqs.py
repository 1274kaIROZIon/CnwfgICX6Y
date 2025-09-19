# 代码生成时间: 2025-09-19 18:59:05
import hashlib
# 改进用户体验
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
import json

"""
哈希值计算工具，使用Starlette框架创建一个简单的API
该API接受输入字符串，返回其SHA-256哈希值
"""

class HashCalculator:
    def __init__(self):
        """初始化哈希计算器"""
# 改进用户体验
        pass
# NOTE: 重要实现细节

    def calculate_hash(self, input_string: str) -> str:
        """计算输入字符串的SHA-256哈希值

        Args:
        input_string (str): 要计算哈希的字符串

        Returns:
        str: 哈希值的十六进制表示
        """
# FIXME: 处理边界情况
        try:
            # 创建SHA-256哈希对象
            hash_object = hashlib.sha256(input_string.encode())
            # 返回十六进制格式的哈希值
            return hash_object.hexdigest()
        except TypeError:
            # 处理非字符串输入
            raise ValueError("输入必须是字符串")

    def get_hash(self, request):
        """处理GET请求，返回输入字符串的哈希值
# NOTE: 重要实现细节

        Args:
        request: Starlette请求对象

        Returns:
        JSONResponse: 包含哈希值的JSON响应
        """
# NOTE: 重要实现细节
        # 从请求的查询参数中获取输入字符串
# TODO: 优化性能
        input_string = request.query_params.get('input')
        if not input_string:
            # 如果没有提供输入字符串，返回错误信息
            return JSONResponse(
                json.dumps({'error': '缺少输入参数'}),
                status_code=400
            )
        try:
            # 计算哈希值
            hash_value = self.calculate_hash(input_string)
            # 返回哈希值的JSON响应
            return JSONResponse(
                json.dumps({'hash': hash_value}),
                status_code=200
            )
        except ValueError as e:
            # 返回错误信息的JSON响应
            return JSONResponse(
                json.dumps({'error': str(e)}),
                status_code=400
# FIXME: 处理边界情况
            )

# 创建Starlette应用
app = Starlette(debug=True)

# 定义路由
app.add_route('/get_hash', HashCalculator().get_hash, methods=['GET'])
