<template>
  <div class="container py-4">
    <div class="mb-4">
      <h1 class="h2 fw-bold">{{ quizName }}</h1>
    </div>

    <h3 class="h5 fw-bold mt-4">Instructions</h3>
    <p>
      This mock test consists of {{ question_count }} questions, with a total of {{ marks }} marks. You have {{
        total_time.hours > 0 ? total_time.hours + ' hours and ' : '' }}{{ total_time.minutes }} minutes to complete the
      test. For multiple-choice
      questions, select the correct option. For numerical type questions, enter the numerical answer in the text box
      provided.
    </p>

    <h3 class="h5 fw-bold mt-4">Quiz</h3>
    <div class="row text-center my-4">
      <div class="col">
        <div class="bg-light p-3 rounded">
          <h4 class="fw-bold mb-0">{{ time.hours }}</h4>
          <small>Hours</small>
        </div>
      </div>
      <div class="col">
        <div class="bg-light p-3 rounded">
          <h4 class="fw-bold mb-0">{{ time.minutes }}</h4>
          <small>Minutes</small>
        </div>
      </div>
      <div class="col">
        <div class="bg-light p-3 rounded">
          <h4 class="fw-bold mb-0">{{ time.seconds }}</h4>
          <small>Seconds</small>
        </div>
      </div>
    </div>

    <div v-for="(question, index) in questions" :key="index" class="mb-4">
      <p class="fw-semibold">Question {{ index + 1 }} ({{ question.marks }} marks): {{ question.text }}</p>

      <div v-if="question.type === 'MCQ'" class="mb-3">
        <div v-for="(option, i) in question.options" :key="i" class="form-check">
          <input class="form-check-input" type="radio" :name="'question-' + index" :id="'option-' + index + '-' + i"
            :value="option" 
            v-model="answers[index]" />
          <label class="form-check-label" :for="'option-' + index + '-' + i">
            {{ option }}
          </label>
        </div>
      </div>

      <div v-else-if="question.type === 'NTA'">
        <input type="text" class="form-control" placeholder="Enter your answer"  v-model="answers[index]" />
      </div>
    </div>

    <div class="d-flex justify-content-end gap-2">
      <!-- <button class="btn btn-light">Previous</button> -->
      <button class="btn btn-dark" @click="submitQuiz">Submit</button>
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
const question_count = ref(0);
const marks = ref(0);
const time = ref({ hours: 0, minutes: 0, seconds: 0 });
const total_time = ref({ hours: 0, minutes: 0 });
const answers = ref([]);

const submitQuiz = async () => {
  clearInterval(timerInterval.value);
  const payload = {
    user_id: authStore.id,
    quiz_session_id: quizSessionId,
    answers: questions.value.map((q, i) => ({
      question_id: q.id,
      answer: answers.value[i] || null
    }))
  };
  console.log('Submitting quiz with payload:', payload);
  try {
    await axios.post(`/user/quiz/questions/${quizSessionId}`, payload);
    toast.success('Quiz submitted successfully!');
    router.push({ name: 'ResultPage' });
  } catch (error) {
    console.error('Error submitting quiz:', error);
    toast.error(`Failed to submit quiz. ${error.response?.data?.message || 'Please try again later.'}`);
  }
};

const startTimer = () => {
  timerInterval.value = setInterval(() => {
    if (time.value.hours === 0 && time.value.minutes === 0 && time.value.seconds === 0) {
      submitQuiz();
      return;
    }

    if (time.value.seconds > 0) {
      time.value.seconds--;
    } else {
      if (time.value.minutes > 0) {
        time.value.minutes--;
        time.value.seconds = 59;
      } else if (time.value.hours > 0) {
        time.value.hours--;
        time.value.minutes = 59;
        time.value.seconds = 59;
      }
    }
  }, 1000);
};

const timerInterval = ref(null);

onMounted(async () => {
  try {
    const response = await axios.get(`/user/quiz/questions/${quizSessionId}`);
    quizName.value = response.data.quiz_name;
    question_count.value = response.data.total_questions;
    marks.value = response.data.marks;
    total_time.value = {
      hours: Math.floor(response.data.time / 60),
      minutes: response.data.time % 60
    };
    time.value = {
      hours: Math.floor(response.data.time / 60),
      minutes: response.data.time % 60,
      seconds: 0
    };
    console.log('Quiz Name:', quizName);
    if (response.data && response.data.questions) {
      startTimer();
      questions.value = response.data.questions;
      answers.value = questions.value.map(() => null);
      //console.log('Quiz Questions:', questions.value);
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
