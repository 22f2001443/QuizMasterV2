from controller.models import db
from controller.models.user_model import BaseModel

class Quiz(BaseModel):
    __tablename__ = 'quizzes'

    title = db.Column(db.String(200), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapters.id', ondelete='CASCADE'), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    time_limit = db.Column(db.Integer, nullable=True)  # Time limit in seconds
    is_active = db.Column(db.Boolean, default=True, nullable=False)

    # Relationship back to Chapter
    chapter = db.relationship('Chapter', back_populates='quizzes')

    # One-to-many: A quiz can have many questions
    questions = db.relationship(
        'Question',
        back_populates='quiz',
        cascade='all, delete-orphan',
        passive_deletes=True
    )

    def update_total_marks(self):
        self.total_marks = sum(q.marks for q in self.questions)
        self.time_limit = self.total_marks * 2

    def __repr__(self):
        return f"<Quiz {self.title}, Chapter ID: {self.chapter_id}>"