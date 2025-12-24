import { useState, useEffect } from 'react';

/**
 * Disclaimer Acceptance Hook
 * 
 * Manages disclaimer acceptance state using localStorage.
 * Required for medical AI ethics compliance.
 */

const DISCLAIMER_KEY = 'lung_cancer_detection_disclaimer_accepted';

export const useDisclaimer = () => {
    const [isAccepted, setIsAccepted] = useState<boolean>(false);
    const [isLoading, setIsLoading] = useState<boolean>(true);

    useEffect(() => {
        // Check localStorage on mount
        const accepted = localStorage.getItem(DISCLAIMER_KEY) === 'true';
        setIsAccepted(accepted);
        setIsLoading(false);
    }, []);

    const acceptDisclaimer = () => {
        localStorage.setItem(DISCLAIMER_KEY, 'true');
        setIsAccepted(true);
    };

    const resetDisclaimer = () => {
        localStorage.removeItem(DISCLAIMER_KEY);
        setIsAccepted(false);
    };

    return {
        isAccepted,
        isLoading,
        acceptDisclaimer,
        resetDisclaimer,
    };
};
