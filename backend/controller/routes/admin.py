from flask_restful import Resource, reqparse
from flask import jsonify, make_response, request
from flask_security import auth_token_required, roles_required
from datetime import datetime, timezone

from controller.models import db, User, Subject, Quiz, Score, Semester, Chapter, Question, SemesterEnum, QuestionTypeEnum
from sqlalchemy.exc import SQLAlchemyError

# --- Resource: Admin Metrics --- #
class AdminMetrics(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        # Fetch total users, subjects, quizzes, and scores
        total_users = User.query.count()
        total_subjects = Subject.query.count()
        total_quizzes = Quiz.query.count()
        total_scores = Score.query.count()

        result = {
            'total_users': total_users,
            'total_subjects': total_subjects,
            'total_quizzes': total_quizzes,
            'total_attempts': total_scores
        }

        return make_response(jsonify(result), 200)

# --- Parser for editing user ---
user_edit_parser = reqparse.RequestParser()
user_edit_parser.add_argument('name', type=str, required=False)
user_edit_parser.add_argument('email', type=str, required=False)
user_edit_parser.add_argument('dob', type=str, required=False)
user_edit_parser.add_argument('active', type=bool, required=False)

# --- Resource: Admin User Management --- #
class AdminUserManagement(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        users = User.query.all()
        result = [
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "active": user.active,
                "roles": [role.name for role in user.roles],
                "dob": str(user.dob) if user.dob else None,
                "semester": user.semester.name.value if user.semester else None
            } for user in users
        ]
        return make_response(jsonify(result), 200)

    @auth_token_required
    @roles_required('admin')
    def put(self):
        data = request.get_json()
        user_id = data.get('id')
        if not user_id:
            return {"message": "User ID is required for update"}, 400

        user = User.query.get(user_id)
        if not user:
            return {"message": "User not found"}, 404

        args = user_edit_parser.parse_args()
        if args['name']:
            user.name = args['name']
        if args['email']:
            user.email = args['email']
        if args['dob']:
            user.dob = args['dob']
        if args['active'] is not None:
            user.active = args['active']

        try:
            db.session.commit()
            return {"message": "User updated successfully"}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": "Update failed", "error": str(e)}, 500

    @auth_token_required
    @roles_required('admin')
    def delete(self):
        print("Raw request data:", request.get_data(as_text=True))
        data = request.get_json()
        print("Parsed JSON data:", data)
        user_id = data.get('id')
        print(f"Deleting user with ID: {user_id}")
        if not user_id:
            return {"message": "User ID is required for deletion"}, 400

        user = User.query.get(user_id)
        print(f"Found user: {user}")
        if not user:
            return {"message": "User not found"}, 404

        try:
            db.session.delete(user)
            db.session.commit()
            return {"message": f"User {user_id} deleted"}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": "Deletion failed", "error": str(e)}, 500


# --- Resource: Admin Subject Management --- #
class AdminSubjectManagement(Resource):
    @auth_token_required
    @roles_required('admin')
    def delete(self):
        data = request.get_json()
        subject_id = data.get('id')

        if not subject_id:
            return {"message": "Subject ID is required for deletion"}, 400

        subject = Subject.query.get(subject_id)
        if not subject:
            return {"message": "Subject not found"}, 404

        try:
            db.session.delete(subject)
            db.session.commit()
            return {"message": f"Subject {subject_id} deleted successfully"}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": "Subject deletion failed", "error": str(e)}, 500
    @auth_token_required
    @roles_required('admin')
    def get(self):
        if request.args.get('form_config') == 'true':
            # Return form schema instead of data
            semesters = Subject.semesters.property.mapper.class_.query.all()
            return make_response(jsonify({
                "type": "add_subject",
                "fields": [
                    {"name": "name", "label": "Subject Name", "type": "text", "required": True},
                    {"name": "code", "label": "Subject Code", "type": "text", "required": True},
                    {"name": "department", "label": "Department", "type": "text", "required": True},
                    {"name": "faculty", "label": "Faculty", "type": "text", "required": False},
                    {"name": "semester_ids", "label": "Semesters", "type": "multiselect", "required": True,
                     "options": [{"label": sem.name.value, "value": sem.id} for sem in semesters]}
                ]
            }), 200)
        
        # Default: Fetch all subjects
        subjects = Subject.query.all()
        #semesters = {sem.name.value: sem.id for sem in Subject.semester}

        result = [
            {
                "id": subject.id,
                "name": subject.name,
                "code": subject.code,
                "department": subject.department,
                "faculty": subject.faculty,
                "semesters": [sem.id for sem in subject.semesters],
                "chapters_count": len(subject.chapters) if subject.chapters else 0
            } for subject in subjects
        ]

        return make_response(jsonify(result), 200)
    
    @auth_token_required
    @roles_required('admin')
    def post(self):
        data = request.get_json()

        # Validate required fields
        required_fields = ['name', 'code', 'department', 'semester_ids']
        for field in required_fields:
            if not data.get(field):
                return {"message": f"{field} is required"}, 400

        try:
            # Fetch Semester objects from provided IDs
            semester_ids = data.get('semester_ids', [])
            semesters = Semester.query.filter(Semester.id.in_(semester_ids)).all()

            if not semesters:
                return {"message": "No valid semesters found"}, 400

            # Create Subject instance
            new_subject = Subject(
                name=data['name'],
                code=data['code'],
                department=data['department'],
                faculty=data.get('faculty'),  # Optional
                semesters=semesters  # Establish many-to-many link
            )

            db.session.add(new_subject)
            db.session.commit()

            return make_response(jsonify({
                "message": "Subject created successfully",
                "id": new_subject.id
            }), 201)

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": "Database error", "error": str(e)}, 500
        
    @auth_token_required
    @roles_required('admin')
    def put(self):
        data = request.get_json()
        subject_id = data.get('id')

        if not subject_id:
            return {"message": "Subject ID is required for update"}, 400

        subject = Subject.query.get(subject_id)
        if not subject:
            return {"message": "Subject not found"}, 404

        try:
            # Update fields
            subject.name = data.get('name', subject.name)
            subject.code = data.get('code', subject.code)
            subject.department = data.get('department', subject.department)
            subject.faculty = data.get('faculty', subject.faculty)

            # Update many-to-many semesters relationship
            semester_ids = data.get('semester_ids', [])
            semesters = Semester.query.filter(Semester.id.in_(semester_ids)).all()

            subject.semesters = semesters

            db.session.commit()
            return {"message": f"Subject {subject.name} updated successfully"}, 200

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": "Subject update failed", "error": str(e)}, 500
    

# --- Resource: Admin Chapter Management --- #

class AdminChapterManagement(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self, subject_id):
        if request.args.get('form_config') == 'true':
            return make_response(jsonify({
                "type": "add_chapter",
                "fields": [
                    {"name": "title", "label": "Chapter Title", "type": "text", "required": True},
                    {"name": "description", "label": "Description", "type": "textarea", "required": False}
                ]
            }), 200)

        subject = Subject.query.get(subject_id)
        if not subject:
            return {"message": "Subject not found"}, 404

        chapters = subject.chapters
        result = {
            "subject_id": subject.id,
            "subject_name": subject.name,
            "chapters": [
                {
                    "id": chapter.id,
                    "title": chapter.name,
                    #"description": chapter.description
                    "quizzes_count": len(chapter.quizzes) if chapter.quizzes else 0
                } for chapter in chapters
            ]
        }
        return make_response(jsonify(result), 200)

    # POST: Create a new chapter under a subject
    @auth_token_required
    @roles_required('admin')
    def post(self, subject_id):
        data = request.get_json()

        title = data.get('title')
        description = data.get('description')

        if not title:
            return {"message": "Title is required"}, 400

        subject = Subject.query.get(subject_id)
        if not subject:
            return {"message": "Subject not found"}, 404

        try:
            new_chapter = Chapter(
                name=title,
                #description=description,
                subject_id=subject.id
            )
            db.session.add(new_chapter)
            db.session.commit()

            return make_response(jsonify({
                "message": "Chapter created successfully",
                "id": new_chapter.id
            }), 201)

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": "Database error", "error": str(e)}, 500

    # DELETE: Remove a chapter by ID
    @auth_token_required
    @roles_required('admin')
    def delete(self, subject_id):
        data = request.get_json()
        chapter_id = data.get('id')
        subject_name = Subject.query.get(subject_id).name if subject_id else "Unknown Subject"
        if not chapter_id:
            return {"message": "Chapter ID is required for deletion"}, 400

        chapter = Chapter.query.filter_by(id=chapter_id).first()
        if not chapter:
            return {"message": "Chapter not found"}, 404

        try:
            db.session.delete(chapter)
            db.session.commit()
            return {"message": f"Chapter [Chapter ID: {chapter_id}] from Subject: {subject_name} deleted successfully"}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": "Deletion failed", "error": str(e)}, 500
        
    # PUT: Update an existing chapter


class AdminQuizManagement(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        if request.args.get('form_config') == 'true':
            # Fetch subjects and chapters
            subjects = Subject.query.all()

            # Create options for subject dropdown
            subject_options = [{"label": subj.name, "value": subj.id} for subj in subjects]

            # Map chapters by subject
            options_by_subject = {}
            for subj in subjects:
                options_by_subject[str(subj.id)] = [
                    {"label": chapter.name, "value": chapter.id}
                    for chapter in subj.chapters
                ]

            return make_response(jsonify({
                "type": "add_quiz",
                "fields": [
                    {
                        "name": "subject_id",
                        "label": "Subject",
                        "type": "select",
                        "required": True,
                        "options": subject_options
                    },
                    {
                        "name": "chapter_id",
                        "label": "Chapter",
                        "type": "select",
                        "required": True,
                        "options_by_subject": options_by_subject
                    },
                    {
                        "name": "title",
                        "label": "Quiz Title",
                        "type": "text",
                        "required": True
                    },
                    {
                        "name": "description",
                        "label": "Description",
                        "type": "textarea",
                        "required": False
                    },
                    # {
                    #     "name": "time_limit",
                    #     "label": "Time Limit (minutes)",
                    #     "type": "number",
                    #     "required": False
                    # },
                    # {
                    #     "name": "is_active",
                    #     "label": "Is Active?",
                    #     "type": "checkbox",
                    #     "required": False
                    # },
                    {
                        "name": "start_time",
                        "label": "Start Time",
                        "type": "datetime-local",
                        "required": False
                    },
                    {
                        "name": "expire_time",
                        "label": "Expire Time",
                        "type": "datetime-local",
                        "required": False
                    }
                ]
            }), 200)

        # Default: return all quizzes
        quizzes = Quiz.query.all()
        result = [
            {
                "id": quiz.id,
                "title": quiz.title,
                "subject": quiz.chapter.subject.name if quiz.chapter and quiz.chapter.subject else None,
                "subject_id": quiz.chapter.subject.id if quiz.chapter and quiz.chapter.subject else None ,
                "chapter": quiz.chapter.name if quiz.chapter else None,
                "chapter_id": quiz.chapter.id if quiz.chapter else None,
                "description": quiz.description,
                "time_limit": quiz.time_limit,
                "is_active": quiz.is_active,
                "start_time": str(quiz.start_time) if quiz.start_time else None,
                "expire_time": str(quiz.expire_time) if quiz.expire_time else None,
                "total_marks": quiz.total_marks
            } for quiz in quizzes
        ]
        return make_response(jsonify(result), 200)
    
    @auth_token_required
    @roles_required('admin')
    def put(self):
        data = request.get_json()
        quiz_id = data.get('id')
        if not quiz_id:
            return {"message": "Quiz ID is required for update"}, 400

        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"message": "Quiz not found"}, 404

        # Update quiz fields
        quiz.title = data.get('title', quiz.title)
        quiz.chapter_id = data.get('chapter_id', quiz.chapter_id)
        quiz.description = data.get('description', quiz.description)
        quiz.time_limit = data.get('time_limit', quiz.time_limit)
        quiz.start_time = datetime.fromisoformat(data.get('start_time')) if data.get('start_time') else quiz.start_time
        quiz.expire_time = datetime.fromisoformat(data.get('expire_time')) if data.get('expire_time') else quiz.expire_time

        try:
            db.session.commit()
            return {"message": "Quiz updated successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Quiz update failed", "error": str(e)}, 500

    # @auth_token_required
    # @roles_required('admin')    
    # def delete(self):
    #     data = request.get_json()
    #     quiz_id = data.get('id')

    #     if not quiz_id:
    #         return {"message": "Quiz ID is required for deletion"}, 400

    #     quiz = Quiz.query.get(quiz_id)
    #     if not quiz:
    #         return {"message": "Quiz not found"}, 404

    #     try:
    #         db.session.delete(quiz)
    #         db.session.commit()
    #         return {"message": f"Quiz {quiz_id} deleted successfully"}, 200
    #     except SQLAlchemyError as e:
    #         db.session.rollback()
    #         return {"message": "Quiz deletion failed", "error": str(e)}, 500
    
    @auth_token_required
    @roles_required('admin')
    def post(self):
        data = request.get_json()

        title = data.get('title')
        chapter_id = data.get('chapter_id')
        description = data.get('description')
        time_limit = data.get('time_limit')
        start_time_str = data.get('start_time')
        expire_time_str = data.get('expire_time')

        if not title or not chapter_id:
            return {"message": "Title and Chapter ID are required"}, 400

        # Validate chapter existence
        chapter = Chapter.query.get(chapter_id)
        if not chapter:
            return {"message": "Invalid chapter ID"}, 400

        try:
            # Convert datetime strings to Python datetime objects
            start_time = datetime.fromisoformat(start_time_str) if start_time_str else None
            expire_time = datetime.fromisoformat(expire_time_str) if expire_time_str else None

            # Determine if the quiz is active
            now = datetime.now(timezone.utc)
            is_active = False
            if start_time and expire_time:
                is_active = start_time <= now <= expire_time

            new_quiz = Quiz(
                title=title,
                chapter_id=chapter_id,
                description=description,
                time_limit=time_limit,
                start_time=start_time,
                expire_time=expire_time,
                is_active=is_active,
                total_marks=0  # Initial marks = 0
         )

            db.session.add(new_quiz)
            db.session.commit()

            return make_response(jsonify({
                "message": "Quiz created successfully",
                "id": new_quiz.id
            }), 201)

        except Exception as e:
            db.session.rollback()
            return {"message": "Quiz creation failed", "error": str(e)}, 500
        
    @auth_token_required
    @roles_required('admin')
    def delete(self):
        data = request.get_json()
        quiz_id = data.get('id')

        if not quiz_id:
            return {"message": "Quiz ID is required for deletion"}, 400

        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"message": "Quiz not found"}, 404

        try:
            db.session.delete(quiz)
            db.session.commit()
            return {"message": f"Quiz {quiz_id} deleted successfully"}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": "Quiz deletion failed", "error": str(e)}, 500

