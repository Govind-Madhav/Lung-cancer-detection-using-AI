import { Link, useLocation } from 'react-router-dom';
import { Home, Activity, BarChart3, Scale } from 'lucide-react';

/**
 * Sidebar Navigation
 * 
 * Clean, functional navigation. No fancy effects.
 */

const Sidebar = () => {
    const location = useLocation();

    const navItems = [
        { path: '/', label: 'Home', icon: Home },
        { path: '/predict', label: 'Predict', icon: Activity },
        { path: '/metrics', label: 'Metrics', icon: BarChart3 },
        { path: '/ethics', label: 'Ethics & Limitations', icon: Scale },
    ];

    return (
        <aside className="w-64 bg-white border-r-2 border-gray-200 min-h-screen p-6">
            <div className="mb-8">
                <h1 className="text-xl font-bold text-gray-900">
                    Lung Cancer Detection
                </h1>
                <p className="text-xs text-gray-600 mt-1">AI-Assisted Analysis</p>
            </div>

            <nav className="space-y-2">
                {navItems.map((item) => {
                    const Icon = item.icon;
                    const isActive = location.pathname === item.path;

                    return (
                        <Link
                            key={item.path}
                            to={item.path}
                            className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${isActive
                                ? 'bg-blue-50 text-medical-blue font-semibold'
                                : 'text-gray-700 hover:bg-gray-50'
                                }`}
                        >
                            <Icon className="w-5 h-5" />
                            <span>{item.label}</span>
                        </Link>
                    );
                })}
            </nav>
        </aside>
    );
};

export default Sidebar;
