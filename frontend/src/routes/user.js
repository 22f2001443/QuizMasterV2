import UserDashboardView from '@/views/user/DashboardView/DashboardView.vue'

const userRoutes = [
    {
    path: '/home',
    name: 'UserDashboard',
    component: UserDashboardView,
    meta: {
      requiresAuth: true,
      isAdmin: false  
    }
  }
]

export default userRoutes

