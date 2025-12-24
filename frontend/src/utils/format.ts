/**
 * Formatting Utilities
 * 
 * Medical-appropriate formatting functions.
 */

/**
 * Format confidence as percentage with 1 decimal place
 * Example: 0.8765 → "87.7%"
 */
export const formatConfidence = (confidence: number | null): string => {
    if (confidence === null) return 'N/A';
    return `${(confidence * 100).toFixed(1)}%`;
};

/**
 * Format confidence with both decimal and percentage
 * Example: 0.8765 → "0.8765 (87.7%)"
 */
export const formatConfidenceFull = (confidence: number | null): string => {
    if (confidence === null) return 'N/A';
    return `${confidence.toFixed(4)} (${formatConfidence(confidence)})`;
};

/**
 * Format inference time
 * Example: 342 → "342ms"
 */
export const formatInferenceTime = (ms: number): string => {
    if (ms < 1000) return `${ms}ms`;
    return `${(ms / 1000).toFixed(2)}s`;
};

/**
 * Format date/time for display
 */
export const formatDateTime = (dateString: string): string => {
    const date = new Date(dateString);
    return date.toLocaleString();
};
