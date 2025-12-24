# Lung Cancer Detection Frontend

Medical-grade React + TypeScript frontend for AI-assisted lung cancer detection.

## Tech Stack

- **React 18** + **TypeScript**
- **Vite** (dev server & build)
- **Tailwind CSS** (styling)
- **React Router** (navigation)
- **React Query** (API state)
- **Recharts** (metrics visualization)
- **lucide-react** (icons)

## Medical UX Principles

### ✅ Implemented
- **Explicit Uncertainty**: INCONCLUSIVE is a valid, equal state
- **Deterministic Rendering**: Every prediction status maps to ONE UI state
- **No Glassmorphism**: Solid white cards on result pages
- **Accessibility**: WCAG AA contrast, muted colors
- **Privacy-Safe**: No PHI storage, images processed in-memory only

### ❌ Prohibited
- Dark mode default
- Glassmorphism on results
- Confidence meters / gamification
- Emojis or marketing language
- Absolute statements ("confirmed", "guaranteed")

## Project Structure

```
src/
├── app/                    # App bootstrap
│   ├── App.tsx            # Main app
│   ├── router.tsx         # Routes
│   └── providers.tsx      # MedicalErrorBoundary + React Query
├── pages/                 # Route-level pages
│   ├── Home.tsx          # Trust establishment
│   ├── Predict.tsx       # Upload + model selection
│   ├── Result.tsx        # **CRITICAL** - Deterministic UI matrix
│   ├── Metrics.tsx       # Performance metrics
│   ├── Ethics.tsx        # Limitations & bias
│   └── NotFound.tsx      # 404
├── components/
│   ├── common/           # Reusable UI
│   │   ├── MedicalErrorBoundary.tsx
│   │   ├── ErrorState.tsx        # INCONCLUSIVE/MODEL_ERROR/INPUT_INVALID
│   │   ├── Loader.tsx
│   │   ├── Alert.tsx
│   │   └── Button.tsx
│   ├── prediction/       # Prediction-specific
│   │   ├── ResultCard.tsx        # NO glassmorphism, confidence rules
│   │   ├── RiskBadge.tsx         # Muted colors
│   │   ├── ExplainabilityViewer.tsx  # 3 states
│   │   ├── ImageUpload.tsx
│   │   └── ModelSelector.tsx
│   ├── layout/           # Layout components
│   │   ├── AppLayout.tsx
│   │   └── Sidebar.tsx
│   └── modals/
│       └── DisclaimerModal.tsx   # Blocks UI
├── services/             # API layer
│   ├── apiClient.ts
│   ├── predictionService.ts
│   └── metricsService.ts
├── hooks/                # Custom hooks
│   ├── usePrediction.ts
│   └── useDisclaimer.ts
├── schemas/              # TypeScript contracts
│   └── prediction.ts
├── utils/
│   ├── format.ts         # Formatting utilities
│   └── validation.ts     # Input validation
└── lib/
    └── utils.ts          # Helper functions
```

## Development

### Install Dependencies
```bash
npm install
```

### Run Dev Server
```bash
npm run dev
```

Frontend runs on `http://localhost:3000`
Backend API proxied from `http://localhost:8000`

### Build for Production
```bash
npm run build
```

## Critical Implementation Details

### Result Page UI Matrix

```typescript
SUCCESS       → Full result + confidence + explainability
INCONCLUSIVE  → NO risk badge, NO confidence, locked wording
MODEL_ERROR   → ErrorState with retry guidance
INPUT_INVALID → Validation error, no inference shown
```

### Confidence Display Rule

**Confidence shown ONLY when `prediction_status === 'SUCCESS'`**

```typescript
{predictionStatus === 'SUCCESS' && binaryConfidence && (
  <p>Confidence: {formatConfidenceFull(binaryConfidence)}</p>
)}
```

### INCONCLUSIVE Wording (Locked)

```
"The system was unable to generate a reliable prediction for this input. 
No diagnostic inference should be made from this result."
```

**DO NOT IMPROVISE THIS TEXT.**

### Explainability States

1. **Available**: Side-by-side CT + heatmap
2. **Not Supported**: Neutral message
3. **Generation Failed**: Warning (prediction still valid)

### Image Safety

- Right-click disabled: `onContextMenu={(e) => e.preventDefault()}`
- Privacy caption: "Images shown are processed in-memory and not stored."

## API Contract

The frontend expects this exact response structure:

```typescript
interface PredictionResponse {
  id: number;
  prediction_status: 'SUCCESS' | 'INCONCLUSIVE' | 'MODEL_ERROR' | 'INPUT_INVALID';
  binary_result: 'BENIGN' | 'MALIGNANT' | null;
  binary_confidence: number | null;
  stage_result: 'LOW' | 'MEDIUM' | 'HIGH' | null;
  stage_confidence: number | null;
  risk_level: 'LOW' | 'MEDIUM' | 'HIGH' | 'INCONCLUSIVE';
  inference_time_ms: number;
  model_id: number;
  explainability_artifacts: ExplainabilityArtifact[];
}
```

## Ethics & Compliance

- **DisclaimerModal**: Blocks UI until accepted, stored in localStorage
- **Ethics Page**: Dataset bias, false positive/negative rates, human-in-loop
- **No PHI**: Uses `external_ref` only
- **Audit Trail**: All actions logged on backend

## Color Palette

```javascript
Medical Blue:    #1E40AF  // Primary
Background:      #F8FAFC
Card:            #FFFFFF  // NO glassmorphism

// Risk Levels (muted)
LOW:         bg: #F0FDF4, text: #166534, border: #BBF7D0
MEDIUM:      bg: #FFFBEB, text: #92400E, border: #FDE68A
HIGH:        bg: #FEF2F2, text: #991B1B, border: #FECACA
INCONCLUSIVE: bg: #F9FAFB, text: #374151, border: #E5E7EB
```

## Interview Talking Points

1. **Medical Safety**: Error boundary prevents partial results on crashes
2. **Deterministic UX**: Every backend state maps to exactly ONE UI state
3. **Explicit Uncertainty**: INCONCLUSIVE treated as equal to other states
4. **Privacy by Design**: No PHI, images in-memory only
5. **Professional Ethics**: Entire page dedicated to limitations and bias
6. **Accessibility**: WCAG AA contrast, no glassmorphism on decisions

---

**Built with medical-grade specifications for production deployment.**
