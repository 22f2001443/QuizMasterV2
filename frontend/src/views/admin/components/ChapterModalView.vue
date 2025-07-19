<template>
  <form @submit.prevent="handleSubmit">
    <div class="mb-3">
      <label class="form-label" for="chapter-title">Chapter Title</label>
      <input id="chapter-title" v-model="chapterForm.title" type="text" class="form-control" required />
    </div>

    <div class="mb-3">
      <label class="form-label" for="chapter-desc">Description</label>
      <textarea id="chapter-desc" v-model="chapterForm.description" class="form-control" rows="3"></textarea>
    </div>

    <button type="submit" class="btn btn-dark w-100">
      {{ mode === 'edit' ? 'Update Chapter' : 'Add Chapter' }}
    </button>
  </form>
</template>

<script setup>
import { toRef, ref, watch, onMounted } from 'vue'
import { useToast } from 'vue-toastification'
import { axiosPrivate } from '@/api/axios'

const props = defineProps({
  modalCloseBtn: Object,
  mode: {
    type: String,
    default: 'add'
  },
  chapter: {
    type: Object,
    default: null
  },
  subjectId: {
    type: [String, Number],
    required: true
  }
})


const emit = defineEmits(['chapter-added'])

const toast = useToast()

const chapterForm = ref({
  title: '',
  description: ''
})

// Prefill form
watch(
  () => props.chapter,
  (newVal) => {
    if (props.mode === 'edit' && newVal) {
      chapterForm.value = {
        title: newVal.title || '',
        description: newVal.description || ''
      }
    } else {
      chapterForm.value = {
        title: '',
        description: ''
      }
    }
  },
  { immediate: true }
)
const modalCloseBtn = toRef(props, 'modalCloseBtn')
const handleSubmit = async () => {
  try {
    const url = `/admin/chapters/${props.subjectId}`
    const payload = {
      ...chapterForm.value,
      subject_id: props.subjectId,
      ...(props.mode === 'edit' && props.chapter?.id ? { id: props.chapter.id } : {})
    }

    const res = props.mode === 'edit'
      ? await axiosPrivate.put(url, payload)
      : await axiosPrivate.post(url, payload)

    toast.success(res.data.message || 'Chapter saved!')

    emit('chapter-added')
    //emit('close-modal')  

    // Reset form
    chapterForm.value = {
      title: '',
      description: ''
    }

    modalCloseBtn.value?.click?.()
    // Close modal if modalCloseBtn is provided
  } catch (err) {
    toast.error(err.response?.data?.message || `Failed to submit chapter ${err}`)
  }
}
</script>

<style scoped>
input:focus,
textarea:focus {
  box-shadow: none;
}
</style>