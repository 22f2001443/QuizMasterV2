from controller.routes.auth import Login, Register
from controller.routes.user import UserProfile

def register_routes(api):
    api.add_resource(Login, '/api/auth/login')
    api.add_resource(Register, '/api/auth/register')
    api.add_resource(UserProfile, '/api/user/profile')