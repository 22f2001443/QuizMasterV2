from controller.routes.auth import Register, Login, Logout #, ResetPassword
from controller.routes.user import UserProfile, UserDashboard, QuizStart, getQuestion, QuizResults
from controller.routes.admin import AdminMetrics, AdminUserManagement, AdminSubjectManagement, AdminChapterManagement, AdminQuizManagement, AdminQuestionManagement, GetStudentDistribution, GetQuizPerformance


def register_routes(api):
    # Routes for authentication [from controller.routes.auth import Register, Login, Logout, ResetPassword]
    api.add_resource(Login, '/api/auth/login')
    api.add_resource(Register, '/api/auth/register')
    api.add_resource(Logout, '/api/auth/logout')
    # api.add_resource(ResetPassword, '/api/auth/reset')

    # Routes for admin metrics [from controller.routes.admin import AdminMetrics]
    api.add_resource(AdminMetrics, '/api/admin/metrics')
    api.add_resource(AdminUserManagement, '/api/admin/users')
    api.add_resource(AdminSubjectManagement, '/api/admin/subjects')
    api.add_resource(AdminChapterManagement, '/api/admin/chapters/<subject_id>')
    api.add_resource(AdminQuizManagement, '/api/admin/quizzes')
    api.add_resource(AdminQuestionManagement, '/api/admin/questions/<quiz_id>')
    
    api.add_resource(GetStudentDistribution, '/api/admin/analytics/student-distribution')
    api.add_resource(GetQuizPerformance, '/api/admin/analytics/quiz-performance')
    
    # Routes for user profile [from controller.routes.user import UserProfile]
    api.add_resource(UserProfile, '/api/user/profile/<user_id>')
    api.add_resource(UserDashboard, '/api/user/dashboard/<user_id>')
    api.add_resource(QuizStart, '/api/user/quiz/start/<quiz_id>')
    api.add_resource(getQuestion, '/api/user/quiz/questions/<score_entry_id>')
    api.add_resource(QuizResults,
                 '/api/user/quiz/results/',                   # Without parameter
                 '/api/user/quiz/results/<string:quiz_session_id>')  # With parameter