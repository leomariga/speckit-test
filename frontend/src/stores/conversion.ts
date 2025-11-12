/**
 * Conversion store using Pinia for tracking conversions.
 */
import { defineStore } from 'pinia';
import { ref } from 'vue';
import api from '../services/api';

interface ConversionHistory {
  conversions: Array<{
    id: string;
    input_type: 'text' | 'file';
    input_file_name?: string;
    page_count: number;
    conversion_method: 'client' | 'server';
    status: 'success' | 'failed';
    error_message?: string;
    converted_at: string;
  }>;
  total: number;
  page: number;
  limit: number;
}

export const useConversionStore = defineStore('conversion', () => {
  // State
  const history = ref<ConversionHistory | null>(null);
  const loading = ref(false);
  const error = ref<string | null>(null);

  // Actions
  async function trackConversion(
    inputType: 'text' | 'file',
    pageCount: number,
    conversionMethod: 'client' | 'server' = 'client',
    inputFileName?: string,
    inputFileSize?: number
  ) {
    loading.value = true;
    error.value = null;
    try {
      const result = await api.post('/conversions', {
        input_type: inputType,
        page_count: pageCount,
        conversion_method: conversionMethod,
        input_file_name: inputFileName,
        input_file_size: inputFileSize,
      });
      return result;
    } catch (err: any) {
      error.value = err.message || 'Failed to track conversion';
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function fetchHistory(page: number = 1, limit: number = 20) {
    loading.value = true;
    error.value = null;
    try {
      history.value = await api.get<ConversionHistory>(
        `/conversions/history?page=${page}&limit=${limit}`
      );
    } catch (err: any) {
      error.value = err.message || 'Failed to fetch conversion history';
    } finally {
      loading.value = false;
    }
  }

  function clearError() {
    error.value = null;
  }

  return {
    // State
    history,
    loading,
    error,
    // Actions
    trackConversion,
    fetchHistory,
    clearError,
  };
});

