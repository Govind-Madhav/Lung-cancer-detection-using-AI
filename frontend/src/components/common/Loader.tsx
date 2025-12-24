import { Loader2 } from 'lucide-react';

interface LoaderProps {
    message?: string;
}

/**
 * Loading Spinner Component
 * 
 * Simple, non-distracting loader for inference operations.
 */

const Loader: React.FC<LoaderProps> = ({ message = 'Processing...' }) => {
    return (
        <div className="flex flex-col items-center justify-center p-12">
            <Loader2 className="w-12 h-12 text-medical-blue animate-spin mb-4" />
            <p className="text-gray-600 text-lg">{message}</p>
        </div>
    );
};

export default Loader;
