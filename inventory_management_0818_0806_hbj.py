# 代码生成时间: 2025-08-18 08:06:30
# inventory_management.py

# 引入starlette库
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import List, Dict
import uuid

# 定义库存项的数据结构
class InventoryItem:
    def __init__(self, name: str, quantity: int):
        self.id = str(uuid.uuid4())  # 唯一标识符
        self.name = name
        self.quantity = quantity

# 库存管理系统
class InventoryManagement:
    def __init__(self):
        self.items: Dict[str, InventoryItem] = {}

    def add_item(self, name: str, quantity: int) -> InventoryItem:
        if name in self.items:
            raise ValueError(f'Item {name} already exists.')
        new_item = InventoryItem(name, quantity)
        self.items[new_item.id] = new_item
        return new_item

    def get_item(self, item_id: str) -> InventoryItem:
        if item_id not in self.items:
            raise ValueError(f'Item with ID {item_id} not found.')
        return self.items[item_id]

    def update_item(self, item_id: str, quantity: int) -> InventoryItem:
        if item_id not in self.items:
            raise ValueError(f'Item with ID {item_id} not found.')
        self.items[item_id].quantity = quantity
        return self.items[item_id]

    def delete_item(self, item_id: str) -> bool:
        if item_id in self.items:
            del self.items[item_id]
            return True
        return False

# 路由和端点处理
def add_inventory_item(request):
    # 解析请求体
    data = request.json()
    name = data.get('name')
    quantity = data.get('quantity')
    
    # 实例化库存管理系统
    inventory = InventoryManagement()
    try:
        new_item = inventory.add_item(name, quantity)
        return JSONResponse(content={'item': {'id': new_item.id, 'name': new_item.name, 'quantity': new_item.quantity}}, status_code=201)
    except ValueError as e:
        raise StarletteHTTPException(status_code=400, detail=str(e))

def get_inventory_item(request, item_id: str):
    inventory = InventoryManagement()
    try:
        return JSONResponse(content={'item': {'id': inventory.get_item(item_id).id, 'name': inventory.get_item(item_id).name, 'quantity': inventory.get_item(item_id).quantity}}, status_code=200)
    except ValueError as e:
        raise StarletteHTTPException(status_code=404, detail=str(e))

def update_inventory_item(request, item_id: str):
    data = request.json()
    quantity = data.get('quantity')
    inventory = InventoryManagement()
    try:
        updated_item = inventory.update_item(item_id, quantity)
        return JSONResponse(content={'item': {'id': updated_item.id, 'name': updated_item.name, 'quantity': updated_item.quantity}}, status_code=200)
    except ValueError as e:
        raise StarletteHTTPException(status_code=404, detail=str(e))

def delete_inventory_item(request, item_id: str):
    inventory = InventoryManagement()
    try:
        success = inventory.delete_item(item_id)
        return JSONResponse(content={'message': 'Item deleted successfully' if success else 'Item not found'}, status_code=200)
    except ValueError as e:
        raise StarletteHTTPException(status_code=404, detail=str(e))

# 创建Starlette应用
app = Starlette(debug=True)

# 定义路由
app.add_route('POST', '/inventory', add_inventory_item)
app.add_route('GET', '/inventory/{item_id}', get_inventory_item)
app.add_route('PUT', '/inventory/{item_id}', update_inventory_item)
app.add_route('DELETE', '/inventory/{item_id}', delete_inventory_item)

# 错误处理
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return JSONResponse({'detail': str(exc)}, status_code=400)

# 启动应用
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)