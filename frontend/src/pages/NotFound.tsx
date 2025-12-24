import { Link } from 'react-router-dom';
import Button from '@/components/common/Button';

/**
 * 404 Not Found Page
 */

const NotFound = () => {
    return (
        <div className="flex items-center justify-center min-h-[60vh]">
            <div className="text-center">
                <h1 className="text-6xl font-bold text-gray-900 mb-4">404</h1>
                <p className="text-xl text-gray-600 mb-8">Page not found</p>
                <Link to="/">
                    <Button variant="primary">Return Home</Button>
                </Link>
            </div>
        </div>
    );
};

export default NotFound;
