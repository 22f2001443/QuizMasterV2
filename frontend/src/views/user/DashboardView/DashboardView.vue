<template>
  <div class="user-dashboard container py-5 text-white">
    <div class="text-center mb-4">
      <h1 class="display-5 fw-bold">Welcome, {{ user?.name || 'User' }}</h1>
      <p class="text-muted">You're logged in as <strong>{{ user?.email }}</strong></p>
    </div>

    <div class="card bg-dark text-white shadow mx-auto" style="max-width: 400px;">
      <div class="card-body">
        <h5 class="card-title">User Details</h5>
        <p class="card-text"><strong>Name:</strong> {{ user?.name }}</p>
        <p class="card-text"><strong>Email:</strong> {{ user?.email }}</p>
        <p class="card-text"><strong>Role:</strong> {{ user?.roles?.[0] || 'User' }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import Cookies from 'js-cookie'

// You may fetch this from the cookie or API depending on your design
const user = ref(null)

onMounted(() => {
  const stored = Cookies.get('user')
  if (stored) {
    try {
      user.value = JSON.parse(stored)
    } catch (err) {
      console.error('Invalid user cookie:', err)
    }
  }
})
</script>

<style scoped>
.user-dashboard {
  min-height: 100vh;
  background-color: #000;
  font-family: 'Inter', sans-serif;
}
.card {
  border-radius: 1rem;
}
</style>