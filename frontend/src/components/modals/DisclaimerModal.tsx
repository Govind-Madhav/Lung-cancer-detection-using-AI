import { useState } from 'react';
import { X } from 'lucide-react';
import Button from '../common/Button';

interface DisclaimerModalProps {
    isOpen: boolean;
    onAccept: () => void;
}

/**
 * Disclaimer Modal Component
 * 
 * CRITICAL: This modal BLOCKS UI until accepted.
 * Required for medical AI ethics compliance.
 * 
 * - Cannot be dismissed without acceptance
 * - Acceptance stored in localStorage via useDisclaimer hook
 * - Shows on first visit only
 */

const DisclaimerModal: React.FC<DisclaimerModalProps> = ({ isOpen, onAccept }) => {
    const [hasRead, setHasRead] = useState(false);

    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
            <div className="bg-white rounded-lg shadow-2xl max-w-2xl w-full max-h-[90vh] overflow-y-auto">
                <div className="p-8">
                    <div className="flex items-center justify-between mb-6">
                        <h2 className="text-2xl font-bold text-gray-900">
                            Medical AI Disclaimer
                        </h2>
                        {/* Cannot close without accepting */}
                    </div>

                    <div className="space-y-4 text-gray-700 leading-relaxed">
                        <p className="font-semibold text-lg text-gray-900">
                            Important Information About This AI System
                        </p>

                        <div className="bg-amber-50 border-2 border-amber-200 rounded-lg p-4">
                            <p className="font-semibold text-amber-900 mb-2">
                                ⚠️ This is NOT a diagnostic tool
                            </p>
                            <p className="text-amber-900">
                                This system provides AI-assisted analysis to support healthcare professionals.
                                It does not replace clinical judgment or professional medical diagnosis.
                            </p>
                        </div>

                        <div className="space-y-3">
                            <h3 className="font-semibold text-gray-900">You acknowledge that:</h3>
                            <ul className="list-disc list-inside space-y-2 ml-4">
                                <li>All results must be reviewed by a qualified radiologist or physician</li>
                                <li>The system may produce false positives and false negatives</li>
                                <li>This tool is trained on specific datasets (NLST) and may not generalize to all populations</li>
                                <li>No medical decisions should be made based solely on AI predictions</li>
                                <li>Results are probabilistic and include uncertainty measurements</li>
                            </ul>
                        </div>

                        <div className="space-y-3">
                            <h3 className="font-semibold text-gray-900">Dataset Limitations:</h3>
                            <ul className="list-disc list-inside space-y-2 ml-4">
                                <li>Predominantly Western population (age 55-74 years)</li>
                                <li>Smoking history required for NLST dataset</li>
                                <li>May not perform equally across all demographics</li>
                            </ul>
                        </div>

                        <div className="bg-blue-50 border-2 border-blue-200 rounded-lg p-4">
                            <p className="font-semibold text-blue-900 mb-2">
                                Human-in-the-Loop Required
                            </p>
                            <p className="text-blue-900">
                                This system is designed to <strong>ASSIST</strong> clinicians, not replace them.
                                Expert review is mandatory for all results.
                            </p>
                        </div>

                        <div className="flex items-start gap-3 mt-6">
                            <input
                                type="checkbox"
                                id="disclaimer-read"
                                checked={hasRead}
                                onChange={(e) => setHasRead(e.target.checked)}
                                className="mt-1 w-5 h-5 text-medical-blue focus:ring-medical-blue border-gray-300 rounded"
                            />
                            <label htmlFor="disclaimer-read" className="text-gray-700 cursor-pointer">
                                I have read and understand these limitations. I acknowledge this system is for research
                                and assistance purposes only, and all results require professional medical review.
                            </label>
                        </div>
                    </div>

                    <div className="mt-8 flex justify-end">
                        <Button
                            variant="primary"
                            size="lg"
                            disabled={!hasRead}
                            onClick={onAccept}
                        >
                            Accept and Continue
                        </Button>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default DisclaimerModal;
