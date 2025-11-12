<template>
  <div :class="['loading-spinner', size]">
    <div class="spinner"></div>
    <span v-if="text" class="loading-text">{{ text }}</span>
  </div>
</template>

<script setup lang="ts">
interface Props {
  size?: 'small' | 'medium' | 'large';
  text?: string;
}

withDefaults(defineProps<Props>(), {
  size: 'medium',
});
</script>

<style scoped>
.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.spinner {
  border: 3px solid rgba(102, 126, 234, 0.1);
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.loading-spinner.small .spinner {
  width: 24px;
  height: 24px;
  border-width: 2px;
}

.loading-spinner.medium .spinner {
  width: 40px;
  height: 40px;
  border-width: 3px;
}

.loading-spinner.large .spinner {
  width: 60px;
  height: 60px;
  border-width: 4px;
}

.loading-text {
  color: #666;
  font-size: 0.9375rem;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>

