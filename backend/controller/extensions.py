from flask_security import Security, SQLAlchemyUserDatastore
import redis
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from celery import Celery

security = Security()
user_datastore = SQLAlchemyUserDatastore(None, None, None)

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

cache = Cache()

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

def make_celery(app_name=__name__):
    return Celery(
        app_name,
        broker='redis://localhost:6379/0',
        backend='redis://localhost:6379/0'
    )

celery = make_celery()