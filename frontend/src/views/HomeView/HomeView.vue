<script setup>
import { APP_NAME, TAGLINE } from '@/constants/appInfo'
</script>

<template>
  <div class="home-container d-flex flex-column justify-content-center align-items-center text-center bg-black text-white vh-100" style="margin: 0; padding: 0;">
    
    <!-- Logo + Title -->
    <div class="mb-4 text-center">
      <img src="@/assets/logo.png" alt="Logo" class="img-fluid mb-2" style="max-height: 64px;" />
      <h1 class="display-4 fw-bold">{{ APP_NAME }}</h1>
    </div>

    <!-- Tagline -->
    <p class="lead mb-4">
      {{ TAGLINE }}
    </p>

    <!-- Action Buttons -->
    <div class="d-flex gap-3 mb-5">
      <router-link to="/auth/login" class="btn btn-light fw-bold px-4 py-2" style="border-radius: 4px;">
        Login
      </router-link>
      <router-link to="/auth/register" class="btn btn-outline-light fw-bold px-4 py-2" style="border-radius: 4px;">
        Register
      </router-link>
    </div>

  </div>
</template>

<style scoped>
.home-container {
  animation: fadeIn 1s ease-in-out;
}

@keyframes fadeIn {
  0% {
    opacity: 0;
    transform: translateY(15px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

a.btn {
  transition: all 0.3s ease;
}

a.btn:hover {
  transform: scale(1.05);
}
</style>