from flask_restful import Resource, reqparse
from werkzeug.security import check_password_hash, generate_password_hash
from flask import request, jsonify, make_response
from flask_security import Security, SQLAlchemyUserDatastore, utils as security_utils, auth_token_required
from datetime import datetime

from controller.models.user_model import User, Role
from controller.models import db
from controller.extensions import user_datastore
from controller.models.semester_model import Semester

# --- Request Parsers ---
register_parser = reqparse.RequestParser()
register_parser.add_argument('name', type=str, required=True, help='Name is required')
register_parser.add_argument('email', type=str, required=True, help='Email is required')
register_parser.add_argument('password', type=str, required=True, help='Password is required')
register_parser.add_argument('dob', type=str, required=False)  # format: 'YYYY-MM-DD'
register_parser.add_argument('semester_id', type=int, required=False)  # optional, or required=True

login_parser = reqparse.RequestParser()
login_parser.add_argument('email', type=str, required=True, help='Email is required')
login_parser.add_argument('password', type=str, required=True, help='Password is required')

# --- Resource: Register --- #working
class Register(Resource):
    def get(self):
        # Fetch all available semesters
        semesters = Semester.query.order_by(Semester.id).all()
        semester_options = [{"label": sem.name.value, "value": sem.id} for sem in semesters]

        # Optional DOB constraint range
        dob_min = "1990-01-01"
        dob_max = "2010-12-31"

        return jsonify({
            "type": "register",
            "fields": [
                { "name": "name", "label": "Name", "type": "text", "required": True },
                { "name": "email", "label": "Email", "type": "email", "required": True },
                { "name": "password", "label": "Password", "type": "password", "required": True },
                { "name": "dob", "label": "Date of Birth", "type": "date", "required": False },
                { "name": "semester_id", "label": "Semester", "type": "select", "required": True, "options": semester_options }
            ],
            "dob_min": dob_min,
            "dob_max": dob_max
        })

    def post(self):
        # Check if request is JSON
        if not request.is_json:
            result = {"message": "Request must be JSON"}
            return result, 400
        # Parse the JSON request
        args = register_parser.parse_args()
        name = args['name']
        email = args['email'].lower()  # Normalize email to lowercase
        password = args['password']
        dob_str = args.get('dob')
        semester_id = args.get('semester_id')
        # Validate semester_id if provided
        if semester_id is None:
            # If semester_id is not provided
            result = {'message': 'Semester ID is required'}
            return result, 400
        elif semester_id is not None:
            if not isinstance(semester_id, int) or semester_id <= 0:
                result = {'message': 'Invalid semester ID'}
                return result, 400
        # Parse the date of birth if provided
        dob = None
        if dob_str:
            try:
                dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
            except ValueError:
                result = {'message': 'DOB must be in YYYY-MM-DD format'}
                return result, 400

        user_datastore.user_model = User
        user_datastore.role_model = Role
        user_datastore.db = db
        user = user_datastore.find_user(email=email)

        # Check if user already exists
        if user:
            result = {'message': 'Email already registered'}
            return result, 409
        # Hash the password
        hashed_password = generate_password_hash(password)

        # Check if user role exists
        # Assuming 'user' role is required for all registered users
        user_role = Role.query.filter_by(name='user').first()
        if not user_role:
            result = {'message': 'User role not found'}
            return result, 404

        # Create new user
        new_user = User(name=name, email=email, password=hashed_password, roles=[user_role],semester_id=semester_id, dob=dob)
        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            result = {'message': 'Error creating user: ' + str(e)}
            return result, 500

        # Return success message
        result = {'message': 'User registered successfully', 'user': {'id': new_user.id, 'name': new_user.name, 'email': new_user.email, 'semester': new_user.semester.name.value}}
        return result, 200

# --- Resource: Login --- #working
class Login(Resource):
    def post(self):
        # Check if request is JSON
        if not request.is_json:
            result = {"message": "Request must be JSON"}
            return result, 400
        # Parse the JSON request
        args = login_parser.parse_args()
        email = args['email'].lower()
        password = args['password']

        # Initialize user_datastore with the models and db
        user_datastore.user_model = User
        user_datastore.role_model = Role
        user_datastore.db = db

        user = user_datastore.find_user(email=email)

        # Data Validation
        if not user or not check_password_hash(user.password, password):
            result = {'message': 'Invalid email or password'}
            return result, 401

        #print(user.fs_uniquifier)  # Should print a valid UUID
        #print(user.get_auth_token())  # Should no longer raise any error
        auth_token = user.get_auth_token()
        if not auth_token:
            result = {'message': 'Authentication token generation failed'}
            return result, 500

        security_utils.login_user(user)

        # Return success message with user details and auth token
        result = {
            'message': 'Login successful',
            'auth_token': auth_token,
            'user': {
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'roles': [role.name for role in user.roles]

            }
        }
        return result, 200
    
    def get(self):
        return jsonify({
            "type": "login",
            "fields": [
                {"name": "email", "label": "Email", "type": "email", "required": True},
                {"name": "password", "label": "Password", "type": "password", "required": True}
            ]
        })

# --- Resource: Logout --- #working
class Logout(Resource):
    @auth_token_required
    def post(self):
        security_utils.logout_user()
        result = {'message': 'Logout successful'}
        response = make_response(jsonify(result), 200)
        # Clear the session cookie
        response.delete_cookie('session')
        return response
    
# # --- Resource: Reset --- #working
# class ResetPassword(Resource):
#     def post(self):
#         # Check if request is JSON
#         if not request.is_json:
#             result = {"message": "Request must be JSON"}
#             return make_response(jsonify(result), 400)

#         # Parse the JSON request
#         args = reset_parser.parse_args()
#         email = args['email'].lower()
#         new_password = args['new_password']

#         # Initialize user_datastore with the models and db
#         user_datastore.user_model = User
#         user_datastore.role_model = Role
#         user_datastore.db = db

#         user = user_datastore.find_user(email=email)

#         # Data Validation
#         if not user:
#             result = {'message': 'User not found'}
#             return make_response(jsonify(result), 404)

#         # Hash the new password
#         hashed_password = generate_password_hash(new_password)

#         try:
#             user.password = hashed_password
#             db.session.commit()
#         except Exception as e:
#             db.session.rollback()
#             result = {'message': 'Error resetting password: ' + str(e)}
#             return make_response(jsonify(result), 500)

#         result = {'message': 'Password reset successful'}
#         return make_response(jsonify(result), 200)
