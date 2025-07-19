<template>
  <div class="modal fade" id="addQuizModal" tabindex="-1" aria-labelledby="addQuizModalLabel" aria-hidden="true">
    <div class="modal-dialog">
      <div class="modal-content">
        <!-- Modal Header -->
        <div class="modal-header">
          <h5 class="modal-title">
            {{ mode === 'edit' ? 'Edit Quiz' : 'Add New Quiz' }}
          </h5>
          <button ref="modalCloseBtn" type="button" class="btn-close" data-bs-dismiss="modal" />
        </div>

        <!-- Modal Body -->
        <div class="modal-body">
          <form @submit.prevent="handleSubmit">
            <div v-for="field in formFields" :key="field.name" class="mb-3">
              <label class="form-label">{{ field.label }}</label>

              <!-- Subject dropdown -->
              <select v-if="field.name === 'subject_id'" class="form-control" v-model="form.subject_id" required>
                <option value="" disabled>Select subject</option>
                <option v-for="opt in field.options" :key="opt.value" :value="opt.value">
                  {{ opt.label }}
                </option>
              </select>

              <!-- Chapter dropdown -->
              <select
                v-else-if="field.name === 'chapter_id'"
                class="form-control"
                v-model="form.chapter_id"
                :disabled="!form.subject_id"
                required
              >
                <option value="" disabled>Select chapter</option>
                <option
                  v-for="opt in chapterOptions"
                  :key="opt.value"
                  :value="opt.value"
                >
                  {{ opt.label }}
                </option>
              </select>

              <!-- Text input -->
              <input
                v-else-if="field.type === 'text'"
                type="text"
                class="form-control"
                v-model="form[field.name]"
                :required="field.required"
              />

              <!-- Textarea -->
              <textarea
                v-else-if="field.type === 'textarea'"
                class="form-control"
                v-model="form[field.name]"
                :required="field.required"
              />

              <!-- Number -->
              <input
                v-else-if="field.type === 'number'"
                type="number"
                class="form-control"
                v-model.number="form[field.name]"
                :required="field.required"
              />

              <!-- DateTime -->
              <input
                v-else-if="field.type === 'datetime-local'"
                type="datetime-local"
                class="form-control"
                v-model="form[field.name]"
              />

              <!-- Checkbox -->
              <div v-else-if="field.type === 'checkbox'" class="form-check">
                <input type="checkbox" class="form-check-input" v-model="form[field.name]" />
              </div>
            </div>

            <button type="submit" class="btn btn-dark w-100">
              {{ mode === 'edit' ? 'Update Quiz' : 'Add Quiz' }}
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { toRef, ref, watch, onMounted } from 'vue'
import { useToast } from 'vue-toastification'
import { axiosPrivate } from '@/api/axios'

const props = defineProps({
  mode: { type: String, default: 'add' },
  quiz: { type: Object, default: null },
  modalCloseBtn: Object,
})
const emit = defineEmits(['quiz-added'])

const toast = useToast()
const modalCloseBtn = ref(null)

const form = ref({})
const formFields = ref([])
const optionsBySubject = ref({})
const chapterOptions = ref([])

const fetchFormConfig = async () => {
  try {
    const res = await axiosPrivate.get('/admin/quizzes?form_config=true')
    formFields.value = res.data.fields || []

    const chapterField = formFields.value.find(f => f.name === 'chapter_id')
    optionsBySubject.value = chapterField?.options_by_subject || {}

    // Initialize form fields with default values
    formFields.value.forEach(field => {
      form.value[field.name] = field.type === 'checkbox' ? false : ''
    })
  } catch (err) {
    toast.error('Failed to load quiz form.')
  }
}

onMounted(fetchFormConfig)

watch(
  () => form.value.subject_id,
  (newVal) => {
    chapterOptions.value = optionsBySubject.value?.[newVal] || []
    form.value.chapter_id = ''
  }
)

watch(
  () => props.quiz,
  (quiz) => {
    if (props.mode === 'edit' && quiz) {
      form.value = {
        subject_id: quiz.subject_id || '',
        chapter_id: quiz.chapter_id || '',
        title: quiz.title || '',
        description: quiz.description || '',
        time_limit: quiz.time_limit || '',
        is_active: quiz.is_active || false,
        start_time: quiz.start_time ? formatToInputDateTime(quiz.start_time) : '',
        expire_time: quiz.expire_time ? formatToInputDateTime(quiz.expire_time) : ''
      }
    }
  },
  { immediate: true }
)

function formatToInputDateTime(isoString) {
  return new Date(isoString).toISOString().slice(0, 16)
}
const handleSubmit = async () => {
  try {
    const payload = {
      ...form.value,
      time_limit: parseInt(form.value.time_limit),
      start_time: form.value.start_time ? new Date(form.value.start_time).toISOString() : null,
      expire_time: form.value.expire_time ? new Date(form.value.expire_time).toISOString() : null
    }

    let res
    if (props.mode === 'edit' && props.quiz?.id) {
      res = await axiosPrivate.put('/admin/quizzes', { ...payload, id: props.quiz.id })
      toast.success('Quiz updated successfully!')
    } else {
      res = await axiosPrivate.post('/admin/quizzes', payload)// it should return the id of the newly created quiz
      const quizId = res.data.id
      toast.success('Quiz added successfully!')
  //     // here I want to redirect to /admin/questions/${quizId} and open the AddQuestionView modal with mode 'add'
  //     await router.push({ 
  //       path: `/admin/questions/${quizId}`, 
  //       query: { openAdd: 'true' } 
  // })
    }
    emit('quiz-added')
    
    modalCloseBtn.value?.click()
  } catch (err) {
    toast.error(err.response?.data?.message || `Failed to save quiz. ${err}`)
  }
}
</script>

<style scoped>
input:focus,
textarea:focus {
  box-shadow: none;
}
</style>