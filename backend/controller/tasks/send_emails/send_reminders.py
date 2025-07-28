from utils.celeryconfig.mailer import send_email
from controller.models import User, Quiz, Score

def getPendingQuizzes(user):
    user = user
    pending_quizzes = [q for sub in user.semester.subjects for chap in sub.chapters for quiz in chap.quizzes for q in quiz.is_active and quiz.questions] if user.semester else []
    return pending_quizzes

@celery.task
def send_daily_quiz_reminders():
    users = User.query.filter_by(active=True).all()
    for user in users:
        pending_quizzes = getPendingQuizzes(user)
        if pending_quizzes:
            send_email(
                to=user.email,
                subject="Pending Quiz Reminder",
                template_name='reminder.html',
                context={
                    'user': user,
                    'quizzes': pending_quizzes
                    }
                )