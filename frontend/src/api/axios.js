// src/api/axios.js
import axios from 'axios'
import { useAuthStore } from '@/stores/authStore'

const BASE_URL = '/api'

// Public instance
const axiosPublic = axios.create({
  baseURL: BASE_URL,
})

// Private instance
const axiosPrivate = axios.create({
  baseURL: BASE_URL,
  withCredentials: true,
})

// Request interceptor: inject token dynamically from Pinia
axiosPrivate.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore()

    if (authStore.token) {
      config.headers['Authentication-Token'] = authStore.token
    }

    return config
  },
  (error) => Promise.reject(error)
)

// Handle 401 errors globally if needed
axiosPrivate.interceptors.response.use(
  (response) => response,
  (error) => {
    return Promise.reject(error)
  }
)

export { axiosPublic, axiosPrivate }