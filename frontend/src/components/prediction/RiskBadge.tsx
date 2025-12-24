import type { RiskLevel } from '@/schemas/prediction';
import { cn } from '@/lib/utils';

interface RiskBadgeProps {
    riskLevel: RiskLevel;
    className?: string;
}

/**
 * Risk Badge Component
 * 
 * Color-coded risk levels with accessible, muted tones.
 * NO GLASSMORPHISM - solid backgrounds only.
 * 
 * - LOW: Muted green
 * - MEDIUM: Muted amber
 * - HIGH: Muted red
 * - INCONCLUSIVE: Gray
 */

const RiskBadge: React.FC<RiskBadgeProps> = ({ riskLevel, className }) => {
    const configs = {
        LOW: {
            bg: 'bg-risk-low-bg',
            text: 'text-risk-low-text',
            border: 'border-risk-low-border',
            label: 'Low Risk',
        },
        MEDIUM: {
            bg: 'bg-risk-medium-bg',
            text: 'text-risk-medium-text',
            border: 'border-risk-medium-border',
            label: 'Medium Risk',
        },
        HIGH: {
            bg: 'bg-risk-high-bg',
            text: 'text-risk-high-text',
            border: 'border-risk-high-border',
            label: 'High Risk',
        },
        INCONCLUSIVE: {
            bg: 'bg-risk-inconclusive-bg',
            text: 'text-risk-inconclusive-text',
            border: 'border-risk-inconclusive-border',
            label: 'Inconclusive',
        },
    };

    const config = configs[riskLevel];

    return (
        <span
            className={cn(
                'inline-flex items-center px-4 py-2 rounded-lg border-2 font-semibold text-sm',
                config.bg,
                config.text,
                config.border,
                className
            )}
        >
            {config.label}
        </span>
    );
};

export default RiskBadge;
