from controller.models import db
from controller.models.enums import SemesterEnum

# Association table for many-to-many relationship between Subject and Semester
subject_semester = db.Table(
    'subject_semester',
    db.Column('subject_id', db.Integer, db.ForeignKey('subjects.id'), primary_key=True),
    db.Column('semester_id', db.Integer, db.ForeignKey('semesters.id'), primary_key=True)
)

class Semester(db.Model):
    __tablename__ = 'semesters'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum(SemesterEnum, values_callable=lambda x: [e.value for e in x]), unique=True, nullable=False)

    # One-to-many: A semester has many users
    users = db.relationship('User', back_populates='semester')

    # Many-to-many: A semester has many subjects
    subjects = db.relationship(
        'Subject',
        secondary=subject_semester,
        back_populates='semesters'
    )

    def __repr__(self):
        return f"<Semester {self.name}>"
    