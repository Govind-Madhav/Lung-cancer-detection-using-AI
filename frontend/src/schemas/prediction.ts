/**
 * TypeScript Schemas - Frontend Contracts
 * 
 * These interfaces match the backend medical-grade schema exactly.
 * Strict typing prevents medical data mishandling.
 */

export type PredictionStatus = 'SUCCESS' | 'INCONCLUSIVE' | 'MODEL_ERROR' | 'INPUT_INVALID';
export type BinaryResult = 'BENIGN' | 'MALIGNANT';
export type StageResult = 'LOW' | 'MEDIUM' | 'HIGH';
export type RiskLevel = 'LOW' | 'MEDIUM' | 'HIGH' | 'INCONCLUSIVE';
export type ModelType = 'cnn_rnn' | 'vit';
export type ArtifactType = 'gradcam' | 'attention';

export interface ExplainabilityArtifact {
    id: number;
    prediction_id: number;
    artifact_type: ArtifactType;
    artifact_ref: string;
    expires_at: string;
    created_at: string;
}

export interface PredictionResponse {
    id: number;
    patient_id: number;
    model_id: number;

    // Status
    prediction_status: PredictionStatus;

    // Binary classification
    binary_result: BinaryResult | null;
    binary_confidence: number | null;

    // Stage classification
    stage_result: StageResult | null;
    stage_confidence: number | null;

    // Derived risk
    risk_level: RiskLevel;

    // Performance
    inference_time_ms: number;

    // Metadata
    created_at: string;

    // Explainability
    explainability_artifacts: ExplainabilityArtifact[];
}

export interface PredictionRequest {
    external_ref: string;
    file: File;
    model_type: ModelType;
}

export interface MetricsData {
    precision: number;
    recall: number;
    f1_score: number;
    confusion_matrix: {
        true_positive: number;
        true_negative: number;
        false_positive: number;
        false_negative: number;
    };
}
