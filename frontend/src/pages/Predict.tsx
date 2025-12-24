import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDisclaimer } from '@/hooks/useDisclaimer';
import { usePrediction } from '@/hooks/usePrediction';
import { validateExternalRef } from '@/utils/validation';
import DisclaimerModal from '@/components/modals/DisclaimerModal';
import ImageUpload from '@/components/prediction/ImageUpload';
import ModelSelector from '@/components/prediction/ModelSelector';
import Button from '@/components/common/Button';
import Alert from '@/components/common/Alert';
import type { ModelType } from '@/schemas/prediction';

/**
 * Predict Page - Input Control
 * 
 * Components:
 * - DisclaimerModal (forced on first visit)
 * - ImageUpload (CT scan)
 * - ModelSelector (CNN-RNN vs ViT)
 * 
 * Submit disabled until: file selected + disclaimer accepted
 */

const Predict = () => {
    const navigate = useNavigate();
    const { isAccepted, isLoading: disclaimerLoading, acceptDisclaimer } = useDisclaimer();
    const { predictAsync, isLoading: isPredicting, error } = usePrediction();

    const [externalRef, setExternalRef] = useState('');
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [modelType, setModelType] = useState<ModelType>('cnn_rnn');
    const [validationError, setValidationError] = useState<string | null>(null);

    const canSubmit = isAccepted && selectedFile && externalRef.trim().length > 0 && !isPredicting;

    const handleSubmit = async () => {
        if (!canSubmit) return;

        // Validate external_ref
        const validation = validateExternalRef(externalRef);
        if (!validation.valid) {
            setValidationError(validation.error || 'Invalid patient ID');
            return;
        }

        setValidationError(null);

        try {
            const result = await predictAsync({
                external_ref: externalRef,
                file: selectedFile!,
                model_type: modelType,
            });

            // Navigate to result page on success
            navigate(`/result/${result.id}`, { state: { prediction: result } });
        } catch (err) {
            console.error('Prediction error:', err);
            // Error is handled by usePrediction hook
        }
    };

    if (disclaimerLoading) {
        return (
            <div className="flex items-center justify-center py-20">
                <p className="text-gray-600">Loading...</p>
            </div>
        );
    }

    return (
        <div className="max-w-3xl mx-auto py-8">
            <DisclaimerModal
                isOpen={!isAccepted}
                onAccept={acceptDisclaimer}
            />

            <div className="mb-8">
                <h1 className="text-4xl font-bold text-gray-900 mb-3">
                    Prediction Analysis
                </h1>
                <p className="text-gray-600">
                    Upload a CT scan image and select a model architecture for analysis.
                </p>
            </div>

            <div className="bg-white border-2 border-gray-200 rounded-lg p-8 space-y-8">
                {/* Patient/External Reference ID */}
                <div>
                    <label htmlFor="external-ref" className="block text-gray-900 font-semibold mb-2">
                        Patient/Dataset ID
                    </label>
                    <input
                        id="external-ref"
                        type="text"
                        value={externalRef}
                        onChange={(e) => setExternalRef(e.target.value)}
                        placeholder="e.g., NLST_001234"
                        className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-medical-blue focus:outline-none"
                        disabled={isPredicting}
                    />
                    <p className="text-sm text-gray-500 mt-1">
                        Enter dataset ID or patient identifier (no PHI)
                    </p>
                </div>

                {/* Image Upload */}
                <ImageUpload
                    onFileSelect={setSelectedFile}
                    selectedFile={selectedFile}
                />

                {/* Model Selection */}
                <ModelSelector
                    selected={modelType}
                    onChange={setModelType}
                />

                {/* Errors */}
                {validationError && (
                    <Alert variant="error">{validationError}</Alert>
                )}

                {error && (
                    <Alert variant="error">
                        {error.message || 'Failed to create prediction. Please try again.'}
                    </Alert>
                )}

                {/* Submit Button */}
                <div className="pt-4">
                    <Button
                        variant="primary"
                        size="lg"
                        onClick={handleSubmit}
                        disabled={!canSubmit}
                        isLoading={isPredicting}
                        className="w-full"
                    >
                        {isPredicting ? 'Analyzing...' : 'Start Analysis'}
                    </Button>

                    {!isAccepted && (
                        <p className="text-sm text-amber-700 mt-2 text-center">
                            Please accept the disclaimer to continue
                        </p>
                    )}
                </div>
            </div>
        </div>
    );
};

export default Predict;
