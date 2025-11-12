/**
 * Auth store using Pinia for state management.
 */
import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import authService, { type User } from '../services/auth';

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);

  // Getters
  const isAuthenticated = computed(() => user.value !== null);
  const userEmail = computed(() => user.value?.email || '');
  const planType = computed(() => user.value?.plan_type || 'free');
  const pagesConverted = computed(() => user.value?.total_pages_converted || 0);

  // Actions
  async function fetchUser() {
    loading.value = true;
    error.value = null;
    try {
      user.value = await authService.getCurrentUser();
    } catch (err: any) {
      error.value = err.message || 'Failed to fetch user';
      user.value = null;
    } finally {
      loading.value = false;
    }
  }

  async function login() {
    authService.initiateGoogleAuth();
  }

  async function logout() {
    loading.value = true;
    error.value = null;
    try {
      await authService.logout();
      user.value = null;
    } catch (err: any) {
      error.value = err.message || 'Logout failed';
    } finally {
      loading.value = false;
    }
  }

  function clearError() {
    error.value = null;
  }

  return {
    // State
    user,
    loading,
    error,
    // Getters
    isAuthenticated,
    userEmail,
    planType,
    pagesConverted,
    // Actions
    fetchUser,
    login,
    logout,
    clearError,
  };
});

