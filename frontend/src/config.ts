/**
 * Frontend configuration management.
 */

interface Config {
  apiUrl: string;
  googleClientId: string;
}

const config: Config = {
  apiUrl: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  googleClientId: import.meta.env.VITE_GOOGLE_CLIENT_ID || '',
};

// Validate required configuration
if (!config.apiUrl) {
  console.error('VITE_API_URL is not set');
}

if (!config.googleClientId) {
  console.warn('VITE_GOOGLE_CLIENT_ID is not set - OAuth will not work');
}

export default config;

