<template>
  <div class="container py-5" style="font-family: 'Inter', sans-serif;">
    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-3">
      <div class="d-flex flex-column gap-2">
        <button class="btn btn-outline-dark btn-sm w-fit" @click="goBack">
          <i class="bi bi-arrow-left"></i> Back to Quizzes
        </button>
        <h2 class="fw-bold text-dark mb-0">Manage Questions</h2>
        <p class="text-muted mb-0">Quiz: {{ quizTitle }}</p>
        <p class="text-muted">Chapter: {{ chapter_name }}</p>
      </div>
      <button
        class="btn btn-light rounded-pill px-3 py-1 fw-medium text-dark shadow-sm"
        @click="handleAddQuestion"
        @emit="handleCloseModal"
        data-bs-toggle="modal"
        data-bs-target="#addQuestionModal"
      >
        Add Question
      </button>
    </div>

    <!-- Loading/Error -->
    <div v-if="loading" class="text-muted text-center">Loading questions...</div>
    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <!-- Question Cards -->
    <div v-else class="row g-4">
      <div v-for="question in questions" :key="question.id" class="col-12">
        <div class="p-4 shadow-sm rounded-4 border d-flex justify-content-between align-items-start">
          <!-- Question Content -->
          <div class="d-flex flex-column gap-2">
            <h5 class="mb-0 fw-bold">Q. {{ question.text }}</h5>
            <small class="text-muted">
              <div v-if="question.options?.length">
                <strong>Options:</strong>
                <ul class="mb-2 ms-3">
                  <li v-for="(opt, i) in question.options" :key="i">{{ opt }}</li>
                </ul>
              </div>
              <div><strong>Answer:</strong> {{ question.correct_answer }}</div>
              <div><strong>Marks:</strong> {{ question.marks }}</div>
            </small>
          </div>

          <!-- Actions -->
          <div class="d-flex flex-column align-items-end gap-2 ms-3">
            <button class="btn btn-sm btn-outline-primary" title="Edit" data-bs-toggle="modal"
              data-bs-target="#addQuestionModal" @click="handleEditQuestion(question)">
              <i class="bi bi-pencil"></i>
            </button>
            <button class="btn btn-sm btn-outline-danger" title="Delete" @click="handleDeleteQuestion(question.id)">
              <i class="bi bi-trash"></i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal -->
    <div class="modal fade" id="addQuestionModal" tabindex="-1" aria-labelledby="addQuestionModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ formMode === 'edit' ? 'Edit Question' : 'Add Question' }}</h5>
            <button ref="modalCloseBtn" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <AddQuestionView
              :modalCloseBtn="modalCloseBtn"
              :mode="formMode"
              :question="selectedQuestion"
              :quizId="quizId"
              @question-added="fetchQuestions"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { axiosPrivate } from '@/api/axios'
import { useToast } from 'vue-toastification'
import AddQuestionView from '@/views/admin/components/AddQuestionView.vue'
import { Modal } from 'bootstrap'

const route = useRoute()
const router = useRouter()
const toast = useToast()

const quizId = route.params.quizId

const loading = ref(true)
const error = ref(null)
const questions = ref([])
const quizTitle = ref('')
const chapter_name = ref('')
const formMode = ref('add')
const selectedQuestion = ref(null)
const modalCloseBtn = ref(null)

const handleCloseModal = () =>{
  const modalElement = document.getElementById('addQuestionModal')
  const modalInstance = Modal.getInstance(modalElement)
  if (modalInstance) {
    modalInstance.hide()
  }
}

const fetchQuestions = async () => {
  try {
    const res = await axiosPrivate.get(`/admin/questions/${quizId}`)
    questions.value = res.data.questions
    quizTitle.value = res.data.quiz_title
    chapter_name.value = res.data.chapter_name
  } catch (err) {
    error.value = 'Failed to load questions'
    toast.error(error.value)
  } finally {
    loading.value = false
  }
}

const handleDeleteQuestion = async (id) => {
  if (!confirm('Are you sure you want to delete this question?')) return
  try {
    await axiosPrivate.delete(`/admin/questions`, { data: { id } })
    questions.value = questions.value.filter((q) => q.id !== id)
    toast.success('Question deleted successfully.')
  } catch (err) {
    toast.error('Failed to delete question.')
  }
}

const handleAddQuestion = () => {
  formMode.value = 'add'
  selectedQuestion.value = null
}

const handleEditQuestion = (question) => {
  formMode.value = 'edit'
  selectedQuestion.value = { ...question }
}

const goBack = () => {
  router.push('/admin/quizzes')
}

onMounted(fetchQuestions)
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

input:focus {
  box-shadow: none;
}
</style>