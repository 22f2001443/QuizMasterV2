<template>
  <form @submit.prevent="handleSubmit">
    <div
      v-for="field in formConfig.fields"
      :key="field.name"
      class="form-floating mb-3"
    >
      <!-- Non-select input -->
      <template v-if="field.type !== 'select'">
        <input
          :type="field.type"
          class="form-control"
          :id="field.name"
          v-model="formData[field.name]"
          :required="field.required"
          placeholder=" "
        />
        <label :for="field.name">{{ startCase(field.name) }}</label>
      </template>

      <!-- Select input -->
      <template v-else>
        <select
          class="form-select"
          :id="field.name"
          v-model="formData[field.name]"
          :required="field.required"
        >
          <option disabled value="">Select...</option>
          <option
            v-for="option in field.options"
            :value="option.value"
            :key="option.value"
          >
            {{ option.label }}
          </option>
        </select>
        <label :for="field.name">{{ startCase(field.name) }}</label>
      </template>
    </div>

    <p v-if="formConfig.type === 'register'" class="text-muted mb-3">
      By registering, you agree to our
      <router-link to="/terms" class="text-decoration-none">Terms of Service</router-link> and
      <router-link to="/privacy" class="text-decoration-none">Privacy Policy</router-link>.
    </p>
    <p v-else class="text-muted mb-3">
      Forgot your password?
      <router-link to="/auth/forgot-password" class="text-decoration-none">Reset it here</router-link>.
    </p>

    <button class="btn btn-dark w-100" type="submit">
      {{ formConfig.type === 'register' ? 'Register' : 'Login' }}
    </button>

    <div class="mt-3 text-center">
      <p v-if="formConfig.type === 'register'">
        Already have an account?
        <router-link to="/auth/login" class="text-decoration-none">Login</router-link>
      </p>
      <p v-else>
        Don't have an account?
        <router-link to="/auth/register" class="text-decoration-none">Register</router-link>
      </p>
    </div>
  </form>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import { startCase } from 'lodash'
import { axiosPublic } from '@/api/axios'
import { useAuthStore } from '@/stores/authStore'

const toast = useToast()
const router = useRouter()
const authStore = useAuthStore()
const props = defineProps({
  formConfig: Object
})

const formData = reactive({})

// Initialize form fields dynamically
props.formConfig.fields.forEach(field => {
  formData[field.name] = ''
})

const handleSubmit = async () => {
  const endpoint = props.formConfig.type === 'register'
    ? '/auth/register'
    : '/auth/login'

  try {
    const res = await axiosPublic.post(endpoint, formData)
    toast.success(res.data.message || 'Success')

    if (props.formConfig.type === 'login') {
      const { user, auth_token } = res.data

      // ✅ Save to Pinia store
      authStore.setAuthData({
        token: auth_token,
        roles: user.roles,
        name: user.name,
        email: user.email,
        id: user.id
      })

      // ✅ Redirect based on role
      if (user.roles.includes('admin')) {
        router.push('/admin/dashboard')
      } else {
        router.push('/home')
      }
    } else {
      // After registration, go to login
      router.replace('/auth/login')
    }
  } catch (err) {
    toast.error(err.response?.data?.message || 'Failed')
    router.replace('/')
  }
}
</script>

<style scoped>
/* Floating label styling */
.form-floating > label {
  color: #555;
  font-weight: 500;
  font-size: 0.95rem;
}

/* Input + Select Field Styling */
input.form-control,
select.form-select {
  border-radius: 12px;
  padding: 1rem 1rem 0.5rem 1rem;
  background-color: #fefefe;
  font-size: 1rem;
  border: 1px solid #ccc;
}

input:focus,
select:focus {
  border-color: #000;
  box-shadow: none;
}

/* Button Styling */
button[type="submit"] {
  border-radius: 12px;
  padding: 0.75rem 1rem;
  font-size: 1.05rem;
  font-weight: 600;
  background-color: #000;
  color: white;
  transition: background-color 0.3s ease;
}

button[type="submit"]:hover {
  background-color: #222;
}
</style>