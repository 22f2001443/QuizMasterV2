import UserDashboardView from '@/views/user/DashboardView/DashboardView.vue'
import UserProfileView from '@/views/user/ProfileView.vue'
import QuizLanding from '@/views/user/QuizView/QuizLandingView.vue'
import QuizQuestionsView from '@/views/user/QuizView/QuizQuestionView.vue'
import QuizResultsView from '@/views/user/QuizView/QuizResultView.vue'

const userRoutes = [
    {
    path: '/home',
    name: 'UserDashboard',
    component: UserDashboardView,
    meta: {
      requiresAuth: true,
      isAdmin: false  
    }
  },
  {
    path: '/profile',
    name: 'UserProfile',
    component: UserProfileView,
    meta: {
      requiresAuth: true,
      isAdmin: false
    }
  },
  {
    path: '/quiz/:quizId',
    name: 'QuizLanding',
    component: QuizLanding,
    meta: {
      requiresAuth: true,
      isAdmin: false
    }
  },
  {
    path: '/quiz/:quizSessionId/questions',
    name: 'Quiz',
    component: QuizQuestionsView,
    meta: {
      requiresAuth: true,
      isAdmin: false
    }
  },
  {
    path: '/quiz/result/:quizSessionId',
    name: 'QuizResults',
    component: QuizResultsView,
    meta: {
      requiresAuth: true,
      isAdmin: false
    }
  }
]

export default userRoutes

