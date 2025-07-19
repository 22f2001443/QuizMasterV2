from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Now import models (not during circular reference)
from .user_model import User, Role, UserRole
from .semester_model import Semester, subject_semester
from .subject_model import Subject
from .chapter_model import Chapter
from .quiz_model import Quiz
from .question_model import Question
from .score_model import Score

from .enums import SemesterEnum, QuestionTypeEnum

__all__ = [
    'db', 'SemesterEnum', 'QuestionTypeEnum',
    'User', 'Role', 'UserRole',
    'Semester', 'subject_semester',
    'Subject', 'Chapter', 'Quiz', 'Question', 'Score'
]