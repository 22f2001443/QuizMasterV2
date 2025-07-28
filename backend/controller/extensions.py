from flask_security import Security, SQLAlchemyUserDatastore
import redis
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from celery import Celery

import utils.celeryconfig as celeryconfig

security = Security()
user_datastore = SQLAlchemyUserDatastore(None, None, None)

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

cache = Cache()

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="redis://localhost:6379",
    default_limits=["200 per day", "50 per hour"]
)

def make_celery(app=None):
    celery = Celery(app.import_name if app else __name__)
    
    # Load config from celeryconfig.py
    celery.config_from_object(celeryconfig)

    if app:
        celery.conf.update(app.config)

    return celery

celery = make_celery()

