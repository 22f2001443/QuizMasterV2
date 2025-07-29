from controller.extensions import celery
from controller.models import db, User, Score, Quiz
from utils.celeryconfig.mailer import send_email

@celery.task(name="tasks.send_emails.send_monthly_report_to_users")
def send_monthly_report_to_users():
    users = User.query.filter_by(active=True).all()

    for user in users:
        scores = Score.query.filter_by(user_id=user.id).all()
        if scores:
            quizzes = {score.quiz_id: Quiz.query.get(score.quiz_id) for score in scores}

            send_email(
                to=user.email,
                subject="📊 Your Monthly Performance Report",
                template_name="report.html",  # Create this in html_templates
                context={
                    "user": user,
                    "scores": scores,
                    "quizzes": quizzes
                }
            )