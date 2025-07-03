from controller.models import db
from controller.models.semester_model import subject_semester
from controller.models.user_model import BaseModel 

class Subject(BaseModel):
    __tablename__ = 'subjects'

    name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=False)
    faculty = db.Column(db.String(100), nullable=True)
    code = db.Column(db.String(20), nullable=False, unique=True)

    # Many-to-many: A subject is taught in multiple semesters
    semesters = db.relationship(
        'Semester',
        secondary=subject_semester,
        back_populates='subjects'
    )

    # One-to-many: A subject has many chapters
    chapters = db.relationship(
        'Chapter',
        back_populates='subject',
        cascade='all, delete-orphan',
        passive_deletes=True
    )

    def __repr__(self):
        return f"<Subject {self.name}, Department: {self.department}, Subject Code: {self.code}, {'Faculty: ' + self.faculty if self.faculty else ''}>"
    
