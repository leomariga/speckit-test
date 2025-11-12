/**
 * Authentication service for handling OAuth and user session.
 */
import api from './api';
import config from '../config';

export interface User {
  id: string;
  email: string;
  plan_type: 'free' | 'premium';
  total_pages_converted: number;
  account_created_at: string;
  last_login_at?: string;
}

class AuthService {
  /**
   * Initiate Google OAuth flow
   */
  initiateGoogleAuth(): void {
    const authUrl = `${config.apiUrl}/auth/google`;
    window.location.href = authUrl;
  }

  /**
   * Get current authenticated user
   */
  async getCurrentUser(): Promise<User> {
    return await api.get<User>('/auth/me');
  }

  /**
   * Check if user is authenticated
   */
  async isAuthenticated(): Promise<boolean> {
    try {
      await this.getCurrentUser();
      return true;
    } catch {
      return false;
    }
  }

  /**
   * Logout user
   */
  async logout(): Promise<void> {
    await api.post('/auth/logout');
  }
}

export const authService = new AuthService();
export default authService;

