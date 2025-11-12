/**
 * Base API client for making HTTP requests to the backend.
 */
import axios, { AxiosInstance, AxiosError, AxiosRequestConfig } from 'axios';
import config from '../config';

interface ApiError {
  error: string;
  message: string;
  details?: any;
}

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: config.apiUrl,
      timeout: 30000,
      withCredentials: true, // Include cookies for auth
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Request interceptor
    this.client.interceptors.request.use(
      (config) => {
        // Add any additional headers here
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor
    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError<ApiError>) => {
        // Handle errors globally
        if (error.response) {
          const apiError: ApiError = {
            error: error.response.data?.error || 'API Error',
            message: error.response.data?.message || error.message,
            details: error.response.data?.details,
          };
          console.error('API Error:', apiError);
          return Promise.reject(apiError);
        } else if (error.request) {
          console.error('Network Error:', error.message);
          return Promise.reject({
            error: 'Network Error',
            message: 'Unable to reach the server',
          });
        } else {
          console.error('Request Error:', error.message);
          return Promise.reject({
            error: 'Request Error',
            message: error.message,
          });
        }
      }
    );
  }

  async get<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.get<T>(url, config);
    return response.data;
  }

  async post<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.post<T>(url, data, config);
    return response.data;
  }

  async put<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.put<T>(url, data, config);
    return response.data;
  }

  async delete<T = any>(url: string, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.delete<T>(url, config);
    return response.data;
  }

  async patch<T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> {
    const response = await this.client.patch<T>(url, data, config);
    return response.data;
  }
}

export const api = new ApiClient();
export default api;

