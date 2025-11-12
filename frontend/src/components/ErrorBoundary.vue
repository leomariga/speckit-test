<template>
  <div v-if="hasError" class="error-boundary">
    <div class="error-content">
      <svg class="error-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
      <h2>Something went wrong</h2>
      <p class="error-message">{{ errorMessage }}</p>
      <div class="error-actions">
        <button @click="resetError" class="retry-button">Try Again</button>
        <button @click="goHome" class="home-button">Go Home</button>
      </div>
    </div>
  </div>
  <slot v-else></slot>
</template>

<script setup lang="ts">
import { ref, onErrorCaptured } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const hasError = ref(false);
const errorMessage = ref('An unexpected error occurred');

onErrorCaptured((error: any) => {
  console.error('Error caught by boundary:', error);
  hasError.value = true;
  errorMessage.value = error.message || 'An unexpected error occurred';
  return false; // Prevent error from propagating
});

const resetError = () => {
  hasError.value = false;
  errorMessage.value = 'An unexpected error occurred';
};

const goHome = () => {
  resetError();
  router.push('/');
};
</script>

<style scoped>
.error-boundary {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 2rem;
}

.error-content {
  text-align: center;
  max-width: 500px;
  background: white;
  padding: 3rem 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.error-icon {
  width: 64px;
  height: 64px;
  color: #f44336;
  margin: 0 auto 1.5rem;
}

h2 {
  font-size: 1.75rem;
  color: #333;
  margin-bottom: 1rem;
}

.error-message {
  color: #666;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.error-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.retry-button,
.home-button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.retry-button {
  background-color: #667eea;
  color: white;
}

.retry-button:hover {
  background-color: #5568d3;
}

.home-button {
  background-color: #f0f0f0;
  color: #333;
}

.home-button:hover {
  background-color: #e0e0e0;
}
</style>

