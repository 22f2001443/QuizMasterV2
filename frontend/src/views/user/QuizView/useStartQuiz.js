// src/composables/useStartQuiz.js
import { useRouter } from 'vue-router'
import { axiosPrivate } from '@/api/axios'
import { useToast } from 'vue-toastification'
import { useAuthStore } from '@/stores/authStore'

const toast = useToast()

export function useStartQuiz() {
  const router = useRouter()
  const authStore = useAuthStore()

  const startQuiz = async (quizId) => {
    if (!confirm('Are you sure you want to start this quiz?\nOnce you start, you cannot reattempt.')) return

    try {
      // Attempt to start the quiz session
      const payload = {
        user_id: authStore.id // Ensure the user ID is included
      }
      const res = await axiosPrivate.post(`user/quiz/start/${quizId}`, payload)
      const quizSessionId = res.data.session_id || quizId

      router.push({ name: 'Quiz', params: { quizSessionId } })
    } catch (error) {
      console.error('Access denied or error starting quiz:', error)
      if (error.response?.status === 409) {
        toast.error('You have already submitted this quiz. Reattempt is not allowed.')
      } else {
        toast.error(error.response?.data?.message || 'You are not authorized to take this quiz.')
      }
    }
  }

  return { startQuiz }
}