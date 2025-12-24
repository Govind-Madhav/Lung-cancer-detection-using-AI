import { AlertCircle, CheckCircle2, XCircle, AlertTriangle } from 'lucide-react';
import type { PredictionStatus } from '@/schemas/prediction';

interface ErrorStateProps {
    status: PredictionStatus;
    title?: string;
    message?: string;
    onRetry?: () => void;
}

/**
 * Error State Component
 * 
 * Handles INCONCLUSIVE, MODEL_ERROR, INPUT_INVALID states.
 * No ambiguous rendering - deterministic UI for each state.
 */

const ErrorState: React.FC<ErrorStateProps> = ({ status, title, message, onRetry }) => {
    const config = {
        INCONCLUSIVE: {
            icon: AlertCircle,
            iconColor: 'text-gray-600',
            bgColor: 'bg-gray-50',
            borderColor: 'border-gray-200',
            title: 'Inconclusive Result',
            // LOCKED WORDING - DO NOT MODIFY
            message: 'The system was unable to generate a reliable prediction for this input. No diagnostic inference should be made from this result.',
            showRetry: false,
        },
        MODEL_ERROR: {
            icon: XCircle,
            iconColor: 'text-red-600',
            bgColor: 'bg-red-50',
            borderColor: 'border-red-200',
            title: 'Model Error',
            message: 'The prediction model encountered an error. Please try again or contact support.',
            showRetry: true,
        },
        INPUT_INVALID: {
            icon: AlertTriangle,
            iconColor: 'text-amber-600',
            bgColor: 'bg-amber-50',
            borderColor: 'border-amber-200',
            title: 'Invalid Input',
            message: 'The uploaded image could not be processed. Please ensure it is a valid CT scan.',
            showRetry: true,
        },
        SUCCESS: {
            icon: CheckCircle2,
            iconColor: 'text-green-600',
            bgColor: 'bg-green-50',
            borderColor: 'border-green-200',
            title: 'Success',
            message: '',
            showRetry: false,
        },
    };

    const state = config[status];
    const Icon = state.icon;

    return (
        <div className={`${state.bgColor} border-2 ${state.borderColor} rounded-lg p-8 text-center max-w-2xl mx-auto`}>
            <Icon className={`w-16 h-16 ${state.iconColor} mx-auto mb-4`} />
            <h2 className="text-2xl font-semibold text-gray-900 mb-3">
                {title || state.title}
            </h2>
            <p className="text-gray-700 text-lg leading-relaxed mb-6">
                {message || state.message}
            </p>
            {state.showRetry && onRetry && (
                <button
                    onClick={onRetry}
                    className="px-6 py-3 bg-medical-blue text-white rounded-lg hover:bg-blue-700 transition-colors"
                >
                    Try Again
                </button>
            )}
        </div>
    );
};

export default ErrorState;
