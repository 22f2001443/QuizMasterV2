<template>
  <div class="container mt-5">
    <div class="card shadow-sm p-4">
      <h2 class="card-title mb-3">Quiz Result</h2>
      <p class="card-text mb-4 text-muted">{{ quiz_info.title }}</p>

      <!-- <div class="row mb-2">
        <div class="col-4 fw-semibold text-secondary">Quiz ID</div>
        <div class="col-8">{{ quiz_info.id }}</div>
      </div> -->
      <div class="row mb-2">
        <div class="col-4 fw-semibold text-secondary">Number of Questions</div>
        <div class="col-8">{{ quiz_info.questions_count }}</div>
      </div>
      <div class="row mb-2">
        <div class="col-4 fw-semibold text-secondary">Marks</div>
        <div class="col-8">{{ quiz_info.marks }}%</div>
      </div>
      <div class="row mb-2">
        <div class="col-4 fw-semibold text-secondary">Submitted on</div>
        <div class="col-8">{{ new Date(quiz_info.updates_on).toLocaleString('en-GB', options) }}</div>
      </div>
      <!-- <div class="row mb-2">
        <div class="col-4 fw-semibold text-secondary">Duration</div>
        <div class="col-8">{{ quiz_info.duration }}</div>
      </div> -->
      <!-- <div class="row mb-2">
        <div class="col-4 fw-semibold text-secondary">Chapter</div>
        <div class="col-8">{{ quiz_info.chapter_name }}</div>
      </div> -->
      <!-- <div class="row mb-4">
        <div class="col-4 fw-semibold text-secondary">Subject</div>
        <div class="col-8">{{ quiz_info.subject_name }}</div>
      </div> -->


      <div class="text-end">
        <button class="btn btn-dark btn-sm" @click="goHome">
          <i class="bi bi-house me-1"></i> Go to Home
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import { useRouter } from 'vue-router';
import { axiosPrivate } from '@/api/axios';

const router = useRouter();
const resultData = ref(null);
const shouldRender = ref(false); // initially false

const quiz_info = ref({
  title: '',
  marks: 0,
  questions_count: 0,
});

const goHome = () => {
  router.push({ name: 'UserDashboard' });
};

onMounted(async () => {
  await nextTick(); // wait for route state to be available

  const result_id = router.currentRoute.value.params.quizSessionId;
  console.log('Current route state:', result_id);
  if (result_id) {
    const res = await axiosPrivate.get(`/user/quiz/results/${result_id}`);
    quiz_info.value = {
      title: res.data.title,
      marks: res.data.percentage,
      questions_count: res.data.question_count,
      updates_on: res.data.updates_on,
    };
    shouldRender.value = true;
  } else {
    goHome(); // redirect if no resultData
  }
});
</script>