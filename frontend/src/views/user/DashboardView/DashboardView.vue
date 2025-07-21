<template>
  <div class="container py-4" style="font-family: 'Be Vietnam Pro', 'Noto Sans', sans-serif;">
    <!-- Welcome Section -->
    <div class="mb-4">
      <h2 class="fw-bold display-6">Welcome back, {{ info.name }}!</h2>
      <p class="text-muted small">Explore quizzes directly or browse by subject</p>
    </div>

    <!-- Search Box -->
    <div class="mb-4">
      <input
        v-model="searchTerm"
        type="text"
        class="form-control"
        placeholder="Search for quizzes"
      />
    </div>

    <!-- Subject Filter Badges -->
    <div class="mb-4">
      <h4 class="fw-bold">Registered Subjects</h4>
      <div class="d-flex flex-wrap gap-2">
        <span
          class="badge p-2"
          :class="selectedSubject === subject.name ? 'bg-primary text-white' : 'bg-light text-dark'"
          v-for="subject in info.subjects"
          :key="subject.id"
          role="button"
          @click="toggleSubjectFilter(subject.name)"
        >
          {{ subject.name }}
        </span>
      </div>
    </div>

    <!-- Quizzes Section -->
    <div class="mb-4">
      <h4 class="fw-bold">Available Quizzes</h4>

      <div v-if="filteredQuizzes.length > 0">
        <div class="card mb-3" v-for="quiz in filteredQuizzes" :key="quiz.id">
          <div class="row g-0">
            <div class="col-md-8 p-3">
              <p class="text-muted mb-1 small">Subject: {{ quiz.subject }}</p>
              <p class="text-muted mb-1 small">Chapter: {{ quiz.chapter }}</p>
              <h5 class="fw-bold mb-1">{{ quiz.name }}</h5>
              <p class="text-muted small">
                {{ quiz.question_count }} questions · {{ quiz.marks }} marks · {{ quiz.time }} minutes
              </p>
            </div>
            <div class="col-md-4 d-flex align-items-center justify-content-center">
              <button v-if="!quiz.is_attempted"
                class="btn btn-sm btn-outline-success"
                @click="() => router.push({ name: 'QuizLanding', params: { quizId: quiz.id } })"
              > Start Quiz <i class="bi bi-play-fill"></i>
              </button>
              <button v-else
                class="btn btn-sm btn-outline-secondary"
                disabled
              >
                Attempted
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="text-muted small">
        No quizzes found for the current filter.
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { axiosPrivate } from '@/api/axios'; 
import { useAuthStore } from '@/stores/authStore';
import { useRouter } from 'vue-router';

const router = useRouter();

const info = ref({ subjects: [], quizzes: [] });
const searchTerm = ref('');
const selectedSubject = ref(null);

const axios = axiosPrivate;
const authStore = useAuthStore();

onMounted(async () => {
  try {
    const response = await axios.get(`/user/dashboard/${authStore.id}`);
    info.value = response.data;
  } catch (error) {
    console.error('Error fetching user profile:', error);
  }
});

const filteredQuizzes = computed(() => {
  return info.value.quizzes.filter((quiz) => {
    const matchesSearch = quiz.name.toLowerCase().includes(searchTerm.value.toLowerCase());
    const matchesSubject = !selectedSubject.value || quiz.subject === selectedSubject.value;
    return matchesSearch && matchesSubject;
  });
});

const toggleSubjectFilter = (subjectName) => {
  selectedSubject.value = selectedSubject.value === subjectName ? null : subjectName;
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;700;900&family=Noto+Sans:wght@400;500;700;900&display=swap");
</style>