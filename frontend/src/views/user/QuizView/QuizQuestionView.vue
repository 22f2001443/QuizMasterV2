<template>
  <div class="container py-4">
    <div class="mb-4">
      <h1 class="h2 fw-bold">{{ quizName }}</h1>
    </div>

    <h3 class="h5 fw-bold mt-4">Instructions</h3>
    <p>
      This mock test consists of 10 questions, with a total of 100 marks. You have 60 minutes to complete the test. Each question carries 10 marks. For multiple-choice
      questions, select the correct option. For numerical type questions, enter the numerical answer in the text box provided.
    </p>

    <h3 class="h5 fw-bold mt-4">Quiz</h3>
    <div class="row text-center my-4">
      <div class="col">
        <div class="bg-light p-3 rounded">
          <h4 class="fw-bold mb-0">{{time.hours}}</h4>
          <small>Hours</small>
        </div>
      </div>
      <div class="col">
        <div class="bg-light p-3 rounded">
          <h4 class="fw-bold mb-0">{{time.minutes}}</h4>
          <small>Minutes</small>
        </div>
      </div>
      <div class="col">
        <div class="bg-light p-3 rounded">
          <h4 class="fw-bold mb-0">{{time.seconds}}</h4>
          <small>Seconds</small>
        </div>
      </div>
    </div>

    <div v-for="(question, index) in questions" :key="index" class="mb-4">
      <p class="fw-semibold">Question {{ index + 1 }} ({{ question.marks }} marks): {{ question.text }}</p>

      <div v-if="question.type === 'MCQ'" class="mb-3">
        <div v-for="(option, i) in question.options" :key="i" class="form-check">
          <input
            class="form-check-input"
            type="radio"
            :name="'question-' + index"
            :id="'option-' + index + '-' + i"
            :value="option"
          />
          <label class="form-check-label" :for="'option-' + index + '-' + i">
            {{ option }}
          </label>
        </div>
      </div>

      <div v-else-if="question.type === 'NTA'">
        <input type="text" class="form-control" placeholder="Enter your answer" />
      </div>
    </div>

    <div class="d-flex justify-content-end gap-2">
      <!-- <button class="btn btn-light">Previous</button> -->
      <button class="btn btn-dark">Submit</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { axiosPrivate } from '@/api/axios';
import { useAuthStore } from '@/stores/authStore';
import { useToast } from 'vue-toastification';

const router = useRouter();
const authStore = useAuthStore();
const toast = useToast();

const quizSessionId = router.currentRoute.value.params.quizSessionId;
const axios = axiosPrivate;

const questions = ref([]);
const quizName = ref('');
const time = ref({ hours: 0, minutes: 0, seconds: 0 });

onMounted(async () => {
  try {
    const response = await axios.get(`/user/quiz/questions/${quizSessionId}`);
    quizName.value = response.data.quiz_name;
    time.value = {
      hours: Math.floor(response.data.time / 60),
      minutes: response.data.time % 60,
      seconds: 0
    };
    console.log('Quiz Name:', quizName);
    if (response.data && response.data.questions) {
      questions.value = response.data.questions;
      console.log('Quiz Questions:', questions.value);
    } else {
      console.error('Unexpected response format:', response.data);
      toast.error('Unexpected server response. Please try again.');
    }
  } catch (error) {
    console.error('Error fetching quiz questions:', error);
    toast.error('Failed to load quiz questions.');
  }
});

// const questions = ref([
//   { text: 'What is the capital of France?', type: 'MCQ', options: ['London', 'Paris', 'Berlin', 'Rome'] },
//   { text: 'Solve for x: 2x + 5 = 15', type: 'NTA' },
//   { text: 'What is the chemical symbol for gold?', type: 'MCQ', options: ['Au', 'Ag', 'Cu', 'Fe'] },
//   { text: 'Calculate the area of a circle with a radius of 5 cm.', type: 'NTA' },
//   { text: "Who wrote 'Romeo and Juliet'?", type: 'MCQ', options: ['Charles Dickens', 'William Shakespeare', 'Jane Austen', 'Mark Twain'] },
//   { text: 'What is the value of pi (π) to two decimal places?', type: 'NTA' },
//   { text: 'What is the largest planet in our solar system?', type: 'MCQ', options: ['Earth', 'Mars', 'Jupiter', 'Saturn'] },
//   { text: 'What is the square root of 144?', type: 'NTA' },
//   { text: 'Which country is known as the Land of the Rising Sun?', type: 'MCQ', options: ['China', 'Japan', 'South Korea', 'Thailand'] },
//   { text: 'What is the speed of light in a vacuum (in meters per second)?', type: 'NTA' }
// ])
</script>

<style scoped>
.container {
  font-family: "Be Vietnam Pro", "Noto Sans", sans-serif;
}
</style>
