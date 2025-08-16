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

// Get current environment - force production for now
const environment = 'production'; // import.meta.env.MODE || 'development';

// Debug logging
console.log('Environment:', environment);
console.log('Import meta env:', import.meta.env);

// Export the appropriate configuration
export const API_BASE_URL = API_CONFIG[environment]?.baseURL || API_CONFIG.production.baseURL;

// Debug logging
console.log('API Base URL:', API_BASE_URL);

// API endpoints
export const API_ENDPOINTS = {
  tryOn: `${API_BASE_URL}/api/try-on`,
};

// Debug logging
console.log('API Endpoints:', API_ENDPOINTS);
