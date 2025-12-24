import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import MedicalErrorBoundary from '@/components/common/MedicalErrorBoundary';

/**
 * Providers Component
 * 
 * Wraps app with:
 * 1. MedicalErrorBoundary (top-level error handling)
 * 2. QueryClientProvider (React Query for API calls)
 * 
 * MedicalErrorBoundary MUST be outermost to catch ALL errors.
 */

const queryClient = new QueryClient({
    defaultOptions: {
        queries: {
            retry: 1,
            refetchOnWindowFocus: false,
        },
    },
});

interface ProvidersProps {
    children: React.ReactNode;
}

const Providers: React.FC<ProvidersProps> = ({ children }) => {
    return (
        <MedicalErrorBoundary>
            <QueryClientProvider client={queryClient}>
                {children}
            </QueryClientProvider>
        </MedicalErrorBoundary>
    );
};

export default Providers;
