<template>
  <footer class="bg-dark text-white text-center py-3">
    <p class="mb-0 small">
      &copy; {{ currentYear }} {{APP_NAME}} All rights reserved.
    </p>
  </footer>
</template>

<script setup>

import { APP_NAME } from '../constants/appInfo';

const currentYear = new Date().getFullYear()
</script>

<style scoped>
footer {
  width: 100%;
  background-color: #111;
  color: #fff;
  text-align: center;
  padding: 1rem 0;
  margin: 0;
}
</style>