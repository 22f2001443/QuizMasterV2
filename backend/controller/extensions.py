from flask_security import Security, SQLAlchemyUserDatastore

security = Security()
user_datastore = SQLAlchemyUserDatastore(None, None, None)
