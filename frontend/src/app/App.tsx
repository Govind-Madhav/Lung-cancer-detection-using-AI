import Providers from './providers';
import Router from './router';

/**
 * Main App Component
 * 
 * Medical-Grade Frontend for Lung Cancer Detection
 * 
 * Architecture:
 * - MedicalErrorBoundary (fallback: no medical inference shown)
 * - React Query (API calls)
 * - React Router (navigation)
 * 
 * UX Principles:
 * - Explicit Uncertainty
 * - Deterministic Rendering
 * - No Glassmorphism on Results
 * - Accessibility > Aesthetics
 */

function App() {
    return (
        <Providers>
            <Router />
        </Providers>
    );
}

export default App;
