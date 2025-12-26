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

const ModelSelector: React.FC<ModelSelectorProps> = () => {
    const models = [
        {
            value: 'cnn_rnn' as ModelType,
            label: 'Model V1 (Hybrid Architecture)',
            badge: 'Primary',
            description: 'Advanced hybrid architecture combining CNN and RNN for precise lung cancer detection.',
        },
    ];

    return (
        <div className="space-y-4">
            <label className="block text-gray-900 font-semibold mb-3">
                Model Architecture
            </label>

            <div className="space-y-3">
                {models.map((model) => (
                    <div
                        key={model.value}
                        className="block border-2 border-medical-blue bg-blue-50 rounded-lg p-4"
                    >
                        <div className="flex items-start gap-3">
                            <div className="mt-1 w-5 h-5 flex items-center justify-center rounded-full border-2 border-medical-blue">
                                <div className="w-2.5 h-2.5 rounded-full bg-medical-blue" />
                            </div>
                            <div className="flex-1">
                                <div className="flex items-center gap-2 mb-1">
                                    <span className="font-semibold text-gray-900">{model.label}</span>
                                    <span className="text-xs px-2 py-0.5 rounded-full font-medium bg-blue-100 text-blue-800">
                                        {model.badge}
                                    </span>
                                </div>
                                <p className="text-sm text-gray-600">{model.description}</p>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ModelSelector;
