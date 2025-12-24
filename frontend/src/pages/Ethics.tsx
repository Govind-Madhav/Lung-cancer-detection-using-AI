import Alert from '@/components/common/Alert';

/**
 * Ethics & Limitations Page - Professional Maturity
 * 
 * This page alone separates you from 90% of projects.
 * 
 * Includes:
 * - Dataset source (NLST)
 * - Bias limitations
 * - False positives / negatives
 * - Human-in-the-loop statement
 */

const Ethics = () => {
    return (
        <div className="max-w-4xl mx-auto py-8">
            <div className="mb-8">
                <h1 className="text-4xl font-bold text-gray-900 mb-3">
                    Ethics & Limitations
                </h1>
                <p className="text-gray-600">
                    Understanding the capabilities and constraints of this AI system.
                </p>
            </div>

            <div className="space-y-8">
                {/* Dataset Source */}
                <div className="bg-white border-2 border-gray-200 rounded-lg p-8">
                    <h2 className="text-2xl font-semibold text-gray-900 mb-4">
                        Dataset Source
                    </h2>
                    <p className="text-gray-700 leading-relaxed mb-4">
                        This model was trained on the <strong>National Lung Screening Trial (NLST)</strong> dataset,
                        a large-scale study conducted in the United States.
                    </p>
                    <div className="bg-blue-50 border-2 border-blue-200 rounded-lg p-4">
                        <p className="text-blue-900 text-sm">
                            <strong>Reference:</strong> National Lung Screening Trial Research Team. (2011).
                            Reduced lung-cancer mortality with low-dose computed tomographic screening.
                            New England Journal of Medicine.
                        </p>
                    </div>
                </div>

                {/* Known Biases */}
                <div className="bg-white border-2 border-gray-200 rounded-lg p-8">
                    <h2 className="text-2xl font-semibold text-gray-900 mb-4">
                        Known Biases & Limitations
                    </h2>
                    <div className="space-y-4">
                        <Alert variant="warning" title="Population Bias">
                            <ul className="list-disc list-inside space-y-2 text-sm">
                                <li>Predominantly Western population</li>
                                <li>Age range: 55-74 years</li>
                                <li>Smoking history required (current or former smokers)</li>
                                <li>May not generalize equally to all demographics</li>
                            </ul>
                        </Alert>

                        <Alert variant="warning" title="Technical Limitations">
                            <ul className="list-disc list-inside space-y-2 text-sm">
                                <li>Performance may vary with different CT scanner models</li>
                                <li>Image quality affects prediction reliability</li>
                                <li>Limited to specific lesion types present in training data</li>
                                <li>Cannot detect novel or rare cancer presentations</li>
                            </ul>
                        </Alert>
                    </div>
                </div>

                {/* False Positives / Negatives */}
                <div className="bg-white border-2 border-gray-200 rounded-lg p-8">
                    <h2 className="text-2xl font-semibold text-gray-900 mb-4">
                        False Positives & False Negatives
                    </h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div className="bg-red-50 border-2 border-red-200 rounded-lg p-6">
                            <h3 className="font-semibold text-red-900 mb-2">
                                False Positives
                            </h3>
                            <p className="text-red-800 text-sm mb-3">
                                The system may flag benign lesions as malignant, leading to unnecessary follow-up procedures.
                            </p>
                            <p className="text-red-900 font-semibold text-lg">
                                Rate: ~12-15% (estimated)
                            </p>
                        </div>

                        <div className="bg-amber-50 border-2 border-amber-200 rounded-lg p-6">
                            <h3 className="font-semibold text-amber-900 mb-2">
                                False Negatives
                            </h3>
                            <p className="text-amber-800 text-sm mb-3">
                                The system may miss actual malignancies, creating a false sense of security.
                            </p>
                            <p className="text-amber-900 font-semibold text-lg">
                                Rate: ~8-10% (estimated)
                            </p>
                        </div>
                    </div>
                    <p className="text-gray-600 text-sm mt-6">
                        <strong>Critical:</strong> These rates emphasize why human expert review is mandatory for all results.
                    </p>
                </div>

                {/* Human-in-the-Loop */}
                <div className="bg-medical-blue bg-opacity-5 border-2 border-blue-300 rounded-lg p-8">
                    <h2 className="text-2xl font-semibold text-blue-900 mb-4">
                        Human-in-the-Loop Required
                    </h2>
                    <div className="space-y-4 text-blue-900">
                        <p className="text-lg leading-relaxed">
                            This system is designed to <strong>ASSIST</strong> healthcare professionals, not replace them.
                        </p>
                        <ul className="list-disc list-inside space-y-2">
                            <li>All predictions must be reviewed by a qualified radiologist or physician</li>
                            <li>Clinical context and patient history must be considered</li>
                            <li>Follow standard medical protocols for diagnosis and treatment</li>
                            <li>This tool provides additional information, not final decisions</li>
                        </ul>
                        <div className="bg-white border-2 border-blue-300 rounded-lg p-4 mt-4">
                            <p className="font-semibold text-blue-900">
                                ⚠️ Medical Decision-Making
                            </p>
                            <p className="text-blue-800 text-sm mt-2">
                                No medical decisions should be made based solely on AI predictions.
                                This system is for research and clinical support purposes only.
                            </p>
                        </div>
                    </div>
                </div>

                {/* Ethical Considerations */}
                <div className="bg-white border-2 border-gray-200 rounded-lg p-8">
                    <h2 className="text-2xl font-semibold text-gray-900 mb-4">
                        Ethical Considerations
                    </h2>
                    <div className="space-y-3 text-gray-700">
                        <p>
                            <strong>Privacy:</strong> No personal health information (PHI) is stored by this system.
                            All identifiers are anonymized dataset references.
                        </p>
                        <p>
                            <strong>Transparency:</strong> Explainability visualizations show model attention,
                            but should not be interpreted as definitive evidence of pathology.
                        </p>
                        <p>
                            <strong>Accountability:</strong> Clinical decisions remain the responsibility of
                            licensed healthcare professionals.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Ethics;
