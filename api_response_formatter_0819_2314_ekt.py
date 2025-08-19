# 代码生成时间: 2025-08-19 23:14:45
import starlette.responses
import starlette.status
from typing import Any, Dict

# API响应格式化工具
class ApiResponseFormatter:
    def __init__(self):
        # 初始化响应格式器
        pass

    def format_response(self, data: Any, status_code: int = starlette.status.HTTP_200_OK) -> starlette.responses.Response:
        """
        格式化响应数据为JSON并返回。
        :param data: 要返回的数据
        :param status_code: HTTP状态码，默认为200
        :return: 格式化后的响应对象
        """
        # 构建响应内容
        response_data = {"code": status_code, "message": "success", "data": data}

        # 返回响应
        return starlette.responses.JSONResponse(response_data, status_code)

    def error_response(self, error_message: str, status_code: int) -> starlette.responses.Response:
        """
        格式化错误响应并返回。
        :param error_message: 错误信息
        :param status_code: HTTP状态码
        :return: 格式化后的错误响应对象
        """
        # 构建错误响应内容
        response_data = {"code": status_code, "message": error_message, "data": None}

        # 返回错误响应
        return starlette.responses.JSONResponse(response_data, status_code)

# 示例用法
if __name__ == "__main__":
    formatter = ApiResponseFormatter()

    # 成功响应示例
    success_response = formatter.format_response({"result": "成功"})
    print(success_response.json())

    # 错误响应示例
    error_response = formatter.error_response("发生错误", starlette.status.HTTP_400_BAD_REQUEST)
    print(error_response.json())