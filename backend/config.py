import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

basedir = os.path.abspath(os.path.dirname(__file__))
db_name = os.getenv("DB_NAME", "default_db.sqlite")
db_path = os.path.join(basedir, 'data', db_name)

class config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret")  # Required for flash messages
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  #Disables tracking
