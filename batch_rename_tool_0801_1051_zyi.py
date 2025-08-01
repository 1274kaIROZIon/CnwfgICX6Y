# 代码生成时间: 2025-08-01 10:51:51
import os
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.requests import Request
import re

class BatchRenameTool:
    """批量文件重命名工具。"""
    def __init__(self, directory):
        self.directory = directory

    def rename_files(self, pattern, replacement):
        """根据给定的模式和替换文本批量重命名文件。

        Args:
            pattern (str): 匹配文件名的正则表达式模式。
            replacement (str): 用于替换匹配到的文本的字符串。

        Returns:
            list: 重命名操作的结果列表。
        """
        results = []
        for filename in os.listdir(self.directory):
            if re.search(pattern, filename):
                new_name = re.sub(pattern, replacement, filename)
                original_path = os.path.join(self.directory, filename)
                new_path = os.path.join(self.directory, new_name)
                try:
                    os.rename(original_path, new_path)
                    results.append({"original": filename, "new": new_name})
                except OSError as e:
                    results.append({"original": filename, "error": str(e)})
        return results

async def rename_files_endpoint(request: Request):
    "