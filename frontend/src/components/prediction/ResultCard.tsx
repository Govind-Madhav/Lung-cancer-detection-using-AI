import RiskBadge from './RiskBadge';
import { formatConfidenceFull, formatDateTime, formatInferenceTime } from '@/utils/format';
import type { PredictionResponse } from '@/schemas/prediction';

interface ResultCardProps {
    prediction: PredictionResponse;
}

/**
 * Result Card Component
 * 
 * NO GLASSMORPHISM - Solid white card with border.
 * 
 * CRITICAL RULES:
 * - Show confidence ONLY if prediction_status === 'SUCCESS'
 * - Never say "confirmed" or make absolute statements
 * - Use structured, neutral language
 */

const ResultCard: React.FC<ResultCardProps> = ({ prediction }) => {
    const {
        prediction_status,
        binary_result,
        binary_confidence,
        stage_result,
        stage_confidence,
        risk_level,
        inference_time_ms,
        created_at,
    } = prediction;

    // Show confidence ONLY for SUCCESS status
    const showConfidence = prediction_status === 'SUCCESS';

    return (
        <div className="bg-white border-2 border-gray-200 rounded-lg p-8 space-y-6">
            {/* Header */}
            <div className="border-b-2 border-gray-100 pb-4">
                <h2 className="text-2xl font-bold text-gray-900 mb-2">
                    Prediction Summary
                </h2>
                <p className="text-sm text-gray-600">
                    Generated on {formatDateTime(created_at)}
                </p>
            </div>

            {/* Status Badge */}
            <div className="flex items-center gap-3">
                <span className="text-gray-700 font-semibold">Status:</span>
                <span className={`px-3 py-1 rounded-lg font-semibold text-sm ${prediction_status === 'SUCCESS' ? 'bg-green-50 text-green-900 border-2 border-green-200' :
                        prediction_status === 'INCONCLUSIVE' ? 'bg-gray-50 text-gray-900 border-2 border-gray-200' :
                            'bg-red-50 text-red-900 border-2 border-red-200'
                    }`}>
                    {prediction_status}
                </span>
            </div>

            {/* Binary Result */}
            {binary_result && (
                <div className="space-y-2">
                    <div className="flex items-baseline gap-3">
                        <span className="text-gray-700 font-semibold">Binary Classification:</span>
                        <span className={`text-lg font-bold ${binary_result === 'MALIGNANT' ? 'text-red-700' : 'text-green-700'
                            }`}>
                            {binary_result}
                        </span>
                    </div>
                    {/* Confidence shown ONLY if SUCCESS */}
                    {showConfidence && binary_confidence !== null && (
                        <p className="text-gray-600 text-sm ml-4">
                            Confidence: {formatConfidenceFull(binary_confidence)}
                        </p>
                    )}
                </div>
            )}

            {/* Stage/Risk Result */}
            {stage_result && (
                <div className="space-y-2">
                    <div className="flex items-baseline gap-3">
                        <span className="text-gray-700 font-semibold">Stage/Risk Level:</span>
                        <RiskBadge riskLevel={stage_result} />
                    </div>
                    {/* Confidence shown ONLY if SUCCESS */}
                    {showConfidence && stage_confidence !== null && (
                        <p className="text-gray-600 text-sm ml-4">
                            Confidence: {formatConfidenceFull(stage_confidence)}
                        </p>
                    )}
                </div>
            )}

            {/* Overall Risk Assessment */}
            <div className="bg-gray-50 border-2 border-gray-200 rounded-lg p-4">
                <div className="flex items-baseline gap-3 mb-2">
                    <span className="text-gray-700 font-semibold">Overall Risk:</span>
                    <RiskBadge riskLevel={risk_level} />
                </div>
            </div>

            {/* Recommendation */}
            <div className="bg-blue-50 border-2 border-blue-200 rounded-lg p-4">
                <p className="font-semibold text-blue-900 mb-2">📋 Recommendation</p>
                <p className="text-blue-900 leading-relaxed">
                    {risk_level === 'HIGH' && binary_result === 'MALIGNANT' && (
                        'This result suggests a higher likelihood of malignancy. Further clinical evaluation is recommended.'
                    )}
                    {risk_level === 'MEDIUM' && (
                        'This result indicates moderate risk. Clinical correlation and follow-up imaging are recommended.'
                    )}
                    {risk_level === 'LOW' && binary_result === 'BENIGN' && (
                        'This result suggests a lower likelihood of malignancy. Routine follow-up as per clinical protocol is recommended.'
                    )}
                    {risk_level === 'INCONCLUSIVE' && (
                        'The system was unable to generate a reliable prediction. Expert radiologist review is required.'
                    )}
                </p>
                <p className="text-blue-800 text-sm mt-2 italic">
                    All results require professional medical review. This is not a diagnostic tool.
                </p>
            </div>

            {/* Performance Metrics */}
            <div className="flex items-center justify-between text-sm text-gray-600 pt-4 border-t-2 border-gray-100">
                <span>Inference Time: {formatInferenceTime(inference_time_ms)}</span>
                <span>Model ID: #{prediction.model_id}</span>
            </div>
        </div>
    );
};

export default ResultCard;
