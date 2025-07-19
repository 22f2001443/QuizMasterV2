import { createRouter, createWebHistory } from 'vue-router'

import { useAuthStore } from '@/stores/authStore'
import Home from '@/views/HomeView/HomeView.vue'
import AuthFormView from '@/views/AuthView/AuthFormView.vue'
// import Register from '@/views/RegisterView.vue'


import admin from './admin'
import userRoutes from './user'

const base = [
  {
    path: '/',
    name: 'HomePage',
    component: Home
  },
  { path: '/auth/:type',
    name: 'AuthForm',
    component: AuthFormView
  }
]
const router = createRouter({
  history: createWebHistory(),
  routes: [...base, ...admin, ...userRoutes],
})

function redirectToLoginWithLogout(auth, next) {
  auth.logout() // Force logout
  console.log(auth.isLoggedIn, auth.ssisAdmin)

  return next({ name: 'AuthForm', params: { type: 'login' } })
}

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()

  // If route requires login
  if (to.meta.requiresAuth) {
    // This is a check for authentoication
    if (!auth.isLoggedIn) {
      // If user is not logged in, redirect to login
      return redirectToLoginWithLogout(auth, next)
    }

    // If admin-only route
    if (to.meta.isAdmin === true && !auth.isAdmin) {
      return redirectToLoginWithLogout(auth, next)
    }

    // If user-only route (isAdmin false)
    if (to.meta.isAdmin === false && auth.isAdmin) {
      // Force logout
      return redirectToLoginWithLogout(auth, next)
    }
  }

  next()
})


export default router