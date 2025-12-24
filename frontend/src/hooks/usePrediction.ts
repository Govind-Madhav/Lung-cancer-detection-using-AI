import { useMutation } from '@tanstack/react-query';
import { createPrediction } from '@/services/predictionService';
import type { PredictionRequest, PredictionResponse } from '@/schemas/prediction';

/**
 * Prediction Hook
 * 
 * Manages prediction state and API calls using React Query.
 */

export const usePrediction = () => {
    const mutation = useMutation<PredictionResponse, Error, PredictionRequest>({
        mutationFn: createPrediction,
    });

    return {
        predict: mutation.mutate,
        predictAsync: mutation.mutateAsync,
        isLoading: mutation.isPending,
        isSuccess: mutation.isSuccess,
        isError: mutation.isError,
        error: mutation.error,
        data: mutation.data,
        reset: mutation.reset,
    };
};
