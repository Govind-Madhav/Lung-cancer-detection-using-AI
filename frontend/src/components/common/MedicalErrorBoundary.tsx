import React, { Component, ErrorInfo, ReactNode } from 'react';
import { AlertTriangle } from 'lucide-react';

interface Props {
    children: ReactNode;
}

interface State {
    hasError: boolean;
    error?: Error;
}

/**
 * Medical Error Boundary
 * 
 * Top-level error handling to prevent white screens.
 * Critical for medical apps: no partial results, clear error state.
 * 
 * Fallback message: "An unexpected error occurred. No medical inference was made."
 */
class MedicalErrorBoundary extends Component<Props, State> {
    constructor(props: Props) {
        super(props);
        this.state = { hasError: false };
    }

    static getDerivedStateFromError(error: Error): State {
        return { hasError: true, error };
    }

    componentDidCatch(error: Error, errorInfo: ErrorInfo) {
        console.error('[MedicalErrorBoundary] Caught error:', error, errorInfo);
    }

    render() {
        if (this.state.hasError) {
            return (
                <div className="flex items-center justify-center min-h-screen bg-medical-bg">
                    <div className="max-w-md w-ful p-8">
                        <div className="bg-white border-2 border-red-200 rounded-lg p-8 text-center">
                            <AlertTriangle className="w-16 h-16 text-red-600 mx-auto mb-4" />
                            <h2 className="text-2xl font-semibold text-gray-900 mb-2">
                                An unexpected error occurred.
                            </h2>
                            <p className="text-gray-700 mb-6">
                                No medical inference was made.
                            </p>
                            <button
                                onClick={() => window.location.href = '/'}
                                className="px-6 py-3 bg-medical-blue text-white rounded-lg hover:bg-blue-700 transition-colors"
                            >
                                Return to Home
                            </button>
                        </div>
                    </div>
                </div>
            );
        }

        return this.props.children;
    }
}

export default MedicalErrorBoundary;
