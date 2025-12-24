import apiClient from './apiClient';
import type { MetricsData } from '@/schemas/prediction';

/**
 * Metrics Service
 * 
 * Retrieves model performance metrics.
 */

export const getMetrics = async (): Promise<MetricsData> => {
    const response = await apiClient.get<MetricsData>('/metrics');
    return response.data;
};
