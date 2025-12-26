import { Upload, X } from 'lucide-react';
import { useState, useRef } from 'react';
import { validateImageFile } from '@/utils/validation';
// import Button from '../common/Button';
import Alert from '../common/Alert';

interface ImageUploadProps {
    onFileSelect: (file: File) => void;
    selectedFile: File | null;
}

/**
 * Image Upload Component
 * 
 * Drag-and-drop or click to upload CT scan images.
 * Validates file type and size before accepting.
 */

const ImageUpload: React.FC<ImageUploadProps> = ({ onFileSelect, selectedFile }) => {
    const [dragActive, setDragActive] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const fileInputRef = useRef<HTMLInputElement>(null);

    const handleFile = (file: File) => {
        const validation = validateImageFile(file);
        if (!validation.valid) {
            setError(validation.error || 'Invalid file');
            return;
        }

        setError(null);
        onFileSelect(file);
    };

    const handleDrag = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === 'dragenter' || e.type === 'dragover') {
            setDragActive(true);
        } else if (e.type === 'dragleave') {
            setDragActive(false);
        }
    };

    const handleDrop = (e: React.DragEvent) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFile(e.dataTransfer.files[0]);
        }
    };

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        e.preventDefault();
        if (e.target.files && e.target.files[0]) {
            handleFile(e.target.files[0]);
        }
    };

    const handleClick = () => {
        fileInputRef.current?.click();
    };

    const handleRemove = () => {
        onFileSelect(null as any);
        setError(null);
        if (fileInputRef.current) {
            fileInputRef.current.value = '';
        }
    };

    return (
        <div className="space-y-4">
            {error && (
                <Alert variant="error">{error}</Alert>
            )}

            {!selectedFile ? (
                <div
                    className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-colors ${dragActive
                        ? 'border-medical-blue bg-blue-50'
                        : 'border-gray-300 hover:border-gray-400'
                        }`}
                    onDragEnter={handleDrag}
                    onDragLeave={handleDrag}
                    onDragOver={handleDrag}
                    onDrop={handleDrop}
                    onClick={handleClick}
                >
                    <Upload className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-700 font-semibold mb-2">
                        Upload CT Scan Image
                    </p>
                    <p className="text-gray-500 text-sm mb-4">
                        Drag and drop or click to select
                    </p>
                    <p className="text-xs text-gray-400">
                        Supported: JPEG, PNG, DICOM (max 50MB)
                    </p>
                    <input
                        ref={fileInputRef}
                        type="file"
                        className="hidden"
                        accept="image/jpeg,image/jpg,image/png,.dcm"
                        onChange={handleChange}
                    />
                </div>
            ) : (
                <div className="bg-green-50 border-2 border-green-200 rounded-lg p-6">
                    <div className="flex items-start justify-between">
                        <div className="flex-1">
                            <p className="font-semibold text-green-900 mb-1">
                                File Selected
                            </p>
                            <p className="text-green-800 text-sm">{selectedFile.name}</p>
                            <p className="text-green-700 text-xs mt-1">
                                {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                            </p>
                        </div>
                        <button
                            onClick={handleRemove}
                            className="text-green-600 hover:text-green-800 p-1"
                            aria-label="Remove file"
                        >
                            <X className="w-5 h-5" />
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
};

export default ImageUpload;
