# 代码生成时间: 2025-09-10 04:05:21
import os
import shutil
from pathlib import Path
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route


class FolderOrganizer:
    def __init__(self, source_dir: str, destination_dir: str):
        """
        初始化文件夹整理器
        :param source_dir: 需要整理的文件夹路径
        :param destination_dir: 整理后的文件夹路径
        """
        self.source_dir = Path(source_dir)
        self.destination_dir = Path(destination_dir)

    def organize(self):
        """
        对文件夹进行整理，将文件按照类型移动到指定文件夹
        """
        for file in self.source_dir.iterdir():
            if file.is_file():
                self.move_file(file)
        print("Folder organization completed.")

    def move_file(self, file: Path):
        """
        将单个文件根据扩展名移动到指定文件夹
        :param file: 需要移动的文件
        """
        extension = file.suffix
        if extension:
            destination_folder = self.destination_dir / extension[1:]  # 去掉点
            destination_folder.mkdir(exist_ok=True)
            shutil.move(str(file), str(destination_folder / file.name))
        else:
            print(f"No extension found for {file.name}. Skipping...")


class FolderOrganizerApp(Starlette):
    def __init__(self):
        super().__init__(
            routes=[
                Route("/organize", FolderOrganizerEndpoint, name="organize_folder")
            ]
        )


class FolderOrganizerEndpoint:
    def __init__(self):
        self.organizer = FolderOrganizer(
            source_dir="./source",
            destination_dir="./destination"
        )

    async def __call__(self, request):
        try:
            self.organizer.organize()
            return JSONResponse(
                content={"message": "Folder organized successfully."},
                status_code=200
            )
        except Exception as e:
            return JSONResponse(
                content={"error": str(e)},
                status_code=500
            )
