# 代码生成时间: 2025-10-02 02:14:24
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST
from starlette.routing import Route

import json

# 模拟身份验证数据
IDENTITY_VERIFICATION_DATA = {
    "John Doe": {
        "date_of_birth": "1990-01-01",
        "national_id": "1234567890"
    },
    "Jane Smith": {
        "date_of_birth": "1995-06-15",
        "national_id": "9876543210"
    }
}

# KYC验证函数
def kyc_verify(name: str, dob: str, national_id: str) -> dict:
    """
    验证给定的身份信息是否与存储的数据匹配。
    
    参数:
    name (str): 被验证人的姓名。
    dob (str): 被验证人的出生日期。
    national_id (str): 被验证人的国家身份证号码。
    
    返回:
    dict: 验证结果。
    """
    identity_data = IDENTITY_VERIFICATION_DATA.get(name)
    if identity_data and identity_data['date_of_birth'] == dob and identity_data['national_id'] == national_id:
        return {"status": "success", "message": "KYC verification successful."}
    else:
        return {"status": "error", "message": "KYC verification failed."}

# API路由
routes = [
    Route("/kyc", endpoint=kyc_verify_endpoint, methods=["POST\]),
]

# API端点处理函数
async def kyc_verify_endpoint(request):
    """
    处理KYC验证请求。
    """
    try:
        data = await request.json()
        name = data.get("name")
        dob = data.get("date_of_birth")
        national_id = data.get("national_id")
        
        if not all([name, dob, national_id]):
            return JSONResponse(
                content={"status": "error", "message": "Missing data."},
                status_code=HTTP_400_BAD_REQUEST
            )
        result = kyc_verify(name, dob, national_id)
        return JSONResponse(content=result)
    except json.JSONDecodeError:
        return JSONResponse(
            content={"status": "error", "message": "Invalid JSON."},
            status_code=HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=HTTP_400_BAD_REQUEST
        )

# 创建Starlette应用
app = Starlette(debug=True, routes=routes)

# 运行应用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)