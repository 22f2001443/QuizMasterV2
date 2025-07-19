<template>
  <form @submit.prevent="handleSubmit">
    <div v-for="field in formFields" :key="field.name" class="mb-3">
      <!-- Text input -->
      <template v-if="field.type === 'text' && !(selectedQuestionType === 'MCQ' && field.name === 'answer')">
        <label class="form-label">{{ field.label }}</label>
        <input
          type="text"
          class="form-control"
          v-model="form[field.name]"
          :required="field.required"
        />
      </template>

      <!-- Textarea -->
      <template v-else-if="field.type === 'textarea'">
        <label class="form-label">{{ field.label }}</label>
        <textarea
          class="form-control"
          v-model="form[field.name]"
          :required="field.required"
        ></textarea>
      </template>

      <!-- Number input -->
      <template v-else-if="field.type === 'number'">
        <label class="form-label">{{ field.label }}</label>
        <input
          type="number"
          class="form-control"
          v-model.number="form[field.name]"
          :required="field.required"
        />
      </template>

      <!-- Datetime input -->
      <template v-else-if="field.type === 'datetime-local'">
        <label class="form-label">{{ field.label }}</label>
        <input
          type="datetime-local"
          class="form-control"
          v-model="form[field.name]"
          :required="field.required"
        />
      </template>

      <!-- Select dropdown -->
      <template v-else-if="field.type === 'select'">
        <label class="form-label">{{ field.label }}</label>
        <select
          class="form-control"
          v-model="form[field.name]"
          :required="field.required"
        >
          <option value="" disabled>Select {{ field.label }}</option>
          <option
            v-for="opt in field.options"
            :key="opt.value"
            :value="opt.value"
          >
            {{ opt.label }}
          </option>
        </select>
      </template>

      <!-- Checkbox -->
      <template v-else-if="field.type === 'checkbox'">
        <div class="form-check">
          <input
            type="checkbox"
            class="form-check-input"
            v-model="form[field.name]"
          />
          <label class="form-check-label">{{ field.label }}</label>
        </div>
      </template>

      <!-- MCQ Options with Radio Button -->
<div
  v-else-if="field.type === 'array' && selectedQuestionType === 'MCQ'"
  class="d-flex flex-column gap-2"
>
  <label class="form-label">{{ field.label }}</label>
  <div
    v-for="(option, index) in form.options"
    :key="index"
    class="d-flex align-items-center gap-2"
  >
    <!-- Correct Option Icon -->
    <i
      class="bi"
      :class="[
        form.answer === option ? 'bi-check-circle-fill text-success' : 'bi-circle text-muted',
        'fs-4',
        'cursor-pointer'
      ]"
      @click="setCorrectAnswer(option)"
    ></i>
    <input
      type="text"
      class="form-control"
      v-model="form.options[index]"
      :placeholder="`Option ${index + 1}`"
      :required="field.required"
    />
    <button
      type="button"
      class="btn btn-sm btn-outline-danger"
      @click="removeOption(index)"
    >
      <i class="bi bi-trash"></i>
    </button>
  </div>
  <button
    type="button"
    class="btn btn-sm btn-outline-secondary mt-2"
    @click="addOption"
  >
    Add Option
  </button>
</div>
</div>

    <button type="submit" class="btn btn-dark w-100">
      {{ mode === 'edit' ? 'Update Question' : 'Add Question' }}
    </button>
  </form>
</template>

<script setup>
import { toRef, ref, watch, onMounted, computed } from 'vue'
import { useToast } from 'vue-toastification'
import { axiosPrivate } from '@/api/axios'
import { useRoute } from 'vue-router'

const route = useRoute()
const showAddQuestionModal = toRef()

const props = defineProps({
  modalCloseBtn: Object,
  mode: { type: String, default: 'add' },
  question: { type: Object, default: null },
  quizId: { type: [String, Number], required: true }
})
const emit = defineEmits(['question-added'])

const toast = useToast()
const modalCloseBtn = toRef(props, 'modalCloseBtn')
const form = ref({})
const formFields = ref([])

const fetchFormConfig = async () => {
  try {
    const res = await axiosPrivate.get(`/admin/questions/${props.quizId}?form_config=true`)
    formFields.value = res.data.fields || []

    const questionTypeField = formFields.value.find(f => f.name === 'question_type')
    if (!form.value.question_type && questionTypeField?.options?.length) {
      form.value.question_type = questionTypeField.options[0].value
    }

    formFields.value.forEach(field => {
      form.value[field.name] =
        field.type === 'checkbox'
          ? false
          : field.type === 'array'
          ? ['']
          : form.value[field.name] || ''
    })
  } catch (err) {
    toast.error('Failed to load question form.')
  }
}

onMounted(fetchFormConfig)
onMounted(() => {
  if (route.query.open_add_modal === 'true') {
    showAddQuestionModal.value = true
  }
})
watch(
  () => props.question,
  (question) => {
    if (props.mode === 'edit' && question) {
      form.value = {
        text: question.text || '',
        options: question.options || [''],
        correct_answer: question.correct_answer || '',
        marks: question.marks || 0,
        question_type: question.question_type || 'MCQ'
      }
    }
  },
  { immediate: true }
)

const setCorrectAnswer = (option) => {
  form.value.answer = option
}

const selectedQuestionType = computed(() => form.value.question_type)

const addOption = () => {
  if (!form.value.options) form.value.options = []
  form.value.options.push('')
}

const removeOption = (index) => {
  if (form.value.options.length > 1) {
    form.value.options.splice(index, 1)
  }
}

const handleSubmit = async () => {
  try {
    const payload = {
      ...form.value,
      quiz_id: props.quizId
    }

    if (props.mode === 'edit' && props.question?.id) {
      await axiosPrivate.put(`/admin/questions/${props.quizId}`, { ...payload, id: props.question.id })
      toast.success('Question updated successfully!')
      
    } else {
      await axiosPrivate.post(`/admin/questions/${props.quizId}`, payload)
      toast.success('Question added successfully!')
    }

    emit('question-added')

    modalCloseBtn.value?.click?.() // Close the modal if using a button reference
    // Reset form
    form.value = {
      text: '', 
      options: [''],
      answer: '',
      marks: 0,
      question_type: 'MCQ'
    }
    //emit('close-modal')  
  } catch (err) {
    toast.error(err?.response?.data?.message || err?.message || 'Failed to save question.')
  }
}
</script>

<style scoped>
input:focus,
textarea:focus {
  box-shadow: none;
}
</style>