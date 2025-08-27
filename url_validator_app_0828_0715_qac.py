# 代码生成时间: 2025-08-28 07:15:40
import starlette.applications  # 导入Starlette应用基类
from starlette.responses import JSONResponse  # 导入Starlette JSON响应类
from starlette.routing import Route  # 导入Starlette路由类
from urllib.parse import urlparse  # 导入URL解析模块
from validator_collection import check, validators  # 导入验证器集合库

# 创建Starlette应用
app = starlette.applications Starlette()

# 定义路由与对应的处理函数
routes = [
    Route('/', 'get', endpoint=get_valid_url)  # 定义根路径的GET请求处理函数
]

# 处理函数，接收URL并验证其有效性
async def get_valid_url(request):
    url = request.query_params.get('url')  # 从请求的查询参数中获取URL
    if not url:
        return JSONResponse({'error': 'Please provide a URL.'}, status_code=400)  # 如果没有URL，返回400错误

    try:
        # 使用validator_collection库验证URL
        is_valid = validators.url(url)
    except:
        return JSONResponse({'error': 'Invalid URL provided.'}, status_code=400)  # 如果URL无效，返回400错误

    # 构建响应数据
    response_data = {
        'url': url,
        'is_valid': is_valid
    }
    return JSONResponse(response_data)  # 返回JSON响应

# 配置应用的路由
app.add_routes(routes)

# 如果是直接运行这个模块，则启动Starlette应用
if __name__ == '__main__':
    import uvicorn  # 导入Uvicorn ASGI服务器
    uvicorn.run(app, host='0.0.0.0', port=8000)  # 在8000端口启动应用
