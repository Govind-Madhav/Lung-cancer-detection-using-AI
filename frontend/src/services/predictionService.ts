import apiClient from './apiClient';
import type { PredictionRequest, PredictionResponse } from '@/schemas/prediction';

/**
 * Prediction Service
 * 
 * Handles all prediction-related API calls.
 */

export const createPrediction = async (
    request: PredictionRequest
): Promise<PredictionResponse> => {
    const formData = new FormData();
    formData.append('external_ref', request.external_ref);
    formData.append('file', request.file);
    formData.append('model_type', request.model_type);

    const response = await apiClient.post<PredictionResponse>('/predict', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });

    return response.data;
};

export const getPrediction = async (id: number): Promise<PredictionResponse> => {
    const response = await apiClient.get<PredictionResponse>(`/predictions/${id}`);
    return response.data;
};
