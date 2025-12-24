import type { ModelType } from '@/schemas/prediction';

interface ModelSelectorProps {
    selected: ModelType;
    onChange: (modelType: ModelType) => void;
}

/**
 * Model Selector Component
 * 
 * Radio button selection for CNN-RNN vs ViT models.
 * Makes multi-model system explicit - reinforces research depth.
 */

const ModelSelector: React.FC<ModelSelectorProps> = ({ selected, onChange }) => {
    const models = [
        {
            value: 'cnn_rnn' as ModelType,
            label: 'CNN-RNN',
            badge: 'Primary',
            description: 'Convolutional + Recurrent Neural Network with Grad-CAM explainability',
        },
        {
            value: 'vit' as ModelType,
            label: 'Vision Transformer (ViT)',
            badge: 'Research',
            description: 'Transformer-based architecture with attention map visualization',
        },
    ];

    return (
        <div className="space-y-4">
            <label className="block text-gray-900 font-semibold mb-3">
                Select Model Architecture
            </label>

            <div className="space-y-3">
                {models.map((model) => (
                    <label
                        key={model.value}
                        className={`block border-2 rounded-lg p-4 cursor-pointer transition-colors ${selected === model.value
                                ? 'border-medical-blue bg-blue-50'
                                : 'border-gray-200 hover:border-gray-300'
                            }`}
                    >
                        <div className="flex items-start gap-3">
                            <input
                                type="radio"
                                name="model"
                                value={model.value}
                                checked={selected === model.value}
                                onChange={() => onChange(model.value)}
                                className="mt-1 w-5 h-5 text-medical-blue focus:ring-medical-blue border-gray-300"
                            />
                            <div className="flex-1">
                                <div className="flex items-center gap-2 mb-1">
                                    <span className="font-semibold text-gray-900">{model.label}</span>
                                    <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${model.badge === 'Primary'
                                            ? 'bg-blue-100 text-blue-800'
                                            : 'bg-purple-100 text-purple-800'
                                        }`}>
                                        {model.badge}
                                    </span>
                                </div>
                                <p className="text-sm text-gray-600">{model.description}</p>
                            </div>
                        </div>
                    </label>
                ))}
            </div>
        </div>
    );
};

export default ModelSelector;
