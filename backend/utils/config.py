import os
from dotenv import load_dotenv
import redis

load_dotenv()  # Load environment variables from .env file

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))  # go up one level
db_name = os.getenv("DB_NAME", "default_db.sqlite")
db_path = os.path.join(basedir, 'data', db_name)

class config:
    SECRET_KEY = os.getenv("SECRET_KEY", "fallback_secret")
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{db_path}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- Flask-Security Config ---
    SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT", "some_random_salt")
    SECURITY_REMEMBER_SALT = os.getenv("SECURITY_REMEMBER_SALT", "some_random_salt")
    SECURITY_REGISTERABLE = True
    SECURITY_SEND_REGISTER_EMAIL = False
    SECURITY_TOKEN_AUTHENTICATION_KEY = "auth_token"
    SECURITY_TOKEN_MAX_AGE = 3600
    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    SESSION_REDIS = redis.from_url(os.getenv("REDIS_URL"))
    CACHE_TYPE = 'RedisCache'
    CACHE_REDIS_URL = os.getenv("REDIS_URL")
    CACHE_DEFAULT_TIMEOUT = 600  # 10 minutes

    CELERY_BROKER_URL = os.getenv("REDIS_URL","redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("REDIS_URL","redis://localhost:6379/0")