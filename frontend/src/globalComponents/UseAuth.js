// src/composables/useAuth.js
import { axiosPrivate } from '@/api/axios'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import { useAuthStore } from '@/stores/authStore'

export function useAuth() {
  const toast = useToast()
  const router = useRouter()
  const authStore = useAuthStore()

  const logout = async () => {
    try {
      await axiosPrivate.post('/auth/logout') // optional: call Flask logout
    } catch (err) {
      // optionally log error or show toast, but don’t block logout
    }

    authStore.logout() // ✅ Reset Pinia state + localStorage

    toast.success('Logged out successfully')
    router.replace('/')
  }

  return { logout }
}