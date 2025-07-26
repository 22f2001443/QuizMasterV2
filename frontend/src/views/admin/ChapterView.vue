<template>
  <div class="container py-5" style="font-family: 'Inter', sans-serif;">
    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-3">
      <div class="d-flex flex-column gap-2">
  <button class="btn btn-outline-dark btn-sm w-fit" @click="goBack">
    <i class="bi bi-arrow-left"></i> Back to Subjects
  </button>
  <h2 class="fw-bold text-dark mb-0">Chapters</h2>
</div>
      <button
        class="btn btn-light rounded-pill px-3 py-1 fw-medium text-dark shadow-sm"
        @click="handleAddChapter"
        data-bs-toggle="modal"
        data-bs-target="#addChapterModal"
      >
        Add Chapter
      </button>
    </div>
    <p class="text-muted mb-4">List of chapters for subject: {{ subjectName }}</p>

    <!-- Search -->
    <div class="mb-4">
      <div class="input-group shadow-sm" style="border: 1px solid #ced4da; border-radius: 0.375rem;">
        <span class="input-group-text bg-transparent border-0">
          <i class="bi bi-search text-muted"></i>
        </span>
        <input
          v-model="search"
          type="text"
          class="form-control bg-transparent border-0"
          placeholder="Search chapters"
          style="padding: 0.75rem 1rem; font-size: 1rem;"
        />
      </div>
    </div>

    <!-- Loading/Error -->
    <div v-if="loading" class="text-muted text-center">Loading chapters...</div>
    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

    <!-- Chapter Table -->
    <div v-else class="table-responsive bg-white rounded shadow-sm">
      <table class="table align-middle mb-0">
        <thead>
          <tr>
            <th>Chapter Title</th>
            <th>Description</th>
            <th>Quizzes</th>
            <th class="text-muted">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="filteredChapters.length === 0">
            <td colspan="4" class="text-center text-muted py-3">No chapters found.</td>
          </tr>
          <tr v-for="chapter in filteredChapters" :key="chapter.id" class="border-top">
            <td>{{ chapter.title }}</td>
            <td>{{ chapter.description || '—' }}</td>
            <td>{{ chapter.quizzes_count || 0 }}</td>
            <td>
              <div class="d-flex gap-2">
                <button class="btn btn-sm btn-outline-primary">
                  <i class="bi bi-pencil"></i>
                </button>
                <button 
                class="btn btn-sm btn-outline-danger"
                @click="handleDeleteChapter(chapter.id)"
                >
                  <i class="bi bi-trash"></i>
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal -->
<div class="modal fade" id="addChapterModal" tabindex="-1" aria-labelledby="addChapterModalLabel" aria-hidden="true">
  <div class="modal-dialog">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title">{{ formMode === 'edit' ? 'Edit Chapter' : 'Add Chapter' }}</h5>
        <button ref="modalCloseBtn" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
        <ChapterModalView
          :mode="formMode"
          :chapter="selectedChapter"
          :subjectId="subjectId"
          :modalCloseBtn="modalCloseBtn"
          @chapter-added="fetchChapters"
        />
      </div>
    </div>
  </div>
</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { axiosPrivate } from '@/api/axios'
import { useToast } from 'vue-toastification'
import ChapterModalView from '@/views/admin/components/ChapterModalView.vue'

const toast = useToast()
const route = useRoute()
const router = useRouter()

const subjectId = route.params.subjectId

const chapters = ref([])
const loading = ref(true)
const error = ref(null)
const search = ref('')
const subjectName = ref('')
const formMode = ref('add')
const selectedChapter = ref(null)
const modalCloseBtn = ref(null)

const fetchChapters = async () => {
  try {
    const res = await axiosPrivate.get(`/admin/chapters/${subjectId}`)
    chapters.value = res.data.chapters
    subjectName.value = res.data.subject_name
  } catch (err) {
    console.error(err)
    error.value = 'Failed to load chapters'
    toast.error(error.value)
  } finally {
    loading.value = false
  }
}

const handleDeleteChapter = async (id) => {
  console.log('Deleting chapter with ID:', id)
  if (!confirm('Are you sure you want to delete this chapter?')) return

  try {
    const res = await axiosPrivate.delete(`/admin/chapters/${subjectId}`, {
      headers: {
        'Content-Type': 'application/json'
      },
      data: { id } // send chapter id in request body
    })

    toast.success(res.data.message || 'Chapter deleted successfully!')
    await fetchChapters()
  } catch (err) {
    console.error(err)
    toast.error(err.response?.data?.message || 'Failed to delete chapter')
  }
}

const handleAddChapter = () => {
  formMode.value = 'add'
  selectedChapter.value = null
}

const goBack = () => {
  router.push('/admin/subjects/')
}

onMounted(fetchChapters)

const filteredChapters = computed(() =>
  chapters.value.filter((ch) =>
    ch.title.toLowerCase().includes(search.value.toLowerCase())
  )
)
</script>

<style scoped>
input:focus {
  box-shadow: none;
}
</style>