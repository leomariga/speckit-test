<template>
  <div class="register-page">
    <div class="container">
      <div class="register-card">
        <div class="logo-section">
          <h1>Get Started</h1>
          <p>Create your account to start converting markdown to PDF</p>
        </div>

        <div class="features">
          <div class="feature">
            <svg class="feature-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            <span>Free plan: Up to 20 pages</span>
          </div>
          <div class="feature">
            <svg class="feature-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            <span>Print-ready PDF output</span>
          </div>
          <div class="feature">
            <svg class="feature-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            <span>Fast and secure</span>
          </div>
        </div>

        <div v-if="error" class="error-message">
          {{ error }}
        </div>

        <button @click="handleGoogleSignup" class="google-button" :disabled="loading">
          <svg class="google-icon" viewBox="0 0 24 24">
            <path
              fill="#4285F4"
              d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
            />
            <path
              fill="#34A853"
              d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
            />
            <path
              fill="#FBBC05"
              d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
            />
            <path
              fill="#EA4335"
              d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
            />
          </svg>
          <span v-if="!loading">Sign up with Gmail</span>
          <span v-else>Creating account...</span>
        </button>

        <p class="signin-link">
          Already have an account?
          <router-link to="/login">Sign in</router-link>
        </p>

        <p class="terms">
          By signing up, you agree to our Terms of Service and Privacy Policy
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';

const authStore = useAuthStore();

const loading = ref(false);
const error = ref('');

const handleGoogleSignup = () => {
  loading.value = true;
  error.value = '';
  try {
    authStore.login(); // Same OAuth flow for signup
  } catch (err: any) {
    error.value = err.message || 'Failed to initiate signup';
    loading.value = false;
  }
};
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
}

.container {
  width: 100%;
  max-width: 500px;
}

.register-card {
  background: white;
  border-radius: 12px;
  padding: 3rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

.logo-section {
  text-align: center;
  margin-bottom: 2rem;
}

.logo-section h1 {
  font-size: 2rem;
  color: #333;
  margin-bottom: 0.5rem;
}

.logo-section p {
  color: #666;
  font-size: 1rem;
}

.features {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin-bottom: 2rem;
}

.feature {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: #666;
}

.feature-icon {
  width: 20px;
  height: 20px;
  color: #4caf50;
  flex-shrink: 0;
}

.error-message {
  padding: 1rem;
  background-color: #ffebee;
  border: 1px solid #ef5350;
  border-radius: 8px;
  color: #c62828;
  margin-bottom: 1.5rem;
  text-align: center;
}

.google-button {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 1rem;
  background-color: white;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  color: #333;
  transition: all 0.2s;
  margin-bottom: 1.5rem;
}

.google-button:hover:not(:disabled) {
  border-color: #4285f4;
  box-shadow: 0 2px 8px rgba(66, 133, 244, 0.2);
}

.google-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.google-icon {
  width: 24px;
  height: 24px;
}

.signin-link {
  text-align: center;
  color: #666;
  margin-bottom: 1rem;
}

.signin-link a {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
}

.signin-link a:hover {
  text-decoration: underline;
}

.terms {
  text-align: center;
  font-size: 0.875rem;
  color: #999;
  line-height: 1.5;
}
</style>

