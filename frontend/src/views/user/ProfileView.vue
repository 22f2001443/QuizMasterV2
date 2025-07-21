<template>
  <div class="container py-4" style="font-family: 'Be Vietnam Pro', 'Noto Sans', sans-serif;">
    <div class="d-flex flex-column align-items-center">
      <i class="bi bi-person-circle text-dark" style="font-size: 6rem;"></i>
      <div class="text-center mt-2">
        <h5 class="fw-semibold mb-1 fs-5">{{ user.name }}</h5>
        <p class="text-muted mb-0 small">{{ user.email }}</p>
        <!-- <p class="text-muted mb-0 small">Enrolled in {{user.semester}}</p> -->
        <p class="text-muted small">Joined in {{ user.joinedDate.year }}</p>
      </div>
    </div>

    <!-- Tabs -->
    <ul class="nav nav-tabs mt-3 px-2 small">
      <li class="nav-item">
        <a class="nav-link fw-semibold fs-8" :style="{ color: activeTab === 'overview' ? '#000000' : '#6c757d' }"
          :class="{ active: activeTab === 'overview' }" @click="activeTab = 'overview'">Overview</a>
      </li>
      <li class="nav-item">
        <a class="nav-link fw-semibold fs-8" :style="{ color: activeTab === 'progress' ? '#000000' : '#6c757d' }"
          :class="{ active: activeTab === 'progress' }" @click="activeTab = 'progress'">Progress</a>
      </li>
    </ul>

    <!-- Overview Content -->
    <div v-if="activeTab === 'overview'" class="mt-3">
      <h6 class="fw-semibold mt-4 px-2 fs-6">Performance Summary</h6>
      <div class="row row-cols-1 row-cols-md-3 g-4 mt-2 px-2">
        <div class="col" v-for="(item, idx) in stats" :key="idx">
          <div class="card h-100 py-3 px-3" style="border: 1px solid rgba(0, 0, 0, 0.1);">
            <div class="card-body text-start p-0">
              <p class="fw-medium small mb-1">{{ item.label }}</p>
              <h5 class="fw-bold fs-5 mb-0">{{ item.value }}</h5>
            </div>
          </div>
        </div>
      </div>
      <div>
        <h6 class="fw-semibold mt-4 px-2 fs-6">Other Information</h6>
        <div class="ps-4">
        <!-- <p class="small mb-1" style="color: rgba(108, 117, 125, 1);">Email: {{ user.email }}</p> -->
        <p class="small mb-1" style="color: rgba(108, 117, 125, 1);">Semester: {{ user.semester }}</p>
        <p class="small mb-1" style="color: rgba(108, 117, 125, 1);">DOB: {{ user.dob }}</p>
        </div>
      </div>
    </div>

    <!-- Progress Content -->
    <div v-if="activeTab === 'progress'" class="mt-3">
      <h6 class="fw-semibold mt-4 px-2 fs-6">Progress Overview</h6>
      <div class="card p-3" style="border: 1px solid rgba(0, 0, 0, 0.1);">
        <p class="text-muted small">Progress chart will be displayed here.</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { axiosPrivate } from '@/api/axios'
import { useAuthStore } from '@/stores/authStore'

const activeTab = ref('overview')
const authStore = useAuthStore()
const user = ref({
  name: '',
  email: '',
  semester: '',
  joinedDate: {
    year: null,
    month: null,
    day: null
  },
  dob: '',
  overallScore: 0,
  quizCount: 0,
  subjectCount: 0
})

const stats = ref([])

const fetchUserProfile = async () => {
  try {
    const res = await axiosPrivate.get(`/user/profile/${authStore.id}`)
    const data = res.data

    user.value = {
      name: data.name || 'Unknown User',
      email: data.email || 'No Email Provided',
      semester: data.semester || 'Unknown Semester',
      joinedDate: data.joinedDate || { year: '-', month: '-', day: '-' },
      overallScore: data.overallScore || 0,
      quizCount: data.quizCount || 0,
      subjectCount: data.subject_count || 0,
      dob: data.dob || 'Unknown DOB'
    }

    stats.value = [
      { label: 'Overall Score', value: user.value.overallScore },
      { label: 'Subjects Enrolled', value: user.value.subjectCount },
      { label: 'Quiz Taken', value: user.value.quizCount }
    ]
  } catch (err) {
    console.error('Failed to load profile:', err)
  }
}

onMounted(fetchUserProfile)
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;700;900&family=Noto+Sans:wght@400;500;700;900&display=swap");
@import "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css";
</style>