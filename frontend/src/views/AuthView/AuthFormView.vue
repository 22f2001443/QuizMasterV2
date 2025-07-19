<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useToast } from 'vue-toastification'
import { axiosPublic } from '@/api/axios'
import DynamicForm from './components/DynamicForm.vue'
import { APP_NAME , TAGLINE } from '@/constants/appInfo'

const route = useRoute()
const formConfig = ref(null)
const toast = useToast()
const axios = axiosPublic

const fetchFormConfig = async () => {
  try {
    const res = await axios.get(`/auth/${route.params.type}`)
    formConfig.value = res.data
  } catch (e) {
    toast.error('Form config fetch failed')
  }
}

onMounted(fetchFormConfig)

watch(() => route.params.type, () => {
  fetchFormConfig()
})
</script>

<template>
  <div class="auth-page d-flex flex-column align-items-center min-vh-100 text-dark px-3 mt-4">

    <!-- Header Logo Banner -->
    <div class="heading-banner text-white text-center px-5 pt-4 pb-5 mb-3 rounded">
      <div class="d-flex align-items-center justify-content-center mb-2">
        <img src="@/assets/logo.png" alt="Book Logo" class="me-2" style="height: 48px;" />
        <h1 class="fw-bold m-0" style="font-weight: 600 !important; font-size: 2.85rem; letter-spacing: 0.6px">{{ APP_NAME }}</h1>
      </div>
      <p class="lead m-0 mt-1" style="font-weight: 400; font-size: 1.4rem;">{{ TAGLINE }}</p>
    </div>

    <!-- Greeting Heading -->
    <h2 class="text-center mb-4 fw-bold">
      {{ formConfig?.type === 'register' ? 'Sign up' : 'Welcome back' }}
    </h2>

    <!-- Form Box -->
    <div class="form-wrapper w-100" style="max-width: 500px;">
      <DynamicForm v-if="formConfig" :form-config="formConfig" />
      <div v-else>Loading...</div>
    </div>

  </div>
</template>

<style scoped>
.heading-banner {
    width: 100%;
    font-family: 'Inter', sans-serif;
  background-color: #111;
  max-width: 630px;
  border-radius: 5rem;
}

.auth-page input,
.auth-page select {
  border-radius: 10px;
  padding: 0.75rem 1rem;
  font-size: 1rem;
}

.auth-page button {
  border-radius: 10px;
  padding: 0.6rem 1.2rem;
  font-weight: 600;
  background-color: #111;
  color: white;
  transition: background 0.3s ease;
}

.auth-page button:hover {
  background-color: #333;
}
</style>