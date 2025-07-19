<template>
  <div class="admin-dashboard bg-white vh-100">
    <!-- Dashboard Title -->
    <div class="container py-5">
      <div class="text-start px-2 pb-4">
        <h2 class="fw-bold display-6 mb-2 text-dark">Admin Dashboard</h2>
        <p class="text-muted">Manage core functionalities like a pro...</p>
      </div>

      <!-- Dashboard Cards -->
      <div class="row g-4">
        <!-- Users -->
        <div class="col-sm-6 col-md-3">
          <div class="card h-100 border-0 shadow rounded-4 overflow-hidden">
            <div class="card-img-top bg-image" :style="cardBg(usersBg)"></div>
            <div class="card-body">
              <h6 class="fw-bold text-dark mb-1">Users</h6>
              <p class="text-muted small mb-1">Manage user accounts and permissions</p>
              <p class="text-muted small mb-2">{{ metrics.users }} users</p>
              <router-link to="/admin/users" class="btn btn-sm btn-outline-dark">View Users</router-link>
            </div>
          </div>
        </div>

        <!-- Subjects -->
        <div class="col-sm-6 col-md-3">
          <div class="card h-100 border-0 shadow rounded-4 overflow-hidden">
            <div class="card-img-top bg-image" :style="cardBg(subjectsBg)"></div>
            <div class="card-body">
              <h6 class="fw-bold text-dark mb-1">Subjects</h6>
              <p class="text-muted small mb-1">Manage subjects and categories</p>
              <p class="text-muted small mb-2">{{ metrics.subjects }} subjects</p>
              <router-link to="/admin/subjects" class="btn btn-sm btn-outline-dark">View Subjects</router-link>
            </div>
          </div>
        </div>

        <!-- Quizzes -->
        <div class="col-sm-6 col-md-3">
          <div class="card h-100 border-0 shadow rounded-4 overflow-hidden">
            <div class="card-img-top bg-image" :style="cardBg(quizzesBg)"></div>
            <div class="card-body">
              <h6 class="fw-bold text-dark mb-1">Quizzes</h6>
              <p class="text-muted small mb-1">Manage quizzes and assessments</p>
              <p class="text-muted small mb-2">{{ metrics.quizzes }} quizzes</p>
              <router-link to="/admin/quizzes" class="btn btn-sm btn-outline-dark">Manage Quizzes</router-link>
            </div>
          </div>
        </div>

        <!-- Analytics -->
        <div class="col-sm-6 col-md-3">
          <div class="card h-100 border-0 shadow rounded-4 overflow-hidden">
            <div class="card-img-top bg-image" :style="cardBg(analyticsBg)"></div>
            <div class="card-body">
              <h6 class="fw-bold text-dark mb-1">Analytics</h6>
              <p class="text-muted small mb-1">View application analytics and reports</p>
              <p class="text-muted small mb-2">{{ metrics.attempts }} participations</p>
              <router-link to="/admin/analytics" class="btn btn-sm btn-outline-dark">View Stats</router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { axiosPrivate } from '@/api/axios'

const metrics = ref({
  users: 0,
  subjects: 0,
  quizzes: 0,
  attempts: 0
})

const cardBg = (url) => `background-image: url('${url}');`

const usersBg =
  'https://lh3.googleusercontent.com/aida-public/AB6AXuAQdcqDA9pYKBRKqD_SkgqCHM6e-DYksUeoVddh2n0XOSv8mvCFEjQDC5B38ZdaqgOZRGfWsAI6By-slwWeuVq2DdnHz1gqrmuVG07D0-OVAsc-jM-rOM55nhElwMr3A99d7jiaaChieMDtdoBxjCry0oH3BtcPrjBnDsgyOar-IyR5vaQw1rp1FKWshJCzEyNLo2_wIVmNqamp1fRZ2nwIghtTkGymukaJBwl19sq4f6-6S8bXuQX-omH5jRuThg_oEWm-OiRPQew'
const subjectsBg =
  'https://lh3.googleusercontent.com/aida-public/AB6AXuCZLJUdIZGkD168kJdiq6cuauTG3tRR_9lsUCFjV4PZRdoYbWUujcBmGi2FSUxthpM17yY5E_7TTyq6WqcrPijN_UzUoaU0gRAM5jj-kk9_puurO-pDdMujK8J59j3yuA4JtVfEY7YCowIqDf9o16RqqPHd8awTW-4dPBcCEsbIGj41AebZNjAOWXdUWJBBqVkhuDz15O6kMgm9r2dGquxOj5NLrL4QghHWMS5cxrVefZrIM-M9TLPVn3TnPXElBITmYWJR7TeussA'
const quizzesBg =
  'https://lh3.googleusercontent.com/aida-public/AB6AXuAEsWa9SPC-uLsQcHlAb3gUjPdAcy5X-0bws-ZxXVRizpye3Fn1jbk8F3T8GtgQo1_Yk0FTTWs71FOgAR-zOZkgSoXu5o4w-prGFXsVp5MbfEoIb-aO0AA5nfRc2yjtz3At9dmI1YZ-CMtv3ckufDqd5l_yH0H8XmutR694cUzWqBdv6KMDKjIJsVU22ROwK4SUBSdaLKeLTe17rDueSkc3o-nGlUz7mn7D78Z-ox9rhERv-qro_8PN-2LDvxKQ0OSOF9oSniRRJWg'
const analyticsBg =
  'https://lh3.googleusercontent.com/aida-public/AB6AXuArgsUWl9pkEk65gqZ59XexRgMNVI3L2mMVuEhzwwbVd_tkRSN4S1SkyLcj8fEDRYUpponWAKkV1IHdxDtXGexccPp9QHjjrDv_3hh_RtLCeAZmWmDyR0M3FTGc7rg-3Ce_zf_feCXBv8luPk4QlQtaLbNyliCxO9hT58dJlEszq0LqZmcWkUq85PNITFoWSqTV78tNY2xLZKl6jZcs4vEpju5kaMlMIhfHPLwhJWYEzcqA-TeXWOrWnDSD4vQxQBd3qaabjPli2ko'

onMounted(async () => {
  try {
    const res = await axiosPrivate.get('/admin/metrics')
    metrics.value = {
      users: res.data.total_users,
      subjects: res.data.total_subjects,
      quizzes: res.data.total_quizzes,
      attempts: res.data.total_attempts
    }
    console.log('Metrics fetched successfully:', metrics.value)
  } catch (err) {
    console.error('Failed to fetch metrics:', err)
  }
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700;900&family=Noto+Sans:wght@400;500;700;900&display=swap');

.admin-dashboard {
  font-family: 'Inter', 'Noto Sans', sans-serif;
}

.card-img-top.bg-image {
  height: 150px;
  background-size: cover;
  background-position: center;
}

.card:hover {
  transform: translateY(-4px);
  transition: transform 0.3s ease;
}
</style>