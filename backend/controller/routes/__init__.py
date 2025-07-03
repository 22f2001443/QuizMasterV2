from controller.routes.auth import Register, Login, Logout #, ResetPassword
from controller.routes.user import UserProfile

def register_routes(api):
    # Routes for authentication [from controller.routes.auth import Register, Login, Logout, ResetPassword]
    api.add_resource(Login, '/api/auth/login')
    api.add_resource(Register, '/api/auth/register')
    api.add_resource(Logout, '/api/auth/logout')
    # api.add_resource(ResetPassword, '/api/auth/reset')

    # Routes for user profile [from controller.routes.user import UserProfile]
    api.add_resource(UserProfile, '/api/user/profile')