# --- Resource: Admin Question Management --- #
class AdminQuestionManagement(Resource):
    def get(self, quiz_id):
        if request.args.get('form_config') == 'true':
            return make_response(jsonify({
                "type": "add_question",
                "fields": [
                    {"name": "text", "label": "Question Text", "type": "text", "required": True},
                    {"name": "question_type", "label": "Question Type", "type": "select", "required": True,
                     "options": [{"label": qt.value, "value": qt.name} for qt in QuestionTypeEnum]},
                    {"name": "marks", "label": "Marks", "type": "number", "required": True},
                    {"name": "options", "label": "Options", "type": "array", "required": True, 
                     "item_type": {"type": "text"}},
                    {"name": "answer", "label": "Correct Answer", "type": "text", "required": True}
                ]
            }), 200)


        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"message": "Quiz not found"}, 404
        chapter_name = quiz.chapter.name if quiz.chapter else "Unknown Chapter"

        questions_data = []
        for question in quiz.questions:
            q_data = {
                "id": question.id,
                "text": question.text,
                "question_type": question.question_type.value,
                "marks": question.marks,
                "correct_answer": question.correct_answer
            }
            if question.question_type == QuestionTypeEnum.MCQ:
                q_data["options"] = question.options or []  # Ensure it's a list
            questions_data.append(q_data)

        result = {
            "quiz_id": quiz.id,
            "quiz_title": quiz.title,
            "chapter_name": chapter_name,
            "questions": questions_data
        }

        return make_response(jsonify(result), 200)
    def post(self, quiz_id):
        data = request.get_json()

        text = data.get('text')
        question_type = data.get('question_type')
        marks = data.get('marks')
        options = data.get('options', [])
        answer = data.get('answer')

        if not text or not question_type or not marks or not answer:
            return {"message": "Text, Question Type, Marks, and Answer are required"}, 400

        # Validate quiz existence
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"message": "Invalid quiz ID"}, 400

        try:
            new_question = Question(
                text=text,
                question_type=QuestionTypeEnum[question_type],
                marks=marks,
                options=options,
                correct_answer=answer,
                quiz_id=quiz.id
            )

            db.session.add(new_question)
            db.session.commit()

            # Update total marks for the quiz
            quiz.update_total_marks()
            db.session.commit()

            return make_response(jsonify({
                "message": "Question created successfully",
                "id": new_question.id
            }), 201)

        except Exception as e:
            db.session.rollback()
            return {"error": str(e), "message": "Question creation failed"}, 500
        
    @auth_token_required
    @roles_required('admin')
    def put(self, quiz_id):
        data = request.get_json()
        question_id = data.get('id')
        if not question_id:
            return {"message": "Question ID is required for update"}, 400

        question = Question.query.get(question_id)
        if not question:
            return {"message": "Question not found"}, 404

        # Update question fields
        question.text = data.get('text', question.text)
        question.question_type = QuestionTypeEnum[data.get('question_type', question.question_type.name)]
        question.marks = data.get('marks', question.marks)
        question.options = data.get('options', question.options)
        question.correct_answer = data.get('answer', question.correct_answer)

        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"message": "Quiz not found"}, 404
        try:
            db.session.commit()
            # Update total marks for the quiz
            quiz.update_total_marks()
            db.session.commit()
            return {"message": "Question updated successfully"}, 200
        except Exception as e:
            db.session.rollback()
            return {"message": "Question update failed", "error": str(e)}, 500
        
    @auth_token_required
    @roles_required('admin')
    def delete(self, quiz_id):
        data = request.get_json()
        question_id = data.get('id')

        if not question_id:
            return {"message": "Question ID is required for deletion"}, 400

        question = Question.query.get(question_id)
        if not question:
            return {"message": "Question not found"}, 404
        # Validate quiz existence
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return {"message": "Invalid quiz ID"}, 400
        try:
            db.session.delete(question)
            db.session.commit()

            # Update total marks for the quiz
            quiz.update_total_marks()
            db.session.commit()

            return {"message": f"Question {question_id} deleted successfully"}, 200
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"message": "Question deletion failed", "error": str(e)}, 500

# --- Resource: Admin Analytics --- #

class GetStudentDistribution(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        # Fetch all semesters and their student counts
        semesters = Semester.query.all()
        distribution = []

        for semester in semesters:
            student_count = User.query.filter_by(semester_id=semester.id).count()
            distribution.append({
                "semester": semester.name.value,
                "student_count": student_count
            })

        return make_response(jsonify(distribution), 200)
    
class GetQuizPerformance(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        # Fetch all quizzes and their average scores
        quizzes = Quiz.query.all()
        performance = []

        for quiz in quizzes:
            average_score = db.session.query(db.func.avg(Score.score)).filter(Score.quiz_id == quiz.id).scalar() or 0
            performance.append({
                "quiz_id": quiz.id,
                "title": quiz.title,
                "average_score": average_score
            })

        return make_response(jsonify(performance), 200)
    
