from app import CreateApp
from controller.extensions import celery

#Create the Flask app instance
app, _ = CreateApp()

app.app_context().push()

from controller.tasks.send_emails import send_daily_quiz_reminders, send_monthly_report_to_users