import enum

class SemesterEnum(enum.Enum):
    SEM_I= "Semester I"
    SEM_II= "Semester II"
    SEM_III= "Semester III"
    SEM_IV= "Semester IV"
    SEM_V= "Semester V"
    SEM_VI= "Semester VI"
    SEM_VII= "Semester VII"
    SEM_VIII= "Semester VIII"

    def __str__(self):
        return self.value
    

class QuestionTypeEnum(enum.Enum):
    MCQ = "MCQ"
    NTA = "NTA"

    def __str__(self):
        return self.value