# 代码生成时间: 2025-09-12 14:30:12
import starlette.applications
import starlette.responses
import starlette.routing
import starlette.status
import requests
import urllib.parse

from starlette.exceptions import HTTPException

# 用于验证URL链接有效性的类
class URLValidator:
    def __init__(self, url):
        self.url = url

    # 检查URL是否有效
    def is_valid(self):
        parsed_url = urllib.parse.urlparse(self.url)
        # 检查是否有协议和主机名
        if not all([parsed_url.scheme, parsed_url.netloc]):
            return False
        try:
            # 使用requests库发送HEAD请求以验证URL
            response = requests.head(self.url)
            # 如果状态码为200或403，认为URL有效
            return response.status_code in (200, 403)
        except requests.RequestException:
            return False

# 创建一个Starlette应用
class URLValidationApp(starlette.applications.Starlette):
    def __init__(self):
        super().__init__(
            routes=[
                starlette.routing.Route(
                    handler=self.validate_url,
                    path='/validate',
                    methods=['POST'],
                ),
            ],
        )

    # URL验证的端点
    async def validate_url(self, request):
        # 从请求体中获取URL
        url_to_validate = await request.json()
        if 'url' not in url_to_validate:
            raise HTTPException(status_code=starlette.status.HTTP_400_BAD_REQUEST, detail='Missing URL in request')

        # 创建URLValidator实例并验证URL
        validator = URLValidator(url_to_validate['url'])
        is_valid = validator.is_valid()

        # 返回验证结果
        return starlette.responses.JSONResponse(
            content={'is_valid': is_valid},
            status_code=starlette.status.HTTP_200_OK,
        )

# 运行应用
if __name__ == '__main__':
    application = URLValidationApp()
    application.run(debug=True)