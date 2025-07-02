import os
from dotenv import load_dotenv
from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from werkzeug.security import generate_password_hash
from sqlalchemy import event

from controller.db import db
from config import config
from controller.model import User, Quiz
from controller.routes.routesRegister import register_routes

# --- Load environment variables ---
load_dotenv()

# --- Setup ---
app = Flask(__name__)  # No template_folder needed anymore
app.config.from_object(config)
api = Api(app)
CORS(app,resources ={
                r"/api/*":
                  {
                    "origins": '*',
                    "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
                    }
                        })  # Enable CORS for all API routes

# --- Register Routes ---
register_routes(api)

# --- Database Initialization ---
with app.app_context():
    db.init_app(app)
    db.create_all()

# --- Run Server with .env PORT ---
if __name__ == '__main__':
    port = int(os.getenv("PORT", 8000))
    app.run(port=port, host='0.0.0.0', debug=True)

