<template>
  <div class="file-upload">
    <label v-if="label" class="upload-label">{{ label }}</label>
    <div class="upload-area" @click="triggerFileInput" @drop.prevent="handleDrop" @dragover.prevent>
      <input
        ref="fileInput"
        type="file"
        :accept="accept"
        @change="handleFileChange"
        class="file-input"
      />
      <div class="upload-content">
        <svg class="upload-icon" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
        </svg>
        <p v-if="!file" class="upload-text">
          Click to upload or drag and drop<br />
          <span class="upload-hint">{{ accept || 'Markdown files' }}</span>
        </p>
        <p v-else class="file-name">{{ file.name }}</p>
      </div>
    </div>
    <button v-if="file" @click.stop="clearFile" class="clear-button">Clear</button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

interface Props {
  label?: string;
  accept?: string;
}

const props = withDefaults(defineProps<Props>(), {
  accept: '.md,.markdown',
});

const emit = defineEmits<{
  (e: 'fileSelected', file: File): void;
  (e: 'fileCleared'): void;
}>();

const fileInput = ref<HTMLInputElement | null>(null);
const file = ref<File | null>(null);

const triggerFileInput = () => {
  fileInput.value?.click();
};

const handleFileChange = (event: Event) => {
  const target = event.target as HTMLInputElement;
  if (target.files && target.files[0]) {
    file.value = target.files[0];
    emit('fileSelected', target.files[0]);
  }
};

const handleDrop = (event: DragEvent) => {
  if (event.dataTransfer?.files && event.dataTransfer.files[0]) {
    file.value = event.dataTransfer.files[0];
    emit('fileSelected', event.dataTransfer.files[0]);
  }
};

const clearFile = () => {
  file.value = null;
  if (fileInput.value) {
    fileInput.value.value = '';
  }
  emit('fileCleared');
};
</script>

<style scoped>
.file-upload {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.upload-label {
  font-weight: 600;
  color: #333;
}

.upload-area {
  border: 2px dashed #ddd;
  border-radius: 8px;
  padding: 2rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
  background-color: #fafafa;
}

.upload-area:hover {
  border-color: #4285f4;
  background-color: #f0f7ff;
}

.file-input {
  display: none;
}

.upload-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.upload-icon {
  width: 48px;
  height: 48px;
  color: #999;
}

.upload-text {
  color: #666;
  line-height: 1.5;
}

.upload-hint {
  font-size: 0.875rem;
  color: #999;
}

.file-name {
  color: #4285f4;
  font-weight: 600;
}

.clear-button {
  padding: 0.5rem 1rem;
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 0.875rem;
  transition: background-color 0.2s;
}

.clear-button:hover {
  background-color: #d32f2f;
}
</style>

