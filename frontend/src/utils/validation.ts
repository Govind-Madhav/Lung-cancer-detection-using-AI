/**
 * Validation Utilities
 * 
 * Input validation for medical data.
 */

const ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/jpg', 'image/png', 'image/dicom'];
const MAX_FILE_SIZE = 50 * 1024 * 1024; // 50MB

/**
 * Validate image file for CT scan upload
 */
export const validateImageFile = (file: File): { valid: boolean; error?: string } => {
    // Check file type
    if (!ALLOWED_IMAGE_TYPES.includes(file.type) && !file.name.endsWith('.dcm')) {
        return {
            valid: false,
            error: 'Invalid file type. Please upload a JPEG, PNG, or DICOM file.',
        };
    }

    // Check file size
    if (file.size > MAX_FILE_SIZE) {
        return {
            valid: false,
            error: `File size exceeds ${MAX_FILE_SIZE / 1024 / 1024}MB limit.`,
        };
    }

    return { valid: true };
};

/**
 * Validate external reference (patient ID)
 */
export const validateExternalRef = (ref: string): { valid: boolean; error?: string } => {
    if (!ref || ref.trim().length === 0) {
        return {
            valid: false,
            error: 'Patient ID is required.',
        };
    }

    if (ref.length > 64) {
        return {
            valid: false,
            error: 'Patient ID must be 64 characters or less.',
        };
    }

    return { valid: true };
};
