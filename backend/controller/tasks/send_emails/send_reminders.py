from controller.extensions import celery
from utils.celeryconfig.mailer import send_email
from controller.models import db, User, Quiz, Score

def getPendingQuizzes(user):
    user = user
    quizzes = []
    for subject in user.semester.subjects:
        for chapter in subject.chapters:
            for quiz in chapter.quizzes:
                if quiz.is_active and quiz.questions:
                    quizzes.append(quiz)
    return quizzes

@celery.task(name='tasks.send_emails.send_daily_quiz_reminders')
def send_daily_quiz_reminders():
    users = User.query.filter(User.active ==True , User.email != "admin@example.com").all()
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