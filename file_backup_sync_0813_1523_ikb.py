# 代码生成时间: 2025-08-13 15:23:01
import os
import shutil
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route


class FileBackupSync:
    def __init__(self, source_dir, target_dir):
        self.source_dir = source_dir
        self.target_dir = target_dir
        os.makedirs(target_dir, exist_ok=True)

    def backup_files(self):
        """备份文件到目标目录"""
        for filename in os.listdir(self.source_dir):
            file_path = os.path.join(self.source_dir, filename)
            if os.path.isfile(file_path):
                shutil.copy2(file_path, self.target_dir)
                print(f"文件 {filename} 已备份到 {self.target_dir}")
        return True

    def sync_directories(self):
        """同步源目录和目标目录，删除目标目录中的多余文件"""
        for filename in os.listdir(self.target_dir):
            file_path = os.path.join(self.target_dir, filename)
            source_path = os.path.join(self.source_dir, filename)
            if not os.path.exists(source_path):
                os.remove(file_path)
                print(f"文件 {filename} 在目标目录中已删除")
        return True


async def backup_sync_endpoint(request):
    """Starlette API端点，用于触发文件备份和同步"""
    backup_sync_tool = FileBackupSync(request.query_params['source'], request.query_params['target'])
    try:
        backup_sync_tool.backup_files()
        backup_sync_tool.sync_directories()
        return JSONResponse({'message': '备份和同步成功'}, status_code=200)
    except Exception as e:
        return JSONResponse({'error': str(e)}, status_code=500)


app = Starlette(debug=True, routes=[
    Route('/backup-sync', endpoint=backup_sync_endpoint)
])

if __name__ == '__main__':
    print("文件备份和同步工具启动中...")
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
