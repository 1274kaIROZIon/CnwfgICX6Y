# 代码生成时间: 2025-09-16 20:27:56
import os
import shutil
from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.routing import Route
from starlette.staticfiles import StaticFiles
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from pathlib import Path
import logging


# 配置日志记录器
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FolderStructureOrganizer:
    def __init__(self, root_directory):
        self.root_directory = Path(root_directory)
        if not self.root_directory.exists():
            raise ValueError("The root directory does not exist.")

    def organize(self):
        """
        将根目录下的所有文件移动到以扩展名命名的子文件夹中
        """
        for item in self.root_directory.iterdir():
            if item.is_file():
                # 获取文件扩展名
                ext = item.suffix
                # 如果扩展名不存在，则创建文件夹
                if ext:
                    target_folder = self.root_directory / ext[1:]
                    target_folder.mkdir(exist_ok=True)
                    # 移动文件到相应的文件夹
                    shutil.move(str(item), str(target_folder / item.name))

    async def organize_async(self, request: Request):
        "