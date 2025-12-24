import Sidebar from './Sidebar';

interface AppLayoutProps {
    children: React.ReactNode;
}

/**
 * App Layout Component
 * 
 * Main layout wrapper with sidebar navigation.
 */

const AppLayout: React.FC<AppLayoutProps> = ({ children }) => {
    return (
        <div className="flex min-h-screen bg-medical-bg">
            <Sidebar />
            <main className="flex-1 p-8">
                <div className="max-w-7xl mx-auto">
                    {children}
                </div>
            </main>
        </div>
    );
};

export default AppLayout;
