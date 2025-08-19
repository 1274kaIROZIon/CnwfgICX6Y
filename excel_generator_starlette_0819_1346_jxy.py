# 代码生成时间: 2025-08-19 13:46:18
import os
from starlette.applications import Starlette
from starlette.responses import JSONResponse, FileResponse
from starlette.routing import Route
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from pandas import DataFrame
import uvicorn

# ExcelGenerator 应用
class ExcelGenerator(Starlette):
    def __init__(self):
        super().__init__(
            routes=[
                Route("/generate", self.generate_excel),
            ]
        )

    # 处理生成 Excel 文件的请求
    async def generate_excel(self, request):
        # 接收 JSON 数据
        data = await request.json()

        # 检查数据是否有效
        if not data or 'data' not in data:
            return JSONResponse(
                content={"error": "Invalid request data."},
                status_code=400
            )

        try:
            # 将数据转换为 DataFrame
            df = DataFrame(data['data'])
            # 创建工作簿
            wb = Workbook()
            # 将 DataFrame 添加到工作簿
            ws = wb.active
            for r in dataframe_to_rows(df, index=False, header=True):
                ws.append(r)
            # 保存 Excel 文件
            wb.save('output.xlsx')
            # 返回文件响应
            return FileResponse('output.xlsx', media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        except Exception as e:
            # 错误处理
            return JSONResponse(
                content={"error": str(e)},
                status_code=500
            )

# 启动应用
if __name__ == '__main__':
    uvicorn.run(ExcelGenerator(), host='0.0.0.0', port=8000)

"""
ExcelGenerator 是一个 Starlette 应用，可以接收 JSON 数据并生成一个 Excel 文件。
它提供了一个 `/generate` 路由来处理生成 Excel 文件的请求。
请求应该包含一个 JSON 对象，其中包含一个数据数组。
应用会将这些数据转换为一个 pandas DataFrame，然后使用 openpyxl 库将其写入 Excel 文件。
如果请求数据无效或在处理过程中发生错误，应用会返回适当的错误响应。
"""