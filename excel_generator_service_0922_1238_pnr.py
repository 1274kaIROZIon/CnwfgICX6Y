# 代码生成时间: 2025-09-22 12:38:17
import csv
from starlette.applications import Starlette
from starlette.responses import FileResponse
from starlette.routing import Route
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR
import pandas as pd
from pathlib import Path

# 设置Excel文件生成器类
class ExcelGeneratorService:
    def __init__(self, data_source):
        self.data_source = data_source

    def generate_excel(self):
        """生成Excel文件"""
        try:
            # 使用Pandas将数据源转换为DataFrame
            df = pd.DataFrame(self.data_source)
            # 指定Excel文件路径
            excel_path = Path("output.xlsx")
            # 将DataFrame导出为Excel文件
            df.to_excel(excel_path, index=False)
            return str(excel_path)
        except Exception as e:
            raise Exception(f"Failed to generate Excel file: {str(e)}")

# 创建Starlette应用
app = Starlette(debug=True)

# 定义路由
@app.route("/generate-excel", methods=["GET", "POST"])
async def generate_excel_endpoint(request):
    """处理生成Excel文件的请求"""
    try:
        # 获取请求数据
        data_source = await request.json()
        # 创建Excel文件生成器实例
        excel_service = ExcelGeneratorService(data_source)
        # 生成Excel文件
        excel_path = excel_service.generate_excel()
        # 返回文件响应
        return FileResponse(path=excel_path, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception as e:
        # 错误处理
        return {'message': f'Error: {str(e)}'}, HTTP_500_INTERNAL_SERVER_ERROR

# 添加路由
routes = [
    Route("/generate-excel", generate_excel_endpoint)
]

# 将路由添加到Starlette应用
app.add_routes(routes)
