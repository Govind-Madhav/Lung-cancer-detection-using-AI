import { BrowserRouter, Routes, Route } from 'react-router-dom';
import AppLayout from '@/components/layout/AppLayout';
import Home from '@/pages/Home';
import Predict from '@/pages/Predict';
import Result from '@/pages/Result';
import Metrics from '@/pages/Metrics';
import Ethics from '@/pages/Ethics';
import NotFound from '@/pages/NotFound';

/**
 * Router Configuration
 * 
 * All routes wrapped in AppLayout for consistent navigation.
 */

const Router = () => {
    return (
        <BrowserRouter>
            <AppLayout>
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/predict" element={<Predict />} />
                    <Route path="/result/:id" element={<Result />} />
                    <Route path="/metrics" element={<Metrics />} />
                    <Route path="/ethics" element={<Ethics />} />
                    <Route path="*" element={<NotFound />} />
                </Routes>
            </AppLayout>
        </BrowserRouter>
    );
};

export default Router;
