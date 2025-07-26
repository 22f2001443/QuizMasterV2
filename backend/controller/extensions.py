from flask_security import Security, SQLAlchemyUserDatastore
import redis
from flask_caching import Cache

security = Security()
user_datastore = SQLAlchemyUserDatastore(None, None, None)

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

cache = Cache()