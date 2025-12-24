import { useQuery } from '@tanstack/react-query';
import { getMetrics } from '@/services/metricsService';
import Loader from '@/components/common/Loader';
import Alert from '@/components/common/Alert';

/**
 * Metrics Page - Scientific Credibility
 * 
 * Displays:
 * - Precision
 * - Recall (highlighted as most important)
 * - F1-Score
 * - Confusion Matrix (table format, NOT heatmap)
 * 
 * No performance bragging. Neutral presentation.
 */

const Metrics = () => {
    const { data: metrics, isLoading, error } = useQuery({
        queryKey: ['metrics'],
        queryFn: getMetrics,
    });

    if (isLoading) {
        return <Loader message="Loading metrics..." />;
    }

    if (error) {
        return (
            <div className="max-w-4xl mx-auto py-12">
                <Alert variant="error">
                    Failed to load metrics. Please try again later.
                </Alert>
            </div>
        );
    }

    if (!metrics) {
        return null;
    }

    const { precision, recall, f1_score, confusion_matrix } = metrics;

    return (
        <div className="max-w-4xl mx-auto py-8">
            <div className="mb-8">
                <h1 className="text-4xl font-bold text-gray-900 mb-3">
                    Model Performance Metrics
                </h1>
                <p className="text-gray-600">
                    Validation set performance for the current model version.
                </p>
            </div>

            {/* Key Metrics */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div className="bg-white border-2 border-gray-200 rounded-lg p-6">
                    <h3 className="text-sm text-gray-600 mb-1">Precision</h3>
                    <p className="text-3xl font-bold text-gray-900">
                        {(precision * 100).toFixed(1)}%
                    </p>
                </div>

                <div className="bg-white border-2 border-blue-200 rounded-lg p-6 bg-blue-50">
                    <h3 className="text-sm text-blue-800 mb-1 font-semibold">
                        Recall (Critical Metric)
                    </h3>
                    <p className="text-3xl font-bold text-blue-900">
                        {(recall * 100).toFixed(1)}%
                    </p>
                </div>

                <div className="bg-white border-2 border-gray-200 rounded-lg p-6">
                    <h3 className="text-sm text-gray-600 mb-1">F1-Score</h3>
                    <p className="text-3xl font-bold text-gray-900">
                        {(f1_score * 100).toFixed(1)}%
                    </p>
                </div>
            </div>

            {/* Confusion Matrix */}
            <div className="bg-white border-2 border-gray-200 rounded-lg p-8">
                <h2 className="text-2xl font-bold text-gray-900 mb-6">
                    Confusion Matrix
                </h2>

                <div className="overflow-x-auto">
                    <table className="w-full border-collapse">
                        <thead>
                            <tr>
                                <th className="border-2 border-gray-300 bg-gray-100 p-4"></th>
                                <th className="border-2 border-gray-300 bg-gray-100 p-4 font-semibold">
                                    Predicted Negative
                                </th>
                                <th className="border-2 border-gray-300 bg-gray-100 p-4 font-semibold">
                                    Predicted Positive
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td className="border-2 border-gray-300 bg-gray-100 p-4 font-semibold">
                                    Actual Negative
                                </td>
                                <td className="border-2 border-gray-300 p-4 text-center bg-green-50">
                                    <div className="text-2xl font-bold text-green-900">
                                        {confusion_matrix.true_negative}
                                    </div>
                                    <div className="text-xs text-green-700">True Negative</div>
                                </td>
                                <td className="border-2 border-gray-300 p-4 text-center bg-red-50">
                                    <div className="text-2xl font-bold text-red-900">
                                        {confusion_matrix.false_positive}
                                    </div>
                                    <div className="text-xs text-red-700">False Positive</div>
                                </td>
                            </tr>
                            <tr>
                                <td className="border-2 border-gray-300 bg-gray-100 p-4 font-semibold">
                                    Actual Positive
                                </td>
                                <td className="border-2 border-gray-300 p-4 text-center bg-red-50">
                                    <div className="text-2xl font-bold text-red-900">
                                        {confusion_matrix.false_negative}
                                    </div>
                                    <div className="text-xs text-red-700">False Negative</div>
                                </td>
                                <td className="border-2 border-gray-300 p-4 text-center bg-green-50">
                                    <div className="text-2xl font-bold text-green-900">
                                        {confusion_matrix.true_positive}
                                    </div>
                                    <div className="text-xs text-green-700">True Positive</div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <p className="text-sm text-gray-600 mt-6">
                    <strong>Note:</strong> Recall is prioritized in medical screening to minimize false negatives.
                </p>
            </div>
        </div>
    );
};

export default Metrics;
