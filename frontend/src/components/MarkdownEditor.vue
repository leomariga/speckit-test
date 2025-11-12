<template>
  <div class="markdown-editor">
    <label v-if="label" class="editor-label">{{ label }}</label>
    <textarea
      :value="modelValue"
      @input="onInput"
      :placeholder="placeholder"
      class="editor-textarea"
      :rows="rows"
    ></textarea>
  </div>
</template>

<script setup lang="ts">
interface Props {
  modelValue: string;
  label?: string;
  placeholder?: string;
  rows?: number;
}

const props = withDefaults(defineProps<Props>(), {
  placeholder: 'Enter markdown content here...',
  rows: 15,
});

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void;
}>();

const onInput = (event: Event) => {
  const target = event.target as HTMLTextAreaElement;
  emit('update:modelValue', target.value);
};
</script>

<style scoped>
.markdown-editor {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.editor-label {
  font-weight: 600;
  color: #333;
}

.editor-textarea {
  width: 100%;
  padding: 1rem;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  line-height: 1.6;
  resize: vertical;
  transition: border-color 0.2s;
}

.editor-textarea:focus {
  outline: none;
  border-color: #4285f4;
}

.editor-textarea::placeholder {
  color: #999;
}
</style>

