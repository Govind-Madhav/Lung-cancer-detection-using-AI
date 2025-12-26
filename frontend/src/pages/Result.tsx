import { useLocation, Link } from 'react-router-dom';
import ResultCard from '@/components/prediction/ResultCard';
import ExplainabilityViewer from '@/components/prediction/ExplainabilityViewer';
import ErrorState from '@/components/common/ErrorState';
// import Loader from '@/components/common/Loader';
import Alert from '@/components/common/Alert';
import Button from '@/components/common/Button';
import type { PredictionResponse } from '@/schemas/prediction';

/**
 * Result Page - MOST IMPORTANT PAGE
 * 
 * This page implements DETERMINISTIC UI rendering based on prediction_status.
 * 
 * PREDICTION STATUS → UI BEHAVIOR MATRIX:
 * 
 * SUCCESS: Full result + confidence + explainability
 * INCONCLUSIVE: NO risk badge, NO confidence, locked wording
 * MODEL_ERROR: ErrorState with retry guidance
 * INPUT_INVALID: Validation error, no inference shown
 * 
 * CRITICAL RULES:
 * - Confidence shown ONLY if prediction_status === 'SUCCESS'
 * - INCONCLUSIVE wording is LOCKED: "The system was unable to generate a reliable prediction..."
 * - NO glassmorphism on result cards
 */

const Result = () => {
    // const { id } = useParams<{ id: string }>();
    const location = useLocation();
    const prediction = location.state?.prediction as PredictionResponse | undefined;

    // TODO: If no state, fetch from API using id
    // const { data: prediction, isLoading } = useQuery(['prediction', id], () => getPrediction(Number(id)));

    if (!prediction) {
        return (
            <div className="max-w-4xl mx-auto py-12">
                <Alert variant="error">
                    Prediction not found. Please try again.
                </Alert>
                <Link to="/predict" className="mt-4 inline-block">
                    <Button variant="primary">New Prediction</Button>
                </Link>
            </div>
        );
    }

    /*
     * PREDICTION STATUS → UI BEHAVIOR MATRIX
     * 
     * This mapping is DETERMINISTIC and MANDATORY.
     * Do not deviate from these rules.
     */
    const { prediction_status, explainability_artifacts } = prediction;

    const renderContent = () => {
        switch (prediction_status) {
            case 'SUCCESS':
                // STATE 1: SUCCESS - Full result + confidence + explainability
                return (
                    <div className="space-y-8">
                        <ResultCard prediction={prediction} />

                        {/* Explainability Section */}
                        <div className="bg-white border-2 border-gray-200 rounded-lg p-8">
                            <h2 className="text-2xl font-bold text-gray-900 mb-6">
                                Explainability Visualization
                            </h2>
                            <ExplainabilityViewer
                                artifacts={explainability_artifacts}
                                isError={false}
                            />
                        </div>
                    </div>
                );

            case 'INCONCLUSIVE':
                // STATE 2: INCONCLUSIVE - NO risk badge, NO confidence, locked wording
                return (
                    <ErrorState
                        status="INCONCLUSIVE"
                    // Uses locked wording from ErrorState component
                    />
                );

            case 'MODEL_ERROR':
                // STATE 3: MODEL_ERROR - ErrorState with retry
                return (
                    <ErrorState
                        status="MODEL_ERROR"
                        onRetry={() => window.location.href = '/predict'}
                    />
                );

            case 'INPUT_INVALID':
                // STATE 4: INPUT_INVALID - Validation error
                return (
                    <ErrorState
                        status="INPUT_INVALID"
                        onRetry={() => window.location.href = '/predict'}
                    />
                );

            default:
                return (
                    <ErrorState
                        status="MODEL_ERROR"
                        title="Unknown Status"
                        message="An unknown prediction status was encountered."
                        onRetry={() => window.location.href = '/predict'}
                    />
                );
        }
    };

    return (
        <div className="max-w-5xl mx-auto py-8">
            {/* Header */}
            <div className="mb-8 flex items-center justify-between">
                <div>
                    <h1 className="text-4xl font-bold text-gray-900 mb-2">
                        Prediction Results
                    </h1>
                    <p className="text-gray-600">
                        Analysis ID: #{prediction.id}
                    </p>
                </div>
                <Link to="/predict">
                    <Button variant="outline">
                        New Analysis
                    </Button>
                </Link>
            </div>

            {/* Deterministic Result Rendering */}
            {renderContent()}

            {/* Footer Actions */}
            <div className="mt-8 flex justify-center">
                <Link to="/">
                    <Button variant="ghost">Return to Home</Button>
                </Link>
            </div>
        </div>
    );
};

export default Result;
