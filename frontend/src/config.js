// API Configuration
const API_CONFIG = {
  // Development environment
  development: {
    baseURL: 'http://localhost:8000',
  },
  // Production environment - use relative URLs when served from same domain
  production: {
    baseURL: '', // Empty string for relative URLs when served from same domain
  }
};

// Get current environment
const environment = import.meta.env.MODE || 'development';

// Debug logging
console.log('Environment:', environment);
console.log('Import meta env:', import.meta.env);

// Export the appropriate configuration
export const API_BASE_URL = API_CONFIG[environment]?.baseURL || API_CONFIG.development.baseURL;

// Debug logging
console.log('API Base URL:', API_BASE_URL);

// API endpoints
export const API_ENDPOINTS = {
  tryOn: `${API_BASE_URL}/api/try-on`,
};

// Debug logging
console.log('API Endpoints:', API_ENDPOINTS);
