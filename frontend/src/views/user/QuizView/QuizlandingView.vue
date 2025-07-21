<template>
  <div class="container py-5" style="font-family: 'Be Vietnam Pro', 'Noto Sans', sans-serif;">
    <div class="mb-4">
      <h2 class="fw-bold display-6">Quiz: {{ quiz_info.title }}</h2>
      <p class="text-muted small">
        {{ quiz_info.description }}
      </p>
    </div>

    <div class="mb-4">
      <div class="row border-top py-3">
        <div class="col-4 text-muted small">Number of Questions</div>
        <div class="col-8 small">{{ quiz_info.questions_count }}</div>
      </div>
      <div class="row border-top py-3">
        <div class="col-4 text-muted small">Marks</div>
        <div class="col-8 small">{{ quiz_info.total_marks }}</div>
      </div>
      <div class="row border-top py-3">
        <div class="col-4 text-muted small">Duration</div>
        <div class="col-8 small">{{ quiz_info.time_limit }} minutes</div>
      </div>
      <!-- <div class="row border-top py-3">
        <div class="col-4 text-muted small">Difficulty</div>
        <div class="col-8 small">Advanced</div>
      </div> -->
      <div class="row border-top py-3">
        <div class="col-4 text-muted small">Chapter</div>
        <div class="col-8 small">{{ quiz_info.chapter_name }}</div>
      </div>
      <div class="row border-top py-3">
        <div class="col-4 text-muted small">Subject</div>
        <div class="col-8 small">{{ quiz_info.subject_name }}</div>
      </div>
    </div>

    <div class="mt-3">
      <button class="btn btn-dark btn-lg px-4" @click="startQuiz(quiz_info.id)">
        Start Quiz
      </button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';
import { axiosPrivate } from '@/api/axios';

import { useStartQuiz } from './useStartQuiz';

const router = useRouter();
const authStore = useAuthStore();
const { startQuiz } = useStartQuiz();
const quizId = router.currentRoute.value.params.quizId;

const quiz_info = ref({});
onMounted(async () => {
  try {
    const response = await axiosPrivate.get(`user/quiz/start/${quizId}`);
    quiz_info.value = response.data;
  } catch (error) {
    console.error("Error fetching quiz info:", error);
  }
});
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;700;900&family=Noto+Sans:wght@400;500;700;900&display=swap");
</style>