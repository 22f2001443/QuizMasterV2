<template>
  <header class="bg-white border-bottom py-3 px-4">
    <div class="container-fluid d-flex justify-content-between align-items-center">
      <!-- Logo + Title -->
      <div class="d-flex align-items-center gap-2">
        <div class="d-flex align-items-center justify-content-center bg-secondary-subtle rounded-circle"
          style="width: 24px; height: 24px;">
          <img src="@/assets/logo.png" alt="Logo" style="width: 28px; height: 28px;" />
        </div>
        <h5 class="mb-0 fw-bold text-dark">{{ APP_NAME }}</h5>
      </div>

      <!-- Navigation -->
      <div class="d-flex align-items-center gap-3">
        <template v-if="isLoggedIn && isAdmin">
          <span v-if="route.path === '/admindashboard'" class="text-muted small me-2">Admin</span>

          <router-link v-if="route.path !== '/admin/dashboard'" to="/admin/dashboard"
            class="btn btn-link btn-sm text-decoration-none text-dark px-2">
            <!-- svg for dashboard icon -->
            <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor"
              viewBox="0 0 256 256">
              <path
                d="M218.83,103.77l-80-75.48a1.14,1.14,0,0,1-.11-.11,16,16,0,0,0-21.53,0l-.11.11L37.17,103.77A16,16,0,0,0,32,115.55V208a16,16,0,0,0,16,16H96a16,16,0,0,0,16-16V160h32v48a16,16,0,0,0,16,16h48a16,16,0,0,0,16-16V115.55A16,16,0,0,0,218.83,103.77ZM208,208H160V160a16,16,0,0,0-16-16H112a16,16,0,0,0-16,16v48H48V115.55l.11-.1L128,40l79.9,75.43.11.1Z">
              </path>
            </svg>
            Dashboard
          </router-link>

          <router-link v-if="route.path !== '/admin/dashboard' && route.path !== '/admin/users'" to="/admin/users"
            class="btn btn-link btn-sm text-decoration-none text-dark px-2">
            <!-- svg for users icon -->
            <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor"
              viewBox="0 0 256 256">
              <path
                d="M117.25,157.92a60,60,0,1,0-66.5,0A95.83,95.83,0,0,0,3.53,195.63a8,8,0,1,0,13.4,8.74,80,80,0,0,1,134.14,0,8,8,0,0,0,13.4-8.74A95.83,95.83,0,0,0,117.25,157.92ZM40,108a44,44,0,1,1,44,44A44.05,44.05,0,0,1,40,108Zm210.14,98.7a8,8,0,0,1-11.07-2.33A79.83,79.83,0,0,0,172,168a8,8,0,0,1,0-16,44,44,0,1,0-16.34-84.87,8,8,0,1,1-5.94-14.85,60,60,0,0,1,55.53,105.64,95.83,95.83,0,0,1,47.22,37.71A8,8,0,0,1,250.14,206.7Z">
              </path>
            </svg>
            Users
          </router-link>

          <router-link v-if="route.path !== '/admin/dashboard' && route.path !== '/admin/subjects' && !route.path.startsWith('/admin/chapters/')" to="/admin/subjects"
            class="btn btn-link btn-sm text-decoration-none text-dark px-2">
            <!-- svg for subjects icon -->
            <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="none" stroke="currentColor" stroke-width="15"
              viewBox="0 0 256 256">
              <path
                d="M240,64V192a16,16,0,0,1-16,16H160a24,24,0,0,0-24,24,8,8,0,0,1-16,0,24,24,0,0,0-24-24H32a16,16,0,0,1-16-16V64A16,16,0,0,1,32,48H88a32,32,0,0,1,32,32v88a8,8,0,0,0,16,0V80a32,32,0,0,1,32-32h56A16,16,0,0,1,240,64Z">
              </path>
            </svg>
            Subjects
          </router-link>

          <router-link v-if="route.path !== '/admin/dashboard' && route.path !== '/admin/quizzes'" to="/admin/quizzes"
            class="btn btn-link btn-sm text-decoration-none text-dark px-2">
            <!-- svg for quizzes icon -->
            <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="currentColor"
              viewBox="0 0 256 256">
              <path
                d="M208,32H48A16,16,0,0,0,32,48V208a16,16,0,0,0,16,16H208a16,16,0,0,0,16-16V48A16,16,0,0,0,208,32Zm-8,64H136V48h64ZM120,48V96H56V48ZM56,208V112h64v96Zm80,0V112h64v96Z" />
            </svg>
            Quizzes
          </router-link>

          <router-link v-if="route.path !== '/admin/dashboard' && route.path !== '/admin/analytics'"
            to="/admin/analytics" class="btn btn-link btn-sm text-decoration-none text-dark px-2">
            <!-- svg for analytics icon -->
            <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" fill="none" viewBox="0 0 256 256"
              stroke="currentColor" stroke-width="16">
              <rect x="40" y="40" width="72" height="72" rx="8" />
              <rect x="144" y="40" width="72" height="72" rx="8" />
              <rect x="144" y="144" width="72" height="72" rx="8" />
              <rect x="40" y="144" width="72" height="72" rx="8" />
            </svg>
            Analytics
          </router-link>

          <button class="btn btn-outline-secondary btn-sm px-3" @click="logout">Logout</button>
        </template>

        <template v-else-if="isLoggedIn && !isAdmin">
          <router-link v-if="route.path !== '/home'" to="/home"
            class="btn btn-link btn-sm text-decoration-none text-dark px-2"><i class="bi bi-house-door" style="font-size: 1rem;"></i> Home</router-link>
          <router-link v-if="route.path !== '/profile'" to="/profile"
            class="btn btn-link btn-sm text-decoration-none text-dark px-2"><i class="bi bi-person-circle" style="font-size: 1rem;"></i> Profile</router-link>
          <button class="btn btn-outline-secondary btn-sm px-3" @click="logout">Logout</button>
        </template>

        <template v-else>
          <router-link to="/auth/login" class="btn btn-outline-dark btn-sm px-3">Login</router-link>
          <router-link to="/auth/register" class="btn btn-dark btn-sm px-3">Register</router-link>
        </template>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { APP_NAME } from '@/constants/appInfo'
import { useAuthStore } from '@/stores/authStore'
import { useAuth } from '@/globalComponents/useAuth'

const authStore = useAuthStore()
const { logout } = useAuth()

const isLoggedIn = authStore.isLoggedIn
const isAdmin = authStore.isAdmin
const route = useRoute()
</script>

<style scoped>
/* No custom CSS needed with Bootstrap */
</style>