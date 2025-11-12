<template>
  <Teleport to="body">
    <div class="toast-container">
      <Transition name="toast">
        <div v-if="visible" :class="['toast', type]">
          <svg v-if="type === 'success'" class="icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          <svg v-else-if="type === 'error'" class="icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
          <svg v-else class="icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span class="message">{{ message }}</span>
          <button @click="close" class="close-button">×</button>
        </div>
      </Transition>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';

interface Props {
  message: string;
  type?: 'success' | 'error' | 'info';
  duration?: number;
  visible: boolean;
}

const props = withDefaults(defineProps<Props>(), {
  type: 'info',
  duration: 3000,
});

const emit = defineEmits<{
  (e: 'close'): void;
}>();

let timer: NodeJS.Timeout | null = null;

const close = () => {
  emit('close');
  if (timer) {
    clearTimeout(timer);
    timer = null;
  }
};

watch(() => props.visible, (newValue) => {
  if (newValue && props.duration > 0) {
    timer = setTimeout(() => {
      close();
    }, props.duration);
  }
});
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 2rem;
  right: 2rem;
  z-index: 9999;
}

.toast {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  min-width: 300px;
  max-width: 500px;
}

.toast.success {
  border-left: 4px solid #4caf50;
}

.toast.error {
  border-left: 4px solid #f44336;
}

.toast.info {
  border-left: 4px solid #2196f3;
}

.icon {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
}

.toast.success .icon {
  color: #4caf50;
}

.toast.error .icon {
  color: #f44336;
}

.toast.info .icon {
  color: #2196f3;
}

.message {
  flex: 1;
  color: #333;
  font-size: 0.9375rem;
}

.close-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #999;
  padding: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: color 0.2s;
}

.close-button:hover {
  color: #666;
}

.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}
</style>

