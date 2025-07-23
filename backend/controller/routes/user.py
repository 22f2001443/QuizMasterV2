from flask_restful import Resource, reqparse
from flask import jsonify, make_response, request
from flask_security import auth_token_required
from datetime import datetime

from controller.models import db, User, Subject, Quiz, Score, Semester, Chapter, Question, SemesterEnum, QuestionTypeEnum

# --- Optional: parser to fetch by email or id ---
# profile_parser = reqparse.RequestParser()
# profile_parser.add_argument('email', type=str, required=False)
# profile_parser.add_argument('id', type=int, required=False)

class UserProfile(Resource):
    @auth_token_required
    def get(self, user_id):
        
        user = User.query.get(user_id)

        if not user:
            return {'message': 'User not found'}, 404

        response = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            #'roles': user.roles,
            'semester': user.semester.name.value if user.semester else None,
            'joinedDate': {
                'year': user.created_at.year,
                'month': user.created_at.month,
                'day': user.created_at.day
            },
            'overallScore': Score.query.filter_by(user_id=user.id).with_entities(db.func.sum(Score.percentage)).scalar() or 0,
            'quizCount': Score.query.filter_by(user_id=user.id).distinct(Score.quiz_id).count(),
            #'subjects': [{'id': subject.id, 'name': subject.name} for subject in user.subjects],
            'subject_count': len(user.semester.subjects) if user.semester else 0,
            'dob': user.dob.strftime('%Y-%m-%d') if user.dob else 'Unknown DOB'
        }
        return make_response(jsonify(response), 200)
    
class UserDashboard(Resource):
    @auth_token_required
    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return make_response(jsonify({'message': 'User not found'}), 404)
        
        subjects = user.semester.subjects if user.semester.name else []
        if not subjects:
            return make_response(jsonify({'message': 'No subjects found for this user'}), 404)
        quizzes = [quiz for sub in subjects for chap in sub.chapters for quiz in chap.quizzes] if user.semester else []

        scores = Score.query.filter_by(user_id=user.id).all()

        response = {
            'user_id': user.id,
            'name': user.name,
            'email': user.email,
            'semester': user.semester.name.value if user.semester else None,
            'subjects': [{'id': subject.id, 'name': subject.name} for subject in subjects],
            # 'chapters': [
            #     {
            #         'id': chapter.id,
            #         'name': chapter.name,
            #         'subject': chapter.subject.name if chapter.subject else None,
            #         'quizzes_count': len(chapter.quizzes) if chapter.quizzes else 0,
            #     }
            #     for subject in subjects for chapter in subject.chapters
            # ],
            'quizzes': [
                {
                    'id': quiz.id,
                    'name': quiz.title,
                    'subject': quiz.chapter.subject.name if quiz.chapter else None,
                    'chapter': quiz.chapter.name if quiz.chapter else None,
                    'question_count': len(quiz.questions),
                    'marks': quiz.total_marks,
                    'time': quiz.time_limit if quiz.time_limit else 0,
                    'is_attempted': any(score.quiz_id == quiz.id for score in scores),
                }
                for quiz in quizzes if quiz.is_active and quiz.questions
            ],
        }

        return make_response(jsonify(response), 200)

class QuizStart(Resource):
    @auth_token_required
    def post(self, quiz_id):
        data = request.get_json()

        user_id = data.get('user_id')
        user = User.query.get(user_id)
        quiz = Quiz.query.get(quiz_id)

        if not user or not quiz:
            return make_response(jsonify({'message': 'User or Quiz not found'}), 404)

        if not quiz.is_active:
            return make_response(jsonify({'message': 'Quiz is not active'}), 403)

        # Check if the user is authorized to take the quiz
        if user.semester not in quiz.chapter.subject.semesters:
            return make_response(jsonify({'message': 'You are not authorized to take this quiz'}), 403)

        # Create a new quiz session
        try:
            session = Score(
                user_id=user.id,
                quiz_id=quiz.id,
                percentage=0,
                # started_at=datetime.utcnow(),
                # is_active=True  # Optional: helps in controlling ongoing/incomplete quizzes
                )
            db.session.add(session)
            db.session.commit()

            return make_response(jsonify({'session_id': session.id}), 200)
        except Exception as error:
            db.session.rollback()
            return make_response(jsonify({f'message': f'Error starting quiz session: {error}'}), 500)

    @auth_token_required
    def get(self, quiz_id):
        quiz = Quiz.query.get(quiz_id)
        if not quiz:
            return make_response(jsonify({'message': 'Quiz not found'}), 404)

        response = {
            'id': quiz.id,
            'title': quiz.title,
            'description': quiz.description,
            'total_marks': quiz.total_marks,
            'time_limit': quiz.time_limit,
            'is_active': quiz.is_active,
            'chapter_name': quiz.chapter.name if quiz.chapter else None,
            'questions_count': len(quiz.questions),
            'subject_name': quiz.chapter.subject.name if quiz.chapter and quiz.chapter.subject else None,
        }

        return make_response(jsonify(response), 200)
    

class getQuestion(Resource):
    @auth_token_required
    def get(self, score_entry_id):
        score_entry = Score.query.get(score_entry_id)
        if not score_entry:
            return make_response(jsonify({'message': 'Score entry not found'}), 404)
        quiz = Quiz.query.get(score_entry.quiz_id)
        if not quiz:
            return make_response(jsonify({'message': 'Quiz not found'}), 404)

        questions = Question.query.filter_by(quiz_id=quiz.id).all()
        if not questions:
            return make_response(jsonify({'message': 'No questions found for this quiz'}), 404)

        response = {
            'quiz_name': quiz.title,
            'time': quiz.time_limit,
            'marks': quiz.total_marks,
            'total_questions': len(questions),
            'questions': [
                {
                    'id': question.id,
                    'text': question.text,
                    'type': question.question_type.value,
                    'options': question.options,  # Make sure this is serializable
                    'marks': question.marks
                }
                for question in questions
            ]
        }

        return make_response(jsonify(response), 200)
    
    @auth_token_required
    def post(self, score_entry_id):
        data = request.get_json()
        score_entry = Score.query.get(score_entry_id)
        user_id = data.get('user_id')
        if not score_entry or score_entry.user_id != user_id:
            return make_response(jsonify({'message': 'Not authorized'}), 404)
        

        return