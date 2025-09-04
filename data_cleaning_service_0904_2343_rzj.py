# 代码生成时间: 2025-09-04 23:43:25
import pandas as pd
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.exceptions import HTTPException as StarletteHTTPException


# 数据清洗和预处理工具类
class DataCleaningService:
    def __init__(self):
        """初始化数据清洗服务"""
        pass

    def clean_data(self, df):
        """
        对给定的DataFrame进行数据清洗和预处理。
        :param df: pandas DataFrame
        :return: 清洗后的DataFrame
        """
        try:
            # 移除空值
            df = df.dropna()

            # 转换数据类型
            df = self.convert_data_types(df)

            # 填充空值
            df = self.fill_missing_values(df)

            return df
        except Exception as e:
            raise StarletteHTTPException(status_code=500, detail=str(e))

    def convert_data_types(self, df):
        """
        转换DataFrame中的数据类型。
        :param df: pandas DataFrame
        :return: 数据类型转换后的DataFrame
        """
        # 示例：将'age'列转换为整型
        df['age'] = df['age'].astype('int')

        return df

    def fill_missing_values(self, df):
        """
        填充DataFrame中的缺失值。
        :param df: pandas DataFrame
        :return: 缺失值填充后的DataFrame
        """
        # 示例：用平均值填充'age'列的空值
        df['age'] = df['age'].fillna(df['age'].mean())

        return df


# Starlette应用
class DataCleaningApp(Starlette):
    def __init__(self):
        super().__init__(
            routes=[
                Route("/clean", endpoint=DataCleaningHandler, methods=["POST"]),
            ]
        )


# 数据清洗请求处理器
class DataCleaningHandler:
    def __init__(self):
        self.service = DataCleaningService()

    async def __call__(self, request):
        try:
            # 解析请求体中的DataFrame
            data = await request.json()
            df = pd.DataFrame(data)

            # 清洗数据
            cleaned_df = self.service.clean_data(df)

            # 返回清洗后的数据
            return JSONResponse(content=cleaned_df.to_dict(orient='records'))
        except Exception as e:
            raise StarletteHTTPException(status_code=400, detail=str(e))


# 运行应用
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(DataCleaningApp(), host="0.0.0.0", port=8000)