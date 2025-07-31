# 代码生成时间: 2025-08-01 06:33:22
import starlette.applications
import starlette.responses
import starlette.routing
import starlette.requests
import starlette.exceptions

"""
A responsive design application using Starlette framework.
This application demonstrates a simple responsive design with a
single endpoint that changes its output based on the request's
user-agent string.
"""

# Define a simple application that uses Starlette's routing
class ResponsiveDesignApp(starlette.applications.Starlette):
    def __init__(self):
        # Initialize the Starlette application with a route
        super().__init__(
            debug=True,  # Enable debug mode for development
            routes=[
                starlette.routing.Route(
                    path='/',
                    endpoint=self.home,
                    methods=['GET']
                )
            ]
        )

    # Define the home route handler
    async def home(self, request: starlette.requests.Request):
        # Check the user-agent to determine the type of device
        user_agent = request.headers.get('User-Agent', '')
        if 'Mobile' in user_agent or 'Android' in user_agent or 'iPhone' in user_agent:
            # Return a mobile-friendly response
            return starlette.responses.HTMLResponse(
                template=f"""
                <html>
                <head>
                    <title>Responsive Design - Mobile</title>
                </head>
                <body>
                    <h1>Welcome to the Mobile Version</h1>
                    <!-- Mobile-friendly content here -->
                </body>
                </html>
                """)
        )
        else:
            # Return a desktop-friendly response
            return starlette.responses.HTMLResponse(
                template=f"""
                <html>
                <head>
                    <title>Responsive Design - Desktop</title>
                </head>
                <body>
                    <h1>Welcome to the Desktop Version</h1>
                    <!-- Desktop-friendly content here -->
                </body>
                </html>
                """)
        )

# Create an instance of the application and run it
if __name__ == '__main__':
    app = ResponsiveDesignApp()
    app.run(host='0.0.0.0', port=8000)
