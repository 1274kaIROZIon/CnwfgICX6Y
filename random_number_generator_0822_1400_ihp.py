# 代码生成时间: 2025-08-22 14:00:03
import random
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route

# 定义一个异常类，用于处理请求参数错误
class InvalidParamsException(Exception):
    pass

# 定义生成随机数的函数
def generate_random_number(min_value: int, max_value: int) -> int:
    """
    生成一个介于min_value和max_value之间的随机整数。
    
    :param min_value: 随机数的最小值
    :param max_value: 随机数的最大值
    :return: 随机生成的整数
    """
    if min_value >= max_value:
        raise InvalidParamsException("min_value must be less than max_value")
    return random.randint(min_value, max_value)

# 定义一个路由处理函数，用于生成随机数
async def random_number_endpoint(request):
    """
    处理生成随机数的请求。
    
    :param request: 请求对象
    :return: 包含随机数的JSON响应
    """
    try:
        # 从请求中获取参数
        params = request.query_params
        min_value = int(params.get("min", 0))
        max_value = int(params.get("max", 100))
        
        # 生成随机数
        random_number = generate_random_number(min_value, max_value)
        
        # 返回随机数的JSON响应
        return JSONResponse({"random_number": random_number})
    except InvalidParamsException as e:
        # 参数错误时返回错误信息的JSON响应
        return JSONResponse({"error": str(e)}, status_code=400)
    except ValueError:
        # 处理参数转换错误
        return JSONResponse({"error": "Invalid input type for min or max."}, status_code=400)

# 创建Starlette应用
app = Starlette(debug=True, routes=[
    Route("/random", random_number_endpoint),
])

# 应用的启动点
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)