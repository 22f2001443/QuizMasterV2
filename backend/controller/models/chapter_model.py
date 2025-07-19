from controller.models import db
from controller.models.user_model import BaseModel 

class Chapter(BaseModel):
    __tablename__ = 'chapters'

    name = db.Column(db.String(200), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subjects.id', ondelete='CASCADE'), nullable=False)
    #description = db.Column(db.Text, nullable=True)
    
    # Relationship back to Subject
    subject = db.relationship('Subject', back_populates='chapters')

    # One-to-many: A chapter has many quizzes
    quizzes = db.relationship(
        'Quiz',
        back_populates='chapter',
        cascade='all, delete-orphan',
        passive_deletes=True
    )


    def __repr__(self):
        return f"<Chapter {self.name}, Subject ID: {self.subject_id}>"