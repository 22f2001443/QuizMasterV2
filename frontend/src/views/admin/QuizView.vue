<template>
  <div class="container py-5" style="font-family: 'Inter', sans-serif;">
    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-2">
      <div>
        <h2 class="fw-bold text-dark mb-0">Manage Quizzes</h2>
        <p class="text-muted">List of all quizzes</p>
      </div>
      <!-- Add Quiz Button -->
      <button class="btn btn-light rounded-pill px-3 py-1 fw-medium text-dark shadow-sm" data-bs-toggle="modal"
        data-bs-target="#addQuizModal" @click="handleAddQuiz">
        Add Quiz
      </button>
      <!-- Modal Component -->
      <AddQuizView :mode="formMode" :quiz="selectedQuiz" @quiz-added="fetchQuizzes" />
    </div>

    <!-- Search -->
    <div class="mb-4">
      <div class="input-group bg-body-tertiary shadow-sm"
        style="background-color: #f1f3f5; border: 1px solid #ced4da; border-radius: 0.375rem;">
        <span class="input-group-text bg-transparent border-0">
          <i class="bi bi-search text-muted"></i>
        </span>
        <input type="text" v-model="searchTerm" class="form-control bg-transparent border-0"
          placeholder="Search quizzes" style="padding: 0.75rem 1rem; font-size: 1rem;" />
      </div>
    </div>

    <!-- Loading/Error -->
    <div v-if="loading" class="text-center text-muted">Loading quizzes...</div>
    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>
    <div v-else-if="filteredQuizzes.length === 0" class="text-center text-muted">No quizzes found.</div>

    <!-- Quiz List -->
    <div v-else>
      <div v-for="quiz in filteredQuizzes" :key="quiz.id"
        class="d-flex justify-content-between align-items-center mb-4 p-4 shadow-sm rounded-4 border">
        <!-- Quiz Info -->
        <div class="d-flex flex-column gap-2">
          <div class="d-flex align-items-center flex-wrap gap-2">
            <h5 class="mb-0 fw-bold">{{ quiz.title }}</h5>
          </div>
          <small class="text-muted">
            <strong>Subject:</strong> {{ quiz.subject || 'N/A' }}<br />
            <strong>Chapter:</strong> {{ quiz.chapter || 'N/A' }}<br />
            <strong>Start Time:</strong> {{ formatDateTime(quiz.start_time) }}<br />
            <strong>End Time:</strong> {{ formatDateTime(quiz.expire_time) }}<br />
            <strong>Time Limit:</strong> {{ quiz.time_limit || 0 }} mins<br />
            <strong>Marks:</strong> {{ quiz.total_marks || 0 }}
          </small>
          <div class="form-check form-switch mt-2">
            <input class="form-check-input" type="checkbox" :checked="quiz.is_active" disabled />
            <label class="form-check-label">
              {{ quiz.is_active ? 'Active' : 'Inactive' }}
            </label>
          </div>
        </div>

        <!-- Actions -->
        <div class="d-flex flex-column align-items-end gap-2">
          <button class="btn btn-sm btn-outline-primary" title="Edit Quiz" data-bs-toggle="modal"
            data-bs-target="#addQuizModal" @click="handleEditQuiz(quiz)">
            <i class="bi bi-pencil"></i>
          </button>
          <button class="btn btn-sm btn-outline-danger" title="Delete Quiz" @click="handleDeleteQuiz(quiz.id)">
            <i class="bi bi-trash"></i>
          </button>
          <!-- <router-link :to="{
            path: `/admin/questions/${quiz.id}`,
            query: {
              title: quiz.title,
              chapter: quiz.chapter,
              marks: quiz.total_marks || 0,
            }
          }" -->
          <router-link
          :to="`/admin/questions/${quiz.id}`"
          class="btn btn-sm btn-outline-success" title="Go to Questions">
            <i class="bi bi-arrow-right-circle"></i>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { axiosPrivate } from '@/api/axios'
import { useToast } from 'vue-toastification'
import AddQuizView from '@/views/admin/components/QuizModalView.vue'

const toast = useToast()
const modalCloseBtn = ref(null)
const quizzes = ref([])
const loading = ref(true)
const error = ref(null)
const searchTerm = ref('')

const formMode = ref('add')
const selectedQuiz = ref(null)

const fetchQuizzes = async () => {
  try {
    const res = await axiosPrivate.get('/admin/quizzes')
    
    quizzes.value = res.data
  } catch (err) {
    error.value = 'Failed to load quizzes.'
    toast.error(error.value)
  } finally {
    loading.value = false
  }
}

onMounted(fetchQuizzes)

const filteredQuizzes = computed(() => {
  return quizzes.value.filter(
    (q) =>
      q.title?.toLowerCase().includes(searchTerm.value.toLowerCase()) ||
      q.subject_name?.toLowerCase().includes(searchTerm.value.toLowerCase())
  )
})

const handleAddQuiz = () => {
  formMode.value = 'add'
  selectedQuiz.value = null
}

const handleEditQuiz = (quiz) => {
  formMode.value = 'edit'
  selectedQuiz.value = { ...quiz }
}

const handleDeleteQuiz = async (id) => {
  if (!confirm('Are you sure you want to delete this quiz?')) return
  try {
    await axiosPrivate.delete(`/admin/quizzes`, { data: { id } })
    quizzes.value = quizzes.value.filter((q) => q.id !== id)
    toast.success('Quiz deleted successfully.')
  } catch (err) {
    toast.error('Failed to delete quiz.')
  }
}

const formatDateTime = (datetime) => {
  if (!datetime) return 'N/A'
  return new Date(datetime).toLocaleString()
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

input:focus {
  box-shadow: none;
}
</style>
