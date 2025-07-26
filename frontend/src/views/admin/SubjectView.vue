<template>
    <div class="container py-5" style="font-family: 'Inter', sans-serif;">
        <!-- Header -->
        <div>
            <div class="d-flex justify-content-between align-items-center mb-2">
                <h2 class="fw-bold text-dark mb-0">Subjects</h2>

                <!-- Add Button -->
                <button class="btn btn-light rounded-pill px-3 py-1 fw-medium text-dark shadow-sm"
                    data-bs-toggle="modal" data-bs-target="#addSubjectModal" @click="handleAddSubject">
                    Add Subject
                </button>

                <!-- Modal Component (Shared for Add and Edit) -->
                <AddSubjectView :mode="formMode" :subject="selectedSubject" @subject-added="fetchSubjects" />
            </div>
            <p class="text-muted">List of all registered subjects</p>
        </div>

        <!-- Search -->
        <div class="mb-4">
            <div class="input-group bg-body-tertiary shadow-sm"
                style="background-color: #f1f3f5; border: 1px solid #ced4da; border-radius: 0.375rem;">
                <span class="input-group-text bg-transparent border-0">
                    <i class="bi bi-search text-muted"></i>
                </span>
                <input type="text" v-model="search" class="form-control bg-transparent border-0"
                    placeholder="Search subjects" style="padding: 0.75rem 1rem; font-size: 1rem;" />
            </div>
        </div>

        <!-- Loading/Error -->
        <div v-if="loading" class="text-muted text-center mb-4">Loading subjects...</div>
        <div v-else-if="error" class="alert alert-danger">{{ error }}</div>

        <!-- Table -->
        <div v-else class="table-responsive bg-white rounded shadow-sm">
            <table class="table align-middle mb-0">
                <thead class="bg-white">

                    <tr>
                        <th class="text-dark">Subject Name</th>
                        <th class="text-dark">Subject Code</th>
                        <th class="text-dark">Department</th>
                        <th class="text-muted">Faculty</th>
                        <th class="text-muted">Semesters</th>
                        <th class="text-muted">Chapters</th>
                        <th class="text-muted">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-if="filteredSubjects.length === 0">
                        <td colspan="7" class="text-center text-muted py-3">No subjects found.</td>
                    </tr>
                    <tr v-for="(subject, index) in filteredSubjects" :key="index" class="border-top">
                        <td class="text-dark">{{ subject.name }}</td>
                        <td class="text-muted">{{ subject.code }}</td>
                        <td class="text-muted">{{ subject.department }}</td>
                        <td class="text-muted">{{ subject.faculty || '—' }}</td>
                        <td class="text-muted">{{ subject.semesters.join(', ') || '—' }}</td>
                        <td class="text-muted">{{ subject.chapters_count }}</td>
                        
                        <td>
                            <div class="d-flex gap-2">
                                <button class="btn btn-sm btn-outline-primary" title="Edit Subject"
                                    data-bs-toggle="modal" data-bs-target="#addSubjectModal"
                                    @click="handleEditSubject(subject)">
                                    <i class="bi bi-pencil"></i>
                                </button>
                                <button class="btn btn-sm btn-outline-danger" @click="handleDeleteSubject(subject.id)"
                                    title="Delete Subject">
                                    <i class="bi bi-trash"></i>
                                </button>
                                <router-link :to="`/admin/chapters/${subject.id}`" class="btn btn-sm btn-outline-success"
                                    title="Go to Chapters">
                                    <i class="bi bi-arrow-right-circle"></i>
                                </router-link>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { axiosPrivate } from '@/api/axios'
import { useToast } from 'vue-toastification'
import AddSubjectView from '@/views/admin/components/AddSubjectView.vue'

const toast = useToast()

const search = ref('')
const subjects = ref([])
const loading = ref(true)
const error = ref(null)

const selectedSubject = ref(null)
const formMode = ref('add')

const handleAddSubject = () => {
    formMode.value = 'add'
    selectedSubject.value = null
}

const handleEditSubject = (subject) => {
    //console.log('Editing subject:', subject) // This wil print the subject being edited
    formMode.value = 'edit'
    selectedSubject.value = {
    ...subject,
    semester_ids: subject.semesters.map(s => typeof s === 'object' ? s.id : s)
  }
    const modalEl = document.getElementById('addSubjectModal')
    const modal = bootstrap.Modal.getOrCreateInstance(modalEl)
    modal.show()
}

const fetchSubjects = async () => {
    try {
        const res = await axiosPrivate.get('/admin/subjects')
        subjects.value = res.data
    } catch (err) {
        console.error('Failed to fetch subjects:', err)
        error.value = 'Failed to load subjects.'
        toast.error(error.value)
    } finally {
        loading.value = false
    }
}

onMounted(fetchSubjects)

const filteredSubjects = computed(() =>
    subjects.value.filter((subject) =>
        subject.name.toLowerCase().includes(search.value.toLowerCase())
    )
)

const handleDeleteSubject = async (id) => {
    if (!confirm('Are you sure you want to delete this subject?')) return
    try {
        await axiosPrivate.delete('/admin/subjects', {
            data: { id }
        })
        subjects.value = subjects.value.filter(s => s.id !== id)
        toast.success('Subject deleted successfully')
    } catch (err) {
        console.error('Delete error:', err)
        toast.error(err.response?.data?.message || 'Failed to delete subject')
    }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

input:focus {
    box-shadow: none;
}
</style>