# 代码生成时间: 2025-08-05 05:01:44
import json
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
import os


# 配置文件管理器
class ConfigManager:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = {}
        self.load_config()

    def load_config(self):
        """
        加载配置文件
        """
        try:
            with open(self.config_file, 'r') as file:
                self.config = json.load(file)
        except FileNotFoundError:
            self.config = {}
        except json.JSONDecodeError as e:
            raise ValueError('配置文件格式错误') from e

    def get_config(self, key):
        """
        获取配置项
        """
        return self.config.get(key, None)

    def update_config(self, key, value):
        """
        更新配置项
        """
        self.config[key] = value
        with open(self.config_file, 'w') as file:
            json.dump(self.config, file, indent=4)

    def delete_config(self, key):
        """
        删除配置项
        """
        if key in self.config:
            del self.config[key]
            with open(self.config_file, 'w') as file:
                json.dump(self.config, file, indent=4)
        else:
            raise KeyError('配置项不存在')


# Starlette 应用
class ConfigManagerApp(Starlette):
    def __init__(self, config_file):
        super().__init__(routes=[
            Route('/config', ConfigManagerEndpoint(config_file), methods=['GET', 'POST', 'DELETE']),
            Route('/config/{key}', ConfigManagerEndpoint(config_file), methods=['GET', 'POST', 'DELETE'])
        ])


# Starlette 端点
class ConfigManagerEndpoint:
    def __init__(self, config_file):
        self.config_manager = ConfigManager(config_file)

    async def get(self, request, key=None):
        """
        获取配置
        """
        if key:
            value = self.config_manager.get_config(key)
            if value is None:
                raise StarletteHTTPException(status_code=HTTP_400_BAD_REQUEST, detail='配置项不存在')
            return JSONResponse({'key': key, 'value': value})
        else:
            config = self.config_manager.config
            return JSONResponse(config)

    async def post(self, request, key=None):
        """
        更新配置
        """
        if not key:
            raise StarletteHTTPException(status_code=HTTP_400_BAD_REQUEST, detail='缺少配置项')

        data = await request.json()
        if not isinstance(data, dict) or 'value' not in data:
            raise StarletteHTTPException(status_code=HTTP_400_BAD_REQUEST, detail='无效的请求体')

        try:
            self.config_manager.update_config(key, data['value'])
        except ValueError as e:
            raise StarletteHTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

        return JSONResponse({'key': key, 'value': data['value']})

    async def delete(self, request, key=None):
        """
        删除配置
        """
        if not key:
            raise StarletteHTTPException(status_code=HTTP_400_BAD_REQUEST, detail='缺少配置项')

        try:
            self.config_manager.delete_config(key)
        except KeyError as e:
            raise StarletteHTTPException(status_code=HTTP_400_BAD_REQUEST, detail=str(e))

        return JSONResponse({'detail': '配置项已删除'})


# 运行应用
if __name__ == '__main__':
    config_file = os.environ.get('CONFIG_FILE', 'config.json')
    app = ConfigManagerApp(config_file)
    app.run()