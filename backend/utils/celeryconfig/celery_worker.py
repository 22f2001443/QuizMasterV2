from app import CreateApp
from controller.extensions import celery

#Create the Flask app instance
app, _ = CreateApp()

app.app_context().push()