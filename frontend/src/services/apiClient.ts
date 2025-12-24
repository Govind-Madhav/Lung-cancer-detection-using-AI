import axios from 'axios';

/**
 * API Client Configuration
 * 
 * Configured to proxy through Vite dev server to backend.
 * Production: Update baseURL to deployed backend.
 */

const apiClient = axios.create({
    baseURL: '/api/v1',
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 60000, // 60 seconds for ML inference
});

// Request interceptor for logging (development only)
if (import.meta.env.DEV) {
    apiClient.interceptors.request.use((config) => {
        console.log(`[API] ${config.method?.toUpperCase()} ${config.url}`);
        return config;
    });
}

// Response interceptor for error handling
apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response) {
            console.error('[API Error]', error.response.status, error.response.data);
        } else if (error.request) {
            console.error('[API Error] No response received');
        } else {
            console.error('[API Error]', error.message);
        }
        return Promise.reject(error);
    }
);

export default apiClient;
