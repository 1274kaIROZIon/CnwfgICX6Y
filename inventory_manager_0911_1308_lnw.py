# 代码生成时间: 2025-09-11 13:08:18
import starlette.routing
import starlette.responses
import starlette.requests
import uvicorn
from starlette import status
from typing import Any, Dict, List
from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware

# 模拟数据库，实际应用中应替换为数据库操作
class InventoryDatabase:
    def __init__(self):
        self.items = {}

    def set_item(self, item_id: str, quantity: int):
        self.items[item_id] = quantity

    def get_item(self, item_id: str):
        return self.items.get(item_id, None)

    def update_item(self, item_id: str, quantity: int):
        if item_id in self.items:
            self.items[item_id] += quantity
            return True
        return False

    def delete_item(self, item_id: str):
        if item_id in self.items:
            del self.items[item_id]
            return True
        return False

# 库存管理器
class InventoryManager:
    def __init__(self):
        self.db = InventoryDatabase()

    def add_item(self, item_id: str, quantity: int):
        self.db.set_item(item_id, quantity)
        return {'item_id': item_id, 'quantity': quantity}

    def get_item_info(self, item_id: str):
        item_quantity = self.db.get_item(item_id)
        if item_quantity is not None:
            return {'item_id': item_id, 'quantity': item_quantity}
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Item {item_id} not found")

    def update_item_quantity(self, item_id: str, quantity: int):
        if self.db.update_item(item_id, quantity):
            return {'item_id': item_id, 'quantity': self.db.get_item(item_id)}
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Item {item_id} not found")

    def delete_item(self, item_id: str):
        if self.db.delete_item(item_id):
            return {'item_id': item_id, 'message': 'Item deleted'}
        else:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Item {item_id} not found")

# Starlette路由
routes = [
    starlette.routing.Route('/', endpoint=lambda request: starlette.responses.JSONResponse({'message': 'Inventory Manager API'} )),
    starlette.routing.Route('/add/{item_id}/{quantity}', endpoint=InventoryManager().add_item, methods=['POST']),
    starlette.routing.Route('/get/{item_id}', endpoint=InventoryManager().get_item_info, methods=['GET']),
    starlette.routing.Route('/update/{item_id}/{quantity}', endpoint=InventoryManager().update_item_quantity, methods=['POST']),
    starlette.routing.Route('/delete/{item_id}', endpoint=InventoryManager().delete_item, methods=['DELETE']),
]

# 启动Uvicorn服务器
if __name__ == '__main__':
    uvicorn.run(
        'inventory_manager:app',
        host='0.0.0.0',
        port=8000,
        reload=True,
    )

# 定义异常类
class HTTPException(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail

# 异常处理器
async def http_exception_middleware(request: starlette.requests.Request, call_next):
    try:
        response = await call_next(request)
    except HTTPException as exc:
        return starlette.responses.JSONResponse(
            status_code=exc.status_code,
            content={'detail': exc.detail}
        )
    return response

# 添加异常处理器
middleware = [
    Middleware(http_exception_middleware, dispatch=starlette.middleware.ASGIAppDispatchFunc),
]

# 应用
app = starlette.applications.Starlette(
    routes=routes,
    middleware=middleware,
)
