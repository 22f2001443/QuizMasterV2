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
      <div class="d-flex justify-content-between align-items-center mt-4 px-2">
        <h6 class="fw-semibold fs-6 mb-0">Progress Overview</h6>

        <button class="btn btn-sm btn-outline-primary" title="Download Progress"
          @click="handleDownloadCSV(authStore.id)">
          <i class="bi bi-download"></i>
        </button>
      </div>

      <div class="container py-4">

        <div class="table-responsive border rounded bg-light">
          <table class="table table-bordered mb-0">
            <thead class="table-light">
              <tr>
                <th scope="col">Quiz Name</th>
                <th scope="col">Subject</th>
                <th scope="col">Chapter</th>
                <th scope="col">Date</th>
                <th scope="col">Score</th>
                <!-- <th scope="col">Time Taken</th> -->
                <th scope="col">Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="quizzes.length === 0">
                <td colspan="6" class="text-center text-muted py-3">No quiz data available.</td>
              </tr>
              <tr v-for="quiz in quizzes" :key="quiz.name">
                <td>{{ quiz.name }}</td>
                <td class="text-muted">{{ quiz.subject }}</td>
                <td class="text-muted">{{ quiz.chapter }}</td>
                <td class="text-muted">{{ quiz.date }}</td>
                <td class="text-muted">{{ quiz.score }}%</td>
                <!-- <td class="text-muted">{{ quiz.time }}</td> -->
                <td>
                  <button class="btn btn-sm btn-outline-dark w-100" @click="QuizResults(quiz.id)">{{ quiz.status
                  }}</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      <h2 class="text-[#141414] text-[22px] font-bold leading-tight tracking-[-0.015em] px-4 pb-3 pt-5">Overall
        Performance</h2>
      <div class="card p-4 mb-3">
        <h6>Quiz Attempts (Last 30 Days)</h6>
        <canvas ref="scoreChart" height="180"></canvas>
      </div>
      <!-- <div v-else class="mb-3 p-4 card">
        <h6> Nothing to show</h6>
      </div> -->

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue'
import { axiosPrivate } from '@/api/axios'
import { useAuthStore } from '@/stores/authStore'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification';
import {
  Chart,
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  Title,
  CategoryScale,
  Tooltip,
  Legend
} from 'chart.js'

Chart.register(
  LineController,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Title,
  Tooltip,
  Legend
)

const router = useRouter()
const activeTab = ref('overview')
const authStore = useAuthStore()
const toast = useToast()



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
const quizzes = ref([])
const scoreChart = ref(null)

const QuizResults = (quizSessionId) => {
  // Navigate to quiz results page
  router.push({ name: 'QuizResults', params: { quizSessionId } })
}

const fetchUserProfile = async () => {
  try {
    const res = await axiosPrivate.get(`/user/profile/${authStore.id}`)
    const data = res.data

    quizzes.value = data.quizzes || []
    console.log('Quizzes:', quizzes.value)
    user.value = {
      name: data.name || 'Unknown User',
      email: data.email || 'No Email Provided',
      semester: data.semester || 'Unknown Semester',
      joinedDate: data.joinedDate || { year: '-', month: '-', day: '-' },
      overallScore: data.overallScore || 0,
      quizCount: data.quizCount || 0,
      subjectCount: data.subject_count || 0,
      dob: data.dob || 'Unknown DOB',
      quizzes: data.quizzes || []
    }

    stats.value = [
      { label: 'Overall Score (%)', value: user.value.overallScore },
      { label: 'Subjects Enrolled', value: user.value.subjectCount },
      { label: 'Quiz Taken', value: user.value.quizCount }
    ]
  } catch (err) {
    console.error('Failed to load profile:', err)
  }
}

const handleDownloadCSV = async (userId) => {
  try {
    const response = await axiosPrivate.get(`user/download/progress/${userId}`, {
      responseType: 'blob'
    })

    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `progress_${userId}.csv`)
    document.body.appendChild(link)
    link.click()
  } catch (error) {
    console.error('Error downloading CSV:', error)
  }
}
const loadScoreChart = async () => {

  if (!scoreChart.value || quizzes.value.length === 0){
    console.log('scoreChart ref:', scoreChart.value)
    console.log('quizzes:', quizzes.value)

    return;
  }

  const now = new Date()
  const thirtyDaysAgo = new Date(now)
  thirtyDaysAgo.setDate(now.getDate() - 30)

  // Step 1: Filter quizzes from the last 30 days
  const recentQuizzes = quizzes.value.filter(q => {
    const quizDate = new Date(q.date)
    return quizDate >= thirtyDaysAgo && quizDate <= now
  })

  // Step 2: Aggregate number of quizzes per date
  const quizCountsByDate = {}

  recentQuizzes.forEach(q => {
    const dateStr = new Date(q.date).toISOString().split('T')[0] // e.g., '2025-07-25'
    quizCountsByDate[dateStr] = (quizCountsByDate[dateStr] || 0) + 1
  })

  // Step 3: Sort and format the data
  const sortedDates = Object.keys(quizCountsByDate).sort()
  const dataPoints = sortedDates.map(date => quizCountsByDate[date])

  // Optional: Fill in missing dates with 0
  const allDates = []
  for (let i = 0; i < 30; i++) {
    const d = new Date(now)
    d.setDate(now.getDate() - (29 - i))
    const dateStr = d.toISOString().split('T')[0]
    allDates.push(dateStr)
  }

  const filledData = allDates.map(date => quizCountsByDate[date] || 0)

  // Destroy previous chart if it exists
  if (scoreChart._instance) {
    scoreChart._instance.destroy()
  }

console.log('📊 allDates:', allDates)
console.log('📊 filledData:', filledData)

if (!scoreChart.value) return
new Chart(scoreChart.value, {
  type: 'line',
  data: {
    labels: allDates,
    datasets: [{
      label: 'Quiz Attempts (last 30 days)',
      data: filledData,
      fill: true,
      borderColor: 'rgba(0, 0, 0, 0.8)',
      backgroundColor: 'rgba(0, 0, 0, 0.1)',
      tension: 0.3,
      pointBackgroundColor: '#000',
      pointRadius: 3
    }]
  },
  options: {
    responsive: true,
    scales: {
      x: {
        ticks: { maxTicksLimit: 7 }
      },
      y: {
        beginAtZero: true,
        title: { display: true, text: 'Attempts' }
      }
    },
    plugins: {
      legend: { display: false },
      tooltip: {
        callbacks: {
          label: ctx => `${ctx.raw} attempts`
          }
        }
      }
    }

})
}

onMounted( async () => {
  try{
    await fetchUserProfile()
  }
  catch(error){
  toast.error('Error loading loading data or charts', error)
  }
})

watch(activeTab, async (newTab) => {
  if (newTab === 'progress') {
    await nextTick()
    loadScoreChart()
  }
})

</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;700;900&family=Noto+Sans:wght@400;500;700;900&display=swap");
@import "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css";
</style>