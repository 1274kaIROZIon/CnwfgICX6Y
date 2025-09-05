# 代码生成时间: 2025-09-05 20:53:28
import starlette.responses
from starlette.routing import Route
from starlette.applications import Starlette
from starlette.exceptions import HTTPException as StarletteHTTPException

# 排序算法模块
class SortingAlgorithm:
    def __init__(self, data):
        """
        初始化排序算法类
        :param data: 待排序的数据列表
        """
        self.data = data

    def bubble_sort(self):
        """
        冒泡排序算法实现
        :return: 排序后的列表
        """
        n = len(self.data)
        for i in range(n):
            for j in range(0, n-i-1):
                if self.data[j] > self.data[j+1]:
                    self.data[j], self.data[j+1] = self.data[j+1], self.data[j]
        return self.data

    def selection_sort(self):
        """
        选择排序算法实现
        :return: 排序后的列表
        """
        n = len(self.data)
        for i in range(n):
            min_idx = i
            for j in range(i+1, n):
                if self.data[min_idx] > self.data[j]:
                    min_idx = j
            self.data[i], self.data[min_idx] = self.data[min_idx], self.data[i]
        return self.data

    def insertion_sort(self):
        """
        插入排序算法实现
        :return: 排序后的列表
        """
        for i in range(1, len(self.data)):
            key = self.data[i]
            j = i-1
            while j >= 0 and key < self.data[j]:
                self.data[j+1] = self.data[j]
                j -= 1
            self.data[j+1] = key
        return self.data

# API 路由和处理函数
async def sort_api(request):
    # 获取请求参数
    data = request.query_params.get('data')
    if not data:
        raise StarletteHTTPException(status_code=400, detail="Missing 'data' query parameter")

    # 将请求参数转换为列表
    try:
        data_list = [int(item.strip()) for item in data.split(',')]
    except ValueError:
        raise StarletteHTTPException(status_code=400, detail="Invalid 'data' format")

    # 初始化排序算法类并排序
    sorting_algorithm = SortingAlgorithm(data_list)
    sorted_data = sorting_algorithm.bubble_sort()  # 默认使用冒泡排序

    # 返回排序结果
    return starlette.responses.JSONResponse({"sorted_data": sorted_data})

# 路由列表
routes = [
    Route("/sort", sort_api, methods=["GET"]),
]

# 应用实例
app = Starlette(debug=True, routes=routes)
