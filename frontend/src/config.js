// API Configuration
const API_CONFIG = {
  // Development environment
  development: {
    baseURL: 'http://localhost:8000',
  },
  // Production environment
  production: {
    baseURL: 'https://uwear-ai-virtual-try-on-clothes.onrender.com',
  }
};

// Get current environment
const environment = import.meta.env.MODE || 'development';

// Export the appropriate configuration
export const API_BASE_URL = API_CONFIG[environment]?.baseURL || API_CONFIG.production.baseURL;

// API endpoints
export const API_ENDPOINTS = {
  tryOn: `${API_BASE_URL}/api/try-on`,
  health: `${API_BASE_URL}/health`,
};
