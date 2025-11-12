/**
 * Vue Router configuration.
 */
import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: () => import('../pages/ConvertPage.vue'),
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('../pages/LoginPage.vue'),
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('../pages/RegisterPage.vue'),
  },
  {
    path: '/account',
    name: 'account',
    component: () => import('../pages/AccountPage.vue'),
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation guards (optional - auth is not required for conversion in Phase 1)
router.beforeEach(async (to, from, next) => {
  // Allow navigation for now - auth will be enforced in Phase 5 for plan limits
  next();
});

export default router;

