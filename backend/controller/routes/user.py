from flask_restful import Resource, reqparse
from flask import jsonify
from controller.models.user_model import User

# --- Optional: parser to fetch by email or id ---
profile_parser = reqparse.RequestParser()
profile_parser.add_argument('email', type=str, required=False)
profile_parser.add_argument('id', type=int, required=False)

class UserProfile(Resource):
    def get(self):
        args = profile_parser.parse_args()
        user = None

        # Prefer email lookup if provided
        if args['email']:
            user = User.query.filter_by(email=args['email']).first()
        elif args['id']:
            user = User.query.get(args['id'])
        else:
            return {'message': 'Please provide user ID or email'}, 400

        if not user:
            return {'message': 'User not found'}, 404

        return {
            
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'created_at': user.created_at.isoformat()
            }, 200