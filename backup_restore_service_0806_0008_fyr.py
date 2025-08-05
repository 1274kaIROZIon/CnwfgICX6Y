# 代码生成时间: 2025-08-06 00:08:55
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_200_OK, HTTP_500_INTERNAL_SERVER_ERROR
import shutil
import os
import tarfile
import tempfile
import logging


# 设置日志记录
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BackupRestoreService:
    def __init__(self, data_dir):
        self.data_dir = data_dir

    def backup(self, backup_path):
        """
        创建数据备份
        :param backup_path: 备份文件的保存路径
        :return: 备份文件路径或错误信息
        """
        try:
            # 创建临时目录用于打包数据
            with tempfile.TemporaryDirectory() as tmp_dir:
                # 创建tar文件
                with tarfile.open(os.path.join(tmp_dir, 'data_backup.tar.gz'), 'w:gz') as tar:
                    # 将数据目录添加到tar文件中
                    for root, dirs, files in os.walk(self.data_dir):
                        for file in files:
                            file_path = os.path.join(root, file)
                            tar.add(file_path, arcname=os.path.relpath(file_path, start=self.data_dir))

                # 将tar文件移动到备份路径
                shutil.move(os.path.join(tmp_dir, 'data_backup.tar.gz'), backup_path)

            return {'message': 'Backup created successfully', 'backup_path': backup_path}
        except Exception as e:
            logger.error(f'Error creating backup: {e}')
            return {'error': str(e)}

    def restore(self, backup_path):
        """
        从备份文件恢复数据
        :param backup_path: 备份文件的路径
        :return: 恢复成功或错误信息
        """
        try:
            # 检查备份文件是否存在
            if not os.path.exists(backup_path):
                return {'error': f'Backup file {backup_path} does not exist'}

            with tarfile.open(backup_path, 'r:gz') as tar:
                # 解压tar文件到数据目录
                tar.extractall(self.data_dir)

            return {'message': 'Data restored successfully'}
        except Exception as e:
            logger.error(f'Error restoring data: {e}')
            return {'error': str(e)}


# 创建Starlette应用
app = Starlette(debug=True)

# 添加路由
app.add_route('/backup', lambda request: JSONResponse(BackupRestoreService(request.scope.get('path')).backup(request.body)), methods=['POST'])
app.add_route('/restore', lambda request: JSONResponse(BackupRestoreService(request.scope.get('path')).restore(request.body)), methods=['POST'])

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)
