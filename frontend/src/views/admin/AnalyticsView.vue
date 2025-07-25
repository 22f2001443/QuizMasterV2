<template>
  <div class="container py-5" style="font-family: 'Inter', sans-serif;">
    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="fw-bold text-dark mb-0">Analytics</h2>
    </div>

    <!-- Student Distribution -->
    <div class="mb-4">
      <h3 class="h4 fw-bold mb-3">Student Distribution</h3>
      <div class="card p-4 mb-3">
        <h6>Students by Semester</h6>
        <canvas ref="semesterChart" height="180"></canvas>
      </div>
    </div>

    <!-- Performance Metrics -->
    <div class="mb-4">
      <h3 class="h4 fw-bold mb-3">Performance Metrics</h3>
      <div class="row">
        <div class="col-md-6 mb-3">
  <div class="card p-4 h-100">
    <div class="d-flex justify-content-between align-items-center mt-4 mb-2 px-2">
        <h6 class="fw-semibold fs-6 mb-0">Top 5 Performers</h6>

        <button class="btn btn-sm btn-outline-primary" title="Download Progress"
          @click="handleDownloadCSV(authStore.id)">
          <i class="bi bi-download"></i>
        </button>
      </div>
    <div class="table-responsive">
      <table class="table table-sm table-striped mb-0">
        <thead>
          <tr>
            <th></th>
            <th>Name</th>
            <th>Semester</th>
            <th>Score (%)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="leaderboard.length === 0">
            <td colspan="4" class="text-center text-muted py-3">No leaderboard data available.</td>
          </tr>
          <tr v-for="(student, index) in leaderboard" :key="student.id">
            <td>{{ index + 1 }}</td>
            <td>{{ student.name }}</td>
            <td>{{ student.semester }}</td>
            <td>{{ student.score }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</div>
        <div class="col-md-6 mb-3">
          <div class="card p-4 h-100">
            <h6>Quiz Completion Rates</h6>
            <canvas ref="completionChart" height="180"></canvas>
          </div>
        </div>
      </div>
    </div>

    <!-- Subject-wise Quiz Attempts -->
    <div>
      <h3 class="h4 fw-bold mb-3">Subject-wise Quiz Attempts</h3>
      <div class="card p-4 mb-3">
        <h6>Quiz Attempts by Subject</h6>
        <canvas ref="subjectChart" height="180"></canvas>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, nextTick } from 'vue'
import { Chart, registerables } from 'chart.js'
import { axiosPrivate } from '@/api/axios'

const axios = axiosPrivate
Chart.register(...registerables)

// Refs to canvas elements
const semesterChart = ref(null)
const completionChart = ref(null)
const subjectChart = ref(null)
const leaderboard = ref([])

const loadSemesterChart = async () => {
  const res = await axios.get('/admin/analytics/student-distribution')
  const data = res.data
  const labels = data.map(item => item.semester)
  const counts = data.map(item => item.student_count)

  if (!semesterChart.value) return
  new Chart(semesterChart.value, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Students',
        data: counts,
        backgroundColor: '#adb5bd',
        borderColor: '#495057',
        borderWidth: 1
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: { beginAtZero: true }
      }
    }
  })
}
const loadLeaderboard = async () => {
  const res = await axios.get('/admin/analytics/leaderboard')
  leaderboard.value = res.data.top_performers || []
  console.log('Leaderboard Data:', leaderboard.value)
}
// 3️⃣ Mock data for completion chart
const loadCompletionChart = async () => {
  const data = {
    completed: 120,
    incomplete: 30
  }

  if (!completionChart.value) return
  new Chart(completionChart.value, {
    type: 'bar',
    data: {
      labels: ['Completed', 'Incomplete'],
      datasets: [{
        label: 'Quizzes',
        data: [data.completed, data.incomplete],
        backgroundColor: ['#198754', '#dc3545']
      }]
    },
    options: {
      responsive: true,
      scales: {
        y: { beginAtZero: true }
      }
    }
  })
}


const loadSubjectChart = async () => {
  const res = await axios.get('/admin/analytics/subject-attempts')
  if (!res || !res.data) return
  const data = res.data
  const labels = data.map(item => item.subject_name)
  const counts = data.map(item => item.attempt_count)
  console.log('Subject Chart Data:', labels, counts)

  if (!subjectChart.value) return
  new Chart(subjectChart.value, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        label: 'Attempts',
        data: counts,
        backgroundColor: '#ffc107'
      }]
    },
    options: {
      responsive: true,
      indexAxis: 'y',
      scales: {
        x: { beginAtZero: true }
      }
    }
  })
}

// Load all charts on component mount
onMounted(async () => {
  try {
    await nextTick()
    await loadSemesterChart()
    await loadCompletionChart()
    await loadLeaderboard()
    await loadSubjectChart()
  } catch (error) {
    console.error('Error loading one or more charts:', error)
  }
})
</script>