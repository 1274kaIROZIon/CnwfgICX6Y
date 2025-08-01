# 代码生成时间: 2025-08-02 06:58:48
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.exceptions import HTTPException

# 排序算法实现
class SortingService:
    def __init__(self, data):
        """
        初始化排序服务，接收一个列表作为待排序的数据。
        :param data: 待排序的数据列表
        """
        self.data = data

    def bubble_sort(self):
        """
        冒泡排序算法实现。
        """
        n = len(self.data)
        for i in range(n):
            for j in range(0, n - i - 1):
                if self.data[j] > self.data[j + 1]:
                    self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]
        return self.data

    def insertion_sort(self):
        """
        插入排序算法实现。
        """
        for i in range(1, len(self.data)):
            key = self.data[i]
            j = i - 1
            while j >= 0 and key < self.data[j]:
                self.data[j + 1] = self.data[j]
                j -= 1
            self.data[j + 1] = key
        return self.data

    def selection_sort(self):
        """
        选择排序算法实现。
        """
        for i in range(len(self.data)):
            min_idx = i
            for j in range(i + 1, len(self.data)):
                if self.data[min_idx] > self.data[j]:
                    min_idx = j
            self.data[i], self.data[min_idx] = self.data[min_idx], self.data[i]
        return self.data

# API路由和处理函数
def sort_api(request):
    """
    排序API处理函数，接收一个JSON请求体，包含待排序的数据列表。
    """
    try:
        data = request.json().get('data')
        if not data:
            raise ValueError("Request body must contain 'data' key with a list value.")
        sorting_service = SortingService(data)
        result = sorting_service.bubble_sort()  # 假设使用冒泡排序
        return JSONResponse(content={'sorted_data': result}, status_code=200)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 创建Starlette应用
app = Starlette(debug=True)

# 添加路由
app.add_route('/api/sort', sort_api, methods=['POST'])