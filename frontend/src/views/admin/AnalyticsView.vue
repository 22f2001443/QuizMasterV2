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
            <h6>Average Score Over Time</h6>
            <canvas ref="scoreChart" height="180"></canvas>
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
const scoreChart = ref(null)
const completionChart = ref(null)
const subjectChart = ref(null)

// 1️⃣ Real API for student distribution
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

// 2️⃣ Mock data for score chart
const loadScoreChart = async () => {
  const data = {
    labels: ["Week 1", "Week 2", "Week 3", "Week 4"],
    values: [75, 80, 78, 85]
  }

  if (!scoreChart.value) return
  new Chart(scoreChart.value, {
    type: 'line',
    data: {
      labels: data.labels,
      datasets: [{
        label: 'Avg Score',
        data: data.values,
        borderColor: '#0d6efd',
        backgroundColor: 'rgba(13,110,253,0.2)',
        fill: true,
        tension: 0.4
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

// 4️⃣ Mock data for subject chart
const loadSubjectChart = async () => {
  const data = {
    labels: ["Math", "Physics", "Stats", "CS"],
    counts: [45, 60, 30, 80]
  }

  if (!subjectChart.value) return
  new Chart(subjectChart.value, {
    type: 'bar',
    data: {
      labels: data.labels,
      datasets: [{
        label: 'Attempts',
        data: data.counts,
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

// 📦 Load all charts after DOM is ready
onMounted(async () => {
  try {
    await nextTick()
    await loadSemesterChart()
    await loadScoreChart()
    await loadCompletionChart()
    await loadSubjectChart()
  } catch (error) {
    console.error('Error loading one or more charts:', error)
  }
})
</script>