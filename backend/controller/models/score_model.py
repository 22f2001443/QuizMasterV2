from datetime import datetime
from controller.models import db
from controller.models.user_model import BaseModel

class Score(BaseModel):
    __tablename__ = 'scores'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzes.id', ondelete='CASCADE'), nullable=False)

    percentage = db.Column(db.Float, nullable=False)
    submission_time = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_submitted = db.Column(db.Boolean, default=False, nullable=False)

    correct_count = db.Column(db.Integer, nullable=False, default=0)
    incorrect_count = db.Column(db.Integer, nullable=False, default=0)

    # Relationships
    user = db.relationship("User", backref=db.backref("scores", cascade="all, delete-orphan", passive_deletes=True))
    quiz = db.relationship("Quiz", backref=db.backref("scores", cascade="all, delete-orphan", passive_deletes=True))

    __table_args__ = (
        db.UniqueConstraint('user_id', 'quiz_id', name='unique_user_quiz_score'),  # ✅ Enforce one attempt per quiz
    )

    def __repr__(self):
        return f"<Score User={self.user_id}, Quiz={self.quiz_id}, %={self.percentage}>"