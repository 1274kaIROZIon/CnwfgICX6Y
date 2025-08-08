# 代码生成时间: 2025-08-09 05:17:23
import starlette.applications
import starlette.responses
import starlette.routing
import starlette.status
from starlette.requests import Request
import logging
from pathlib import Path
import re
from datetime import datetime

"""
日志文件解析工具
"""

# 设置日志配置
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 正则表达式用于匹配日志中的日期和时间
log_date_pattern = re.compile(r'\[(.*?)\]')

# 定义日志解析函数
def parse_log_line(line: str) -> dict:
    """
    解析单行日志并返回包含日期、时间和其他信息的字典。
    """
    match = log_date_pattern.search(line)
    if match:
        datetime_str = match.group(1)
        datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
        return {"datetime": datetime_obj, "message": line.replace(f'[{datetime_str}]', '').strip()}
    else:
        return {"datetime": None, "message": line}

# 创建Starlette应用
class LogParserApp(starlette.applications_STARLETTE.Application):
    def __init__(self):
        super().__init__(
            routes=[
                starlette.routing.Route(
                    handler=parse_log_file,
                    path="/parse",
                    methods=["POST"],
                ),
            ],
        )

    async def parse_log_file(self, request: Request) -> starlette.responses.Response:
        """
        处理POST请求，解析上传的日志文件。
        """
        try:
            # 从请求中获取日志文件
            file = await request.form()
            log_file = file.get('log_file')
            if not log_file:
                return starlette.responses.Response(
                    content="No log file provided.",
                    status_code=starlette.status.HTTP_400_BAD_REQUEST
                )

            # 读取日志文件内容
            log_content = await log_file.read()
            log_lines = log_content.decode('utf-8').splitlines()

            # 解析日志行
            parsed_logs = [parse_log_line(line) for line in log_lines]

            # 返回解析结果
            return starlette.responses.JSONResponse(parsed_logs)
        except Exception as e:
            logger.error(f'Error parsing log file: {e}')
            return starlette.responses.Response(
                content="Error parsing log file.",
                status_code=starlette.status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# 运行应用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(LogParserApp(), host='0.0.0.0', port=8000)