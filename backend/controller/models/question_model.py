from controller.models import db
from controller.models.user_model import BaseModel
from controller.models.enums import QuestionTypeEnum

class Question(BaseModel):
    __tablename__ = 'questions'

    text = db.Column(db.String(1000), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id', ondelete='CASCADE'), nullable=False)

    question_type = db.Column(
        db.Enum(QuestionTypeEnum, values_callable=lambda obj: [e.value for e in obj]), nullable=False
    )

    options = db.Column(db.JSON, nullable=True)  # List of options if MCQ
    correct_answer = db.Column(db.String(255), nullable=False)
    marks = db.Column(db.Integer, nullable=False, default=1)

    quiz = db.relationship('Quiz', back_populates='questions')

    def __repr__(self):
        return f"<Question {self.text[:30]}... | Type: {self.question_type} | Marks: {self.marks}>"
