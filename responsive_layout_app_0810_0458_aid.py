# 代码生成时间: 2025-08-10 04:58:59
import starlette.applications
import starlette.responses
import starlette.routing
import starlette.requests

from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware

# 响应式布局配置
RESPONSIVE_CONFIG = {
    "small": "(max-width: 600px)",
    "medium": "(max-width: 1024px)",
    "large": "(max-width: 1200px)",
    "extra_large": "(max-width: 1920px)",
}

# 应用配置
app = starlette.applications Starlette()

# 添加中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware)
app.add_middleware(AuthenticationMiddleware)

# 路由配置
routes = [
    # 响应式布局的主页
    starlette.routing.Route("/", endpoint=home, methods=["GET"]),
]

# 将路由添加到应用
app.routes.extend(routes)

# 主页视图函数
async def home(request: starlette.requests.Request):
    """
    响应式布局的主页视图函数。
    
    返回一个HTML页面，根据设备的屏幕尺寸应用不同的样式。
    """
    # 获取屏幕尺寸
    width = request.client.host[0]
    
    # 应用响应式布局样式
    if width < 600:
        layout = "small"
    elif width < 1024:
        layout = "medium"
    elif width < 1200:
        layout = "large"
    else:
        layout = "extra_large"
    
    # 返回HTML响应
    return starlette.responses.HTMLResponse(
        f"""
        <!DOCTYPE html>
        <html lang="en">\        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Responsive Layout</title>
            <style>
                /* 响应式布局样式 */
                @media {small} {{
                    .container {{
                        max-width: 600px;
                    }}
                }}
                @media {medium} {{
                    .container {{
                        max-width: 1024px;
                    }}
                }}
                @media {large} {{
                    .container {{
                        max-width: 1200px;
                    }}
                }}
                @media {extra_large} {{
                    .container {{
                        max-width: 1920px;
                    }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Responsive Layout Example</h1>
                <p>This layout adapts to your screen size: {layout}</p>
            </div>
        </body>
        </html>
        """,
        media_type="text/html",
    )

# 启动应用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)