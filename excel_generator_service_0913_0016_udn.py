# 代码生成时间: 2025-09-13 00:16:44
import os
from fastapi import FastAPI, HTTPException, File, UploadFile
from starlette.responses import JSONResponse
from openpyxl import Workbook
from typing import List

# 应用初始化
app = FastAPI()

# Excel表格自动生成器服务
@app.post("/generate_excel/")
async def generate_excel(file_data: List[dict] = [], sheet_title: str = "Sheet1"):
    # 检查输入数据
    if not file_data:
        raise HTTPException(status_code=400, detail="No data provided")

    try:
        # 创建Workbook对象
        wb = Workbook()
        ws = wb.active
        ws.title = sheet_title

        # 如果提供了数据，则创建Excel表格
        if file_data:
            # 写入标题行（假设每个字典的键为列名）
            ws.append(list(file_data[0].keys()))
            # 写入数据行
            for row_data in file_data:
                ws.append(list(row_data.values()))

        # 保存Workbook到临时文件
        temp_excel_file = "temp_excel_file.xlsx"
        wb.save(temp_excel_file)

        # 读取临时文件并返回
        with open(temp_excel_file, "rb") as f:
            excel_file = f.read()

        # 删除临时文件
        os.remove(temp_excel_file)

        return JSONResponse(content={"filename": temp_excel_file, "file": excel_file.hex()}, media_type="application/json")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 错误处理器
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )
