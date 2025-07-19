<template>
  <!-- Add/Edit Subject Modal -->
  <div class="modal fade" id="addSubjectModal" tabindex="-1" aria-labelledby="addSubjectModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <!-- Modal Header -->
        <div class="modal-header">
          <h5 class="modal-title" id="addSubjectModalLabel">
            {{ mode === 'edit' ? 'Edit Subject' : 'Add New Subject' }}
          </h5>
          <button ref="modalCloseBtn" type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
        </div>

        <!-- Modal Body -->
        <div class="modal-body">
          <form @submit.prevent="handleSubmit">
            <div class="mb-3">
              <label class="form-label">Subject Name</label>
              <input v-model="subjectForm.name" type="text" class="form-control" required />
            </div>

            <div class="mb-3">
              <label class="form-label">Code</label>
              <input v-model="subjectForm.code" type="text" class="form-control" required />
            </div>

            <div class="mb-3">
              <label class="form-label">Department</label>
              <input v-model="subjectForm.department" type="text" class="form-control" required />
            </div>

            <div class="mb-3">
              <label class="form-label">Faculty (Optional)</label>
              <input v-model="subjectForm.faculty" type="text" class="form-control" />
            </div>

            <div class="mb-3">
              <label class="form-label">Semesters</label>
              <div class="d-flex flex-column gap-1">
                <div class="form-check" v-for="sem in semesterOptions" :key="sem.value">
                  <input
                    class="form-check-input"
                    type="checkbox"
                    :id="'sem-' + sem.value"
                    :value="sem.value"
                    v-model="subjectForm.semester_ids"
                  />
                  <label class="form-check-label" :for="'sem-' + sem.value">
                    {{ sem.label }}
                  </label>
                </div>
              </div>
            </div>

            <button type="submit" class="btn btn-dark w-100">
              {{ mode === 'edit' ? 'Update Subject' : 'Add Subject' }}
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useToast } from 'vue-toastification'
import { axiosPrivate } from '@/api/axios'

// Props
const props = defineProps({
  mode: {
    type: String,
    default: 'add' // 'add' or 'edit'
  },
  subject: {
    type: Object,
    default: null
  }
})

// Emits
const emit = defineEmits(['subject-added'])

const toast = useToast()
const modalCloseBtn = ref(null)

// Form state
const subjectForm = ref({
  name: '',
  code: '',
  department: '',
  faculty: '',
  semester_ids: []
})

const semesterOptions = ref([])

// Fetch semester options
const fetchFormConfig = async () => {
  try {
    const res = await axiosPrivate.get('/admin/subjects?form_config=true')
    const semesterField = res.data.fields.find(f => f.name === 'semester_ids')
    semesterOptions.value = semesterField?.options || []
  } catch (e) {
    toast.error('Failed to load form options')
  }
}

onMounted(fetchFormConfig)

// Watch for mode/subject change and prefill form
watch(
  () => props.subject,
  (newVal) => {
    if (props.mode === 'edit' && newVal) {
      subjectForm.value = {
        name: newVal.name || '',
        code: newVal.code || '',
        department: newVal.department || '',
        faculty: newVal.faculty || '',
        semester_ids: newVal.semester_ids || []
      }
    } else {
      subjectForm.value = {
        name: '',
        code: '',
        department: '',
        faculty: '',
        semester_ids: []
      }
    }
  },
  { immediate: true }
)

// Handle form submission
const handleSubmit = async () => {
  try {
    if (props.mode === 'edit' && props.subject?.id) {
      const res = await axiosPrivate.put('/admin/subjects', {
        ...subjectForm.value,
        id: props.subject.id
      })
      toast.success(res.data.message || 'Subject updated successfully!')
    } else {
      const res = await axiosPrivate.post('/admin/subjects', subjectForm.value)
      toast.success(res.data.message || 'Subject added successfully!')
    }

    emit('subject-added')
    emit('close-modal')  
    subjectForm.value = {
      name: '',
      code: '',
      department: '',
      faculty: '',
      semester_ids: []
    }

    modalCloseBtn.value?.click()
  } catch (err) {
    toast.error(err.response?.data?.message || `Failed to submit form ${err}`)
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

input:focus {
  box-shadow: none;
}
</style>