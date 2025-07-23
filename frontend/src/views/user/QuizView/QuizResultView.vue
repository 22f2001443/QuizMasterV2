<template>
<div class="container mt-5">
    <h1 class="mb-4">Quiz Details</h1>
  <div class="card p-4">
    <h2 class="card-title">{{ quiz_info.title }}</h2>
    <p class="card-text">{{ quiz_info.description }}</p>

    <div class="row border-top py-3">
      <div class="col-4 text-muted small">Quiz ID</div>
      <div class="col-8 small">{{ quiz_info.id }}</div>
    </div>
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
      <div class="col-8 small">{{ quiz_info.duration }}</div>   
    </div>
    <div class="row border-top py-3">
      <div class="col-4 text-muted small">Chapter</div>
      <div class="col-8 small">{{ quiz_info.chapter_name }}</div>
    </div>
    <div class="row border-top py-3">
      <div class="col-4 text-muted small">Subject</div>
      <div class="col-8 small">{{ quiz_info.subject_name }}</div>
    </div>      

</div>
</div>
</template>

<script setup>
import { ref } from 'vue';

const quiz_info = ref({
  title: 'Sample Quiz',
  description: 'This is a sample quiz description.',
  id: 'quiz-123',
  questions_count: 10,
  total_marks: 100,
  duration: '30 minutes',
  chapter_name: 'Chapter 1',
  subject_name: 'Mathematics'
});
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: auto;
}
.card {
  background-color: #f8f9fa;
  border-radius: 0.5rem;
}
.card-title {
  font-size: 1.5rem;
  font-weight: bold;
}
</style>