import os
from dotenv import load_dotenv
from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from werkzeug.security import generate_password_hash
from sqlalchemy import event
from flask_security import Security, SQLAlchemyUserDatastore, utils as security_utils


from controller.models import db, User, Role, UserRole , Semester
from utils.config import config
from controller.routes import register_routes
from controller.extensions import security, user_datastore
from controller.models.enums import SemesterEnum

# --- Load environment variables ---
load_dotenv()

# --- Seed Semesters ---
# This function seeds the database with predefined semesters if they do not already exist.
def seed_semesters():
    for sem in SemesterEnum:
        if not Semester.query.filter_by(name=sem.value).first():
            db.session.add(Semester(name=sem.value))
    db.session.commit()

# --- Setup ---
def CreateApp():
    app = Flask(__name__)  # No template_folder needed anymore
    app.config.from_object(config)
    api = Api(app)

    return app, api
# --- Initialize Flask App and API ---
app, api = CreateApp()
CORS(app, resources={
        r"/api/*": {
            "origins": '*',
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
        }
    })  # Enable CORS for all API routes

# --- Setup Flask-Security ---
user_datastore.user_model = User
user_datastore.role_model = Role
user_datastore.db = db

security.init_app(app, user_datastore)

def enable_foreign_keys():
    @event.listens_for(db.engine, "connect")
    def set_sqlite_pragma(dbapi_connection, connection_record):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

# --- Database Initialization ---
def CreateDatabase(app, db):
    with app.app_context():
      db.init_app(app)
      enable_foreign_keys()
      db.create_all()

      # --- Create default roles if they don't exist ---
      if not user_datastore.find_role("admin"):
        user_datastore.create_role(
          name="admin",
          description="Administrator role"
          )
      if not user_datastore.find_role("user"):
        user_datastore.create_role(
          name="user",
          description="User role"
          )
        # --- Create default admin user if it doesn't exist ---
      if not user_datastore.find_user(email="admin@example.com"):
        user_datastore.create_user(
          name="Admin",
          email="admin@example.com",
          password=generate_password_hash("admin"),  
          roles=["admin"]
        )

      # Seed semesters
      seed_semesters()

      # --- Register Routes ---
      register_routes(api)

      # --- Create User Roles Table ---
      db.session.commit()
      
# --- Create Database and Tables ---
CreateDatabase(app, db)


# --- Run Server with .env PORT ---
if __name__ == '__main__':
    port = int(os.getenv("PORT", 8000))
    app.run(port=port, host='0.0.0.0', debug=True)
    