<template>
  <div class="convert-page">
    <div class="container">
      <header class="page-header">
        <h1>Markdown to PDF Converter</h1>
        <p>Convert your markdown content to beautiful print-ready PDFs</p>
      </header>

      <div class="input-section">
        <div class="input-tabs">
          <button
            :class="['tab', { active: inputMode === 'text' }]"
            @click="inputMode = 'text'"
          >
            Paste Text
          </button>
          <button
            :class="['tab', { active: inputMode === 'file' }]"
            @click="inputMode = 'file'"
          >
            Upload File
          </button>
        </div>

        <div v-if="inputMode === 'text'" class="input-content">
          <MarkdownEditor v-model="markdownText" />
        </div>

        <div v-else class="input-content">
          <FileUpload @fileSelected="handleFileSelected" @fileCleared="handleFileCleared" />
        </div>
      </div>

      <div v-if="error" class="error-message">
        <svg xmlns="http://www.w3.org/2000/svg" class="error-icon" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        {{ error }}
      </div>

      <div class="actions">
        <button
          @click="convertToPdf"
          :disabled="isConverting || !hasContent"
          class="convert-button"
        >
          <span v-if="!isConverting">Convert to PDF</span>
          <span v-else class="loading">
            <span class="spinner"></span>
            Converting...
          </span>
        </button>
      </div>

      <div v-if="conversionInfo" class="conversion-info">
        <p>✓ PDF generated successfully!</p>
        <p class="page-count">{{ conversionInfo.pageCount }} page(s)</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import MarkdownEditor from '../components/MarkdownEditor.vue';
import FileUpload from '../components/FileUpload.vue';
import pdfService from '../services/pdf';

type InputMode = 'text' | 'file';

const inputMode = ref<InputMode>('text');
const markdownText = ref('');
const selectedFile = ref<File | null>(null);
const isConverting = ref(false);
const error = ref('');
const conversionInfo = ref<{ pageCount: number } | null>(null);

const hasContent = computed(() => {
  return inputMode.value === 'text' ? markdownText.value.trim().length > 0 : selectedFile.value !== null;
});

const handleFileSelected = (file: File) => {
  selectedFile.value = file;
  error.value = '';
  conversionInfo.value = null;
};

const handleFileCleared = () => {
  selectedFile.value = null;
  error.value = '';
  conversionInfo.value = null;
};

const convertToPdf = async () => {
  error.value = '';
  conversionInfo.value = null;
  isConverting.value = true;

  try {
    let markdown = '';

    if (inputMode.value === 'text') {
      markdown = markdownText.value;
    } else if (selectedFile.value) {
      // Validate file
      const validation = pdfService.validateMarkdownFile(selectedFile.value);
      if (!validation.valid) {
        error.value = validation.error || 'Invalid file';
        isConverting.value = false;
        return;
      }

      // Read file content
      try {
        markdown = await pdfService.readFileContent(selectedFile.value);
      } catch (err) {
        error.value = 'Failed to read file content';
        isConverting.value = false;
        return;
      }
    }

    if (!markdown.trim()) {
      error.value = 'Please provide markdown content';
      isConverting.value = false;
      return;
    }

    // Convert to PDF
    const result = await pdfService.convertToPdf(markdown, {
      filename: selectedFile.value?.name.replace(/\.[^/.]+$/, '') + '.pdf' || 'markdown-export.pdf',
    });

    if (result.success) {
      conversionInfo.value = {
        pageCount: result.pageCount,
      };
    } else {
      error.value = result.error || 'Conversion failed';
    }
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'An unexpected error occurred';
  } finally {
    isConverting.value = false;
  }
};
</script>

<style scoped>
.convert-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
}

.container {
  max-width: 900px;
  margin: 0 auto;
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
}

.page-header {
  text-align: center;
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 0.5rem;
}

.page-header p {
  color: #666;
  font-size: 1.1rem;
}

.input-section {
  margin-bottom: 2rem;
}

.input-tabs {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

.tab {
  flex: 1;
  padding: 0.75rem 1.5rem;
  background-color: #f5f5f5;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  color: #666;
  transition: all 0.2s;
}

.tab:hover {
  background-color: #e0e0e0;
}

.tab.active {
  background-color: #667eea;
  color: white;
}

.input-content {
  margin-top: 1rem;
}

.error-message {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  background-color: #ffebee;
  border: 1px solid #ef5350;
  border-radius: 8px;
  color: #c62828;
  margin-bottom: 1rem;
}

.error-icon {
  width: 24px;
  height: 24px;
  flex-shrink: 0;
}

.actions {
  display: flex;
  justify-content: center;
  margin: 2rem 0;
}

.convert-button {
  padding: 1rem 3rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  transition: transform 0.2s, box-shadow 0.2s;
}

.convert-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.convert-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

.conversion-info {
  text-align: center;
  padding: 1rem;
  background-color: #e8f5e9;
  border: 1px solid #4caf50;
  border-radius: 8px;
  color: #2e7d32;
}

.conversion-info p {
  margin: 0.25rem 0;
}

.page-count {
  font-weight: 600;
}
</style>

