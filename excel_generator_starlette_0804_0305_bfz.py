# 代码生成时间: 2025-08-04 03:05:31
import os
from pathlib import Path
from datetime import datetime
from starlette.applications import Starlette
from starlette.responses import JSONResponse, FileResponse
from starlette.routing import Route
from openpyxl import Workbook
from openpyxl.utils.exceptions import InvalidFileError
from openpyxl.utils.dataframe import dataframe_to_rows
from pandas import DataFrame

class ExcelGeneratorApp(Starlette):
    def __init__(self):
        super().__init__(
            routes=[
                Route("/generate", self.generate_excel),
                Route("/download/{filename}", self.download_excel),
            ]
        )

    # Handler for generating Excel file
    async def generate_excel(self, request):
        """
        Generates an Excel file with sample data.

        Args:
            request (Request): The incoming request.

        Returns:
            JSONResponse: A JSON response with the filename of the generated Excel file.
        """
        try:
            # Generate a sample data frame
            data = {"Date": [datetime.now()], "Value": [1234]}
            df = DataFrame(data)

            # Create a new Excel workbook
            wb = Workbook()
            ws = wb.active

            # Fill the workbook with data from the data frame
            for r in dataframe_to_rows(df, index=False, header=True):
                ws.append(r)

            # Save the workbook to a temporary file
            temp_dir = Path("/tmp")
            temp_dir.mkdir(exist_ok=True)
            filename = "sample_excel_" + datetime.now().strftime("%Y%m%d%H%M%S") + ".xlsx"
            file_path = temp_dir / filename
            wb.save(file_path)

            # Return the filename of the generated Excel file
            return JSONResponse(content={"filename": str(file_path)})
        except Exception as e:
            return JSONResponse(content={"error": str(e)}, status_code=500)

    # Handler for downloading Excel file
    async def download_excel(self, request, filename):
        """
        Allows downloading of the previously generated Excel file.

        Args:
            request (Request): The incoming request.
            filename (str): The filename of the Excel file to download.

        Returns:
            FileResponse: A file response to trigger the download of the Excel file.
        """
        try:
            # Construct the full file path
            file_path = Path("/tmp") / filename

            # Check if the file exists
            if file_path.exists():
                return FileResponse(path=str(file_path), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            else:
                return JSONResponse(content={"error": "File not found"}, status_code=404)
        except InvalidFileError:
            # Handle the case where the file is not a valid Excel file
            return JSONResponse(content={"error": "Invalid file format"}, status_code=400)
        except Exception as e:
            return JSONResponse(content={"error": str(e)}, status_code=500)

# Entry point for the application
if __name__ == 