<template>
  <div class="account-page">
    <div class="container">
      <header class="page-header">
        <h1>My Account</h1>
        <button @click="handleLogout" class="logout-button">Logout</button>
      </header>

      <div v-if="loading" class="loading">Loading...</div>

      <div v-else-if="accountInfo" class="account-content">
        <div class="card">
          <h2>Account Information</h2>
          <div class="info-grid">
            <div class="info-item">
              <span class="label">Email:</span>
              <span class="value">{{ accountInfo.email }}</span>
            </div>
            <div class="info-item">
              <span class="label">Account Created:</span>
              <span class="value">{{ formatDate(accountInfo.account_created_at) }}</span>
            </div>
          </div>
        </div>

        <div class="card">
          <h2>Plan & Usage</h2>
          <div class="plan-badge" :class="accountInfo.plan_type">
            {{ accountInfo.plan_type.toUpperCase() }} Plan
          </div>
          
          <div class="usage-stats">
            <div class="stat">
              <div class="stat-value">{{ accountInfo.total_pages_converted }}</div>
              <div class="stat-label">Pages Converted</div>
            </div>
            <div class="stat">
              <div class="stat-value">{{ accountInfo.remaining_pages }}</div>
              <div class="stat-label">Pages Remaining</div>
            </div>
            <div class="stat">
              <div class="stat-value">{{ accountInfo.plan_limits.max }}</div>
              <div class="stat-label">Plan Limit</div>
            </div>
          </div>

          <div class="progress-bar">
            <div 
              class="progress-fill" 
              :style="{ width: progressPercentage + '%' }"
              :class="{ warning: progressPercentage > 80, danger: progressPercentage > 95 }"
            ></div>
          </div>
          <p class="progress-text">
            {{ progressPercentage }}% of plan limit used
          </p>

          <div v-if="accountInfo.plan_type === 'free'" class="upgrade-prompt">
            <p>Want more pages? Upgrade to Premium for up to 500 pages!</p>
            <button class="upgrade-button">Upgrade to Premium</button>
          </div>
        </div>

        <div class="card">
          <h2>Recent Conversions</h2>
          <div v-if="conversions.length === 0" class="empty-state">
            <p>No conversions yet. Start converting markdown to PDF!</p>
            <router-link to="/" class="convert-link">Go to Converter</router-link>
          </div>
          <div v-else class="conversions-list">
            <div 
              v-for="conversion in conversions" 
              :key="conversion.id" 
              class="conversion-item"
              :class="conversion.status"
            >
              <div class="conversion-info">
                <span class="conversion-date">{{ formatDate(conversion.converted_at) }}</span>
                <span class="conversion-name">
                  {{ conversion.input_file_name || 'Text input' }}
                </span>
                <span class="conversion-pages">{{ conversion.page_count }} pages</span>
              </div>
              <div class="conversion-status" :class="conversion.status">
                {{ conversion.status }}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="error">
        <p>Failed to load account information</p>
        <button @click="fetchAccountInfo">Retry</button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import { useConversionStore } from '../stores/conversion';
import api from '../services/api';

const router = useRouter();
const authStore = useAuthStore();
const conversionStore = useConversionStore();

const loading = ref(false);
const accountInfo = ref<any>(null);
const conversions = computed(() => conversionStore.history?.conversions || []);

const progressPercentage = computed(() => {
  if (!accountInfo.value) return 0;
  const used = accountInfo.value.total_pages_converted;
  const limit = accountInfo.value.plan_limits.max;
  return Math.min(100, Math.round((used / limit) * 100));
});

const fetchAccountInfo = async () => {
  loading.value = true;
  try {
    accountInfo.value = await api.get('/users/account');
    await conversionStore.fetchHistory();
  } catch (error) {
    console.error('Failed to fetch account info:', error);
  } finally {
    loading.value = false;
  }
};

const handleLogout = async () => {
  await authStore.logout();
  router.push('/login');
};

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
};

onMounted(() => {
  fetchAccountInfo();
});
</script>

<style scoped>
.account-page {
  min-height: 100vh;
  background-color: #f5f5f5;
  padding: 2rem;
}

.container {
  max-width: 1000px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.page-header h1 {
  font-size: 2rem;
  color: #333;
}

.logout-button {
  padding: 0.75rem 1.5rem;
  background-color: #ef5350;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  transition: background-color 0.2s;
}

.logout-button:hover {
  background-color: #d32f2f;
}

.loading {
  text-align: center;
  padding: 3rem;
  font-size: 1.2rem;
  color: #666;
}

.account-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.card {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.card h2 {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 1.5rem;
}

.info-grid {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.info-item {
  display: flex;
  justify-content: space-between;
  padding: 0.75rem 0;
  border-bottom: 1px solid #eee;
}

.info-item:last-child {
  border-bottom: none;
}

.label {
  font-weight: 600;
  color: #666;
}

.value {
  color: #333;
}

.plan-badge {
  display: inline-block;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-weight: 600;
  margin-bottom: 1.5rem;
}

.plan-badge.free {
  background-color: #e3f2fd;
  color: #1976d2;
}

.plan-badge.premium {
  background: linear-gradient(135deg, #ffd700, #ffed4e);
  color: #333;
}

.usage-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat {
  text-align: center;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #667eea;
  margin-bottom: 0.5rem;
}

.stat-label {
  font-size: 0.875rem;
  color: #666;
}

.progress-bar {
  height: 12px;
  background-color: #e0e0e0;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.progress-fill {
  height: 100%;
  background-color: #4caf50;
  transition: width 0.3s, background-color 0.3s;
}

.progress-fill.warning {
  background-color: #ff9800;
}

.progress-fill.danger {
  background-color: #f44336;
}

.progress-text {
  text-align: center;
  font-size: 0.875rem;
  color: #666;
  margin-bottom: 1.5rem;
}

.upgrade-prompt {
  padding: 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
  color: white;
  text-align: center;
}

.upgrade-prompt p {
  margin-bottom: 1rem;
}

.upgrade-button {
  padding: 0.75rem 2rem;
  background-color: white;
  color: #667eea;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  transition: transform 0.2s;
}

.upgrade-button:hover {
  transform: translateY(-2px);
}

.empty-state {
  text-align: center;
  padding: 2rem;
  color: #666;
}

.convert-link {
  display: inline-block;
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  background-color: #667eea;
  color: white;
  text-decoration: none;
  border-radius: 8px;
  transition: transform 0.2s;
}

.convert-link:hover {
  transform: translateY(-2px);
}

.conversions-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.conversion-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background-color: #f9f9f9;
  border-radius: 8px;
  border-left: 4px solid #4caf50;
}

.conversion-item.failed {
  border-left-color: #f44336;
}

.conversion-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.conversion-date {
  font-size: 0.875rem;
  color: #999;
}

.conversion-name {
  font-weight: 600;
  color: #333;
}

.conversion-pages {
  font-size: 0.875rem;
  color: #666;
}

.conversion-status {
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 600;
  text-transform: capitalize;
}

.conversion-status.success {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.conversion-status.failed {
  background-color: #ffebee;
  color: #c62828;
}

.error {
  text-align: center;
  padding: 3rem;
}

.error button {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  background-color: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
}
</style>

