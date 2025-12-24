import { Link } from 'react-router-dom';
import { ArrowRight, Info } from 'lucide-react';
import Button from '@/components/common/Button';

/**
 * Home Page - Trust Establishment
 * 
 * NO marketing language. NO promises.
 * Neutral, professional presentation.
 */

const Home = () => {
    return (
        <div className="max-w-4xl mx-auto py-12">
            {/* Hero Section */}
            <div className="text-center mb-16">
                <h1 className="text-5xl font-bold text-gray-900 mb-4">
                    AI-Assisted Lung Cancer Detection
                </h1>
                <p className="text-xl text-gray-600 mb-8">
                    Supporting early detection using deep learning (CNN-RNN, ViT)
                </p>

                <div className="flex items-center justify-center gap-4">
                    <Link to="/predict">
                        <Button variant="primary" size="lg">
                            Start Analysis
                            <ArrowRight className="ml-2 w-5 h-5" />
                        </Button>
                    </Link>
                    <Link to="/ethics">
                        <Button variant="outline" size="lg">
                            <Info className="mr-2 w-5 h-5" />
                            How It Works
                        </Button>
                    </Link>
                </div>
            </div>

            {/* Information Cards */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-12">
                <div className="bg-white border-2 border-gray-200 rounded-lg p-6">
                    <h3 className="font-semibold text-gray-900 mb-2">
                        Model Architectures
                    </h3>
                    <p className="text-gray-600 text-sm">
                        Choose between CNN-RNN with Grad-CAM or Vision Transformer with attention visualization.
                    </p>
                </div>

                <div className="bg-white border-2 border-gray-200 rounded-lg p-6">
                    <h3 className="font-semibold text-gray-900 mb-2">
                        Explainable AI
                    </h3>
                    <p className="text-gray-600 text-sm">
                        Visualizations show which regions the model focused on during analysis.
                    </p>
                </div>

                <div className="bg-white border-2 border-gray-200 rounded-lg p-6">
                    <h3 className="font-semibold text-gray-900 mb-2">
                        Clinical Support Tool
                    </h3>
                    <p className="text-gray-600 text-sm">
                        Designed to assist healthcare professionals, not replace clinical judgment.
                    </p>
                </div>
            </div>

            {/* Disclaimer Notice */}
            <div className="mt-12 bg-amber-50 border-2 border-amber-200 rounded-lg p-6">
                <p className="text-amber-900 text-sm">
                    <strong>Important:</strong> This system provides AI-assisted analysis for research and clinical support purposes.
                    All results must be reviewed by qualified healthcare professionals. This is not a diagnostic tool.
                </p>
            </div>
        </div>
    );
};

export default Home;
