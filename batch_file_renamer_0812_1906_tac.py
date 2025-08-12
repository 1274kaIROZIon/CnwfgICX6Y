# 代码生成时间: 2025-08-12 19:06:59
import os
from pathlib import Path
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.requests import Request

# 定义批量文件重命名工具的类
class BatchFileRenamer:
    def __init__(self, directory):
        """构造函数，初始化目录路径"""
        self.directory = directory

    def rename_files(self, pattern, replacement):
        """根据给定的模式和替换字符串重命名文件"""
        for file_path in Path(self.directory).glob(pattern):
            try:
                old_name = str(file_path)
                new_name = old_name.replace(pattern, replacement)
                os.rename(old_name, new_name)
                print(f"Renamed '{old_name}' to '{new_name}'")
            except Exception as e:
                print(f"Error renaming '{old_name}' to '{new_name}': {e}")

# 创建一个Starlette应用
app = Starlette(
    routes=[
        Route("/rename", endpoint=rename_files_endpoint, methods=["POST"]),
    ],
)

async def rename_files_endpoint(request: Request):
    "