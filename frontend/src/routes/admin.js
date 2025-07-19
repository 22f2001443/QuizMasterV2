import AdminDashboardView from '@/views/admin/DashboardView.vue'
import UsersView from '@/views/admin/UsersView.vue'
import SubjectView from '@/views/admin/SubjectView.vue'
import ChapterView from '@/views/admin/ChapterView.vue'
import QuizzesView from '@/views/admin/QuizView.vue'
import QuestionView from '@/views/admin/QuestionView.vue'
const admin = [
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: AdminDashboardView,
    meta: {
      requiresAuth: true,
      isAdmin: true
    }
  },
  {
    path: '/admin/users',
    name: 'AdminUsers',
    component: UsersView,
    meta: {
      requiresAuth: true,
      isAdmin: true
    }
  },
  {
    path: '/admin/subjects',
    name: 'AdminSubjects',
    component: SubjectView,
    meta: {
      requiresAuth: true,
      isAdmin: true
    }
  },
  {
    path: '/admin/chapters/:subjectId',
    name: 'AdminChapters',
    component: ChapterView,
    meta: {
      requiresAuth: true,
      isAdmin: true
    }
  },
  {
    path: '/admin/quizzes',
    name: 'AdminQuizzes',
    component: QuizzesView,
    meta: {
      requiresAuth: true,
      isAdmin: true
    }
  },
  {
    path: '/admin/questions/:quizId',
    name: 'AdminQuestions',
    component: QuestionView,
    meta: {
      requiresAuth: true,
      isAdmin: true
    }
  },
  {
    path: '/admin/analytics',
    name: 'AdminAnalytics',
    component: () => import('@/views/admin/AnalyticsView.vue'),
    meta: {
      requiresAuth: true,
      isAdmin: true
    }
  }
]
  
export default admin