# 代码生成时间: 2025-08-04 06:40:59
import os
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route, Mount
from starlette.staticfiles import StaticFiles
from openpyxl import Workbook
from openpyxl.utils.exceptions import InvalidFileException
import uvicorn

# 定义生成Excel文件的函数
def generate_excel(sheet_name, data):
    """Generate an Excel file with the given sheet name and data.

    Args:
        sheet_name (str): The name of the sheet.
        data (list of list): 2D list containing data to fill in the Excel sheet.

    Returns:
        str: The path to the generated Excel file.
    """
    try:
        # 创建一个新的Workbook对象
        wb = Workbook()
        # 添加一个工作表
        ws = wb.active
        ws.title = sheet_name
        # 填充数据
        for row in data:
            ws.append(row)
        # 保存Workbook
        file_path = f'./{sheet_name}.xlsx'
        wb.save(file_path)
        return file_path
    except Exception as e:
        # 处理异常情况
        return str(e)

# 创建Starlette应用
app = Starlette()

# 定义路由和处理函数
@app.route("/generate", methods=["POST"])
async def generate_excel_endpoint(request):
    """Endpoint to generate an Excel file.

    Args:
        request (Request): The incoming request.

    Returns:
        JSONResponse: Response with the path to the generated Excel file.
    """
    try:
        # 获取请求数据
        data = await request.json()
        # 提取sheet名称和数据
        sheet_name = data.get("sheet_name", "Sheet")
        data_rows = data.get("data", [])
        # 生成Excel文件
        file_path = generate_excel(sheet_name, data_rows)
        # 返回文件路径
        return JSONResponse(content={"file_path": file_path})
    except InvalidFileException as e:
        # 处理无效文件异常
        return JSONResponse(content={"error": str(e)}, status_code=400)
    except Exception as e:
        # 处理其他异常
        return JSONResponse(content={"error": str(e)}, status_code=500)

# 定义静态文件路由
app.mount("/static", StaticFiles(directory="static"))

# 运行应用
if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)