from flask_restful import Resource, reqparse
from werkzeug.security import check_password_hash, generate_password_hash

from controller.model import User
from controller.db import db

# --- Request Parsers ---
register_parser = reqparse.RequestParser()
register_parser.add_argument('name', type=str, required=True, help='Name is required')
register_parser.add_argument('email', type=str, required=True, help='Email is required')
register_parser.add_argument('password', type=str, required=True, help='Password is required')

login_parser = reqparse.RequestParser()
login_parser.add_argument('email', type=str, required=True, help='Email is required')
login_parser.add_argument('password', type=str, required=True, help='Password is required')

# --- Resource: Register --- #working
class Register(Resource):
    def post(self):
        args = register_parser.parse_args()
        name = args['name']
        email = args['email']
        password = args['password']

        # Check if user already exists
        if User.query.filter_by(email=email).first():
            return {'message': 'Email already registered'}, 409

        hashed_password = generate_password_hash(password)

        new_user = User(username=name, email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User registered successfully'}, 201

# --- Resource: Login ---
class Login(Resource):
    def post(self):
        args = login_parser.parse_args()
        email = args['email']
        password = args['password']

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            return {'message': 'Invalid email or password'}, 401

        return {'message': 'Login successful', 'user': {'id': user.id, 'name': user.name, 'email': user.email}}, 200