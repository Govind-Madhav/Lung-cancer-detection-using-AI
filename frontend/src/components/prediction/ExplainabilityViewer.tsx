import { useState } from 'react';
import Alert from '../common/Alert';
import type { ExplainabilityArtifact } from '@/schemas/prediction';

interface ExplainabilityViewerProps {
    artifacts: ExplainabilityArtifact[];
    originalImage?: string;
    isError?: boolean;
}

/**
 * Explainability Viewer Component
 * 
 * Side-by-side CT scan and heatmap/attention map display.
 * Supports 3 states:
 * 
 * 1. Available: Show side-by-side images
 * 2. Not supported: Show neutral message
 * 3. Generation failed: Show warning but prediction is valid
 * 
 * IMAGE SAFETY:
 * - Right-click disabled (privacy signal)
 * - Caption: "Images shown are processed in-memory and not stored."
 */

const ExplainabilityViewer: React.FC<ExplainabilityViewerProps> = ({
    artifacts,
    originalImage,
    isError = false,
}) => {
    // STATE 3: Generation Failed
    if (isError) {
        return (
            <Alert variant="warning" title="Explainability Generation Error">
                Explainability generation encountered an error. The prediction result remains valid.
            </Alert>
        );
    }

    // STATE 2: Not Supported by Model
    if (!artifacts || artifacts.length === 0) {
        return (
            <Alert variant="neutral">
                Explainability visualization is not available for this model or prediction.
            </Alert>
        );
    }

    // STATE 1: Available
    const artifact = artifacts[0]; // Use first artifact

    return (
        <div className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Original CT Scan */}
                <div className="space-y-2">
                    <h4 className="font-semibold text-gray-900 text-lg">Original CT Scan</h4>
                    <div className="bg-gray-100 rounded-lg overflow-hidden border-2 border-gray-200">
                        {originalImage ? (
                            <img
                                src={originalImage}
                                alt="Original CT scan"
                                className="w-full h-auto"
                                onContextMenu={(e) => e.preventDefault()} // Disable right-click
                                draggable={false}
                            />
                        ) : (
                            <div className="aspect-square flex items-center justify-center text-gray-500">
                                CT Scan Not Available
                            </div>
                        )}
                    </div>
                </div>

                {/* AI Attention Map */}
                <div className="space-y-2">
                    <h4 className="font-semibold text-gray-900 text-lg">
                        AI Attention Map ({artifact.artifact_type === 'gradcam' ? 'Grad-CAM' : 'Attention'})
                    </h4>
                    <div className="bg-gray-100 rounded-lg overflow-hidden border-2 border-gray-200">
                        <img
                            src={artifact.artifact_ref}
                            alt={`${artifact.artifact_type} heatmap`}
                            className="w-full h-auto"
                            onContextMenu={(e) => e.preventDefault()} // Disable right-click
                            draggable={false}
                        />
                    </div>
                    <p className="text-sm text-gray-600 italic">
                        Highlighted areas indicate regions of interest identified by the model
                    </p>
                </div>
            </div>

            {/* Privacy Caption */}
            <p className="text-xs text-gray-500 text-center mt-4">
                Images shown are processed in-memory and not stored.
            </p>
        </div>
    );
};

export default ExplainabilityViewer;
