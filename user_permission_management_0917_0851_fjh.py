# 代码生成时间: 2025-09-17 08:51:35
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.status import HTTP_404_NOT_FOUND, HTTP_200_OK
import uvicorn

"""
User Permission Management System using Starlette framework.
This system allows for managing user permissions through HTTP requests.
"""

class PermissionDenied(Exception):
    """Custom exception for permission denied errors."""
    pass

class UserPermissionManager:
    """Manages user permissions."""
    def __init__(self):
        self.permissions = {
            'admin': ['read', 'write', 'delete'],
            'user': ['read'],
        }

    def has_permission(self, user_role, action):
        """Check if a user has the given permission."""
        try:
            return action in self.permissions[user_role]
        except KeyError:
            raise PermissionDenied(f"User role '{user_role}' is not defined.")

    def add_permission(self, user_role, action):
        """Add a new permission to a user role."""
        if user_role not in self.permissions:
            self.permissions[user_role] = []
        self.permissions[user_role].append(action)

app = Starlette(debug=True)

# Route to check permission
@app.route('/check_permission/{user_role}/{action}', methods=['GET'])
async def check_permission(request):
    user_role = request.path_params['user_role']
    action = request.path_params['action']
    manager = UserPermissionManager()
    try:
        can_access = manager.has_permission(user_role, action)
        return JSONResponse({'can_access': can_access}, status_code=HTTP_200_OK)
    except PermissionDenied as e:
        return JSONResponse({'error': str(e)}, status_code=HTTP_403_FORBIDDEN)

# Route to add permission
@app.route('/add_permission/{user_role}/{action}', methods=['POST'])
async def add_permission(request):
    user_role = request.path_params['user_role']
    action = request.path_params['action']
    manager = UserPermissionManager()
    try:
        manager.add_permission(user_role, action)
        return JSONResponse({'success': 'Permission added'}, status_code=HTTP_200_OK)
    except PermissionDenied as e:
        return JSONResponse({'error': str(e)}, status_code=HTTP_403_FORBIDDEN)

if __name__ == '__main__':
    # Run the Starlette application
    uvicorn.run(app, host='0.0.0.0', port=8000)