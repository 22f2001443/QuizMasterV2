from os import abort
from flask_restful import Resource, reqparse
from flask_caching import Cache
from flask import jsonify, make_response, request, Blueprint
from flask_security import auth_token_required, roles_required
from datetime import datetime, timezone
import json
from io import StringIO
import csv

from controller.extensions import redis_client
from controller.extensions import cache
from controller.models import db, User, Subject, Quiz, Score, Semester, Chapter, Question, SemesterEnum, QuestionTypeEnum
from sqlalchemy.exc import SQLAlchemyError



def get_or_set_cache(key, fetch_func, ttl=300):
    cached_data = redis_client.get(key)
    if cached_data:
        return json.loads(cached_data)
    data = fetch_func()
    redis_client.setex(key, ttl, json.dumps(data))
    return data

# --- Resource: Admin Analytics --- 

class GetStudentDistribution(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        def fetch_distribution():
            semesters = Semester.query.all()
            return [
                {
                    "semester": semester.name.value,
                    "student_count": User.query.filter_by(semester_id=semester.id).count()
                } for semester in semesters
            ]

        result = get_or_set_cache("admin:student_distribution", fetch_distribution)
        return make_response(jsonify(result), 200)

class GetLeaderboard(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        def fetch_leaderboard():
            top_students = db.session.query(
                User.id, User.name, Semester.name.label('semester_name'),
                db.func.avg(Score.percentage).label('average_score')
            ).join(Score).join(Semester, User.semester_id == Semester.id)\
             .group_by(User.id, Semester.name).order_by(db.desc('average_score')).limit(5).all()

            return [
                {
                    "id": student.id,
                    "name": student.name,
                    "semester": student.semester_name.value if student.semester_name else None,
                    "score": round(student.average_score, 2) if student.average_score else 0
                } for student in top_students
            ]

        result = get_or_set_cache("admin:leaderboard", fetch_leaderboard)
        return make_response(jsonify({"top_performers": result}), 200)
    

        
class GetLeaderboard(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        # Fetch top 10 students based on their average scores
        top_students = db.session.query(
            User.id, User.name, Semester.name.label('semester_name'), db.func.avg(Score.percentage).label('average_score')
        ).join(Score).join(Semester, User.semester_id == Semester.id).group_by(User.id, Semester.name).order_by(db.desc('average_score')).limit(5).all()

        leaderboard = [
            {
                "id": student.id,
                "name": student.name,
                "semester": student.semester_name.value if student.semester_name else None,
                "score": round(student.average_score, 2) if student.average_score is not None else 0
            } for student in top_students
        ]

        return make_response(jsonify({"top_performers": leaderboard}), 200)
    
class GetSubjectAttempts(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        def fetch_attempts():
            subjects = Subject.query.all()
            return [
                {
                    "subject_name": subject.name,
                    "attempt_count": db.session.query(Score)
                        .join(Score.quiz)
                        .join(Quiz.chapter)
                        .join(Chapter.subject)
                        .filter(Subject.id == subject.id)
                        .count()
                } for subject in subjects
            ]

        result = get_or_set_cache("admin:subject_attempts", fetch_attempts)
        return make_response(jsonify(result), 200)
    
class GetQuizPerformance(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        def fetch_performance():
            quizzes = Quiz.query.all()
            return [
                {
                    "quiz_id": quiz.id,
                    "title": quiz.title,
                    "average_score": db.session.query(db.func.avg(Score.percentage))
                                      .filter(Score.quiz_id == quiz.id).scalar() or 0
                } for quiz in quizzes
            ]

        result = get_or_set_cache("admin:quiz_performance", fetch_performance)
        return make_response(jsonify(result), 200)

class GetStudentStatusCount(Resource):
    @auth_token_required
    @roles_required('admin')
    def get(self):
        def fetch_status_count():
            # users = User.query.all()
            return {
                'active_count': User.query.filter_by(active=True).count(),
                "inactive_count": User.query.filter_by(active=False).count(),
            }

        result = get_or_set_cache("admin:student_status_count", fetch_status_count)
        return make_response(jsonify(result), 200)


class DownloadProgress(Resource):
    @auth_token_required
    @cache.cached(timeout=300)
    @roles_required('admin')
    def get(self):
        output = StringIO()
        writer = csv.writer(output)

        # --- Section 1: Leaderboard ---
        def fetch_leaderboard():
            top_students = db.session.query(
                User.id, User.name, Semester.name.label('semester_name'),
                db.func.avg(Score.percentage).label('average_score')
            ).join(Score).join(Semester, User.semester_id == Semester.id)\
             .group_by(User.id, Semester.name).order_by(db.desc('average_score')).limit(5).all()

            return [
                {
                    "ID": student.id,
                    "Name": student.name,
                    "Semester": student.semester_name.value if student.semester_name else '',
                    "Score (%)": round(student.average_score or 0, 2)
                } for student in top_students
            ]

        writer.writerow(['--- Top 5 Leaderboard ---'])
        leaderboard_data = fetch_leaderboard()
        writer.writerow(leaderboard_data[0].keys())
        for row in leaderboard_data:
            writer.writerow(row.values())
        writer.writerow([])

        # --- Section 2: Student Status ---
        def fetch_status_count():
            return {
                'Active Students': User.query.filter_by(active=True).count(),
                'Inactive Students': User.query.filter_by(active=False).count()
            }

        writer.writerow(['--- Student Status ---'])
        status_data = fetch_status_count()
        for key, val in status_data.items():
            writer.writerow([key, val])
        writer.writerow([])

        # --- Section 3: Subject Attempts ---
        def fetch_attempts():
            subjects = Subject.query.all()
            return [
                {
                    "Subject": subject.name,
                    "Attempts": db.session.query(Score)
                        .join(Score.quiz)
                        .join(Quiz.chapter)
                        .join(Chapter.subject)
                        .filter(Subject.id == subject.id)
                        .count()
                } for subject in subjects
            ]

        writer.writerow(['--- Subject Attempts ---'])
        subject_data = fetch_attempts()
        writer.writerow(subject_data[0].keys())
        for row in subject_data:
            writer.writerow(row.values())
        writer.writerow([])

        # --- Section 4: Quiz Performance ---
        def fetch_performance():
            quizzes = Quiz.query.all()
            return [
                {
                    "Quiz ID": quiz.id,
                    "Title": quiz.title,
                    "Avg Score (%)": round(
                        db.session.query(db.func.avg(Score.percentage))
                        .filter(Score.quiz_id == quiz.id).scalar() or 0, 2
                    )
                } for quiz in quizzes
            ]

        writer.writerow(['--- Quiz Performance ---'])
        quiz_data = fetch_performance()
        writer.writerow(quiz_data[0].keys())
        for row in quiz_data:
            writer.writerow(row.values())
        writer.writerow([])

        # --- Finalize CSV Response ---
        response = make_response(output.getvalue())
        response.headers['Content-Disposition'] = 'attachment; filename=progress_report.csv'
        response.headers['Content-type'] = 'text/csv'
        return response