<template>
  <div class="pdf-viewer">
    <div v-if="pdfUrl" class="viewer-container">
      <iframe :src="pdfUrl" class="pdf-iframe" />
    </div>
    <div v-else class="no-pdf">
      <p>No PDF to display</p>
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  pdfUrl?: string;
}

const props = defineProps<Props>();
</script>

<style scoped>
.pdf-viewer {
  width: 100%;
  height: 100%;
}

.viewer-container {
  width: 100%;
  height: 600px;
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
}

.pdf-iframe {
  width: 100%;
  height: 100%;
  border: none;
}

.no-pdf {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 600px;
  border: 2px dashed #ddd;
  border-radius: 8px;
  color: #999;
}
</style>

