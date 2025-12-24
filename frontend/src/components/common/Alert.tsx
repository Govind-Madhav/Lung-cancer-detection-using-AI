import { AlertCircle, AlertTriangle, Info, CheckCircle2 } from 'lucide-react';
import { cn } from '@/lib/utils';

interface AlertProps {
    variant?: 'info' | 'warning' | 'error' | 'success' | 'neutral';
    title?: string;
    children: React.ReactNode;
    className?: string;
}

/**
 * Alert Component
 * 
 * Medical-appropriate alert styling.
 * No emotional colors - muted, accessible tones only.
 */

const Alert: React.FC<AlertProps> = ({
    variant = 'info',
    title,
    children,
    className
}) => {
    const variants = {
        info: {
            icon: Info,
            bg: 'bg-blue-50',
            border: 'border-blue-200',
            iconColor: 'text-blue-600',
            textColor: 'text-blue-900',
        },
        warning: {
            icon: AlertTriangle,
            bg: 'bg-amber-50',
            border: 'border-amber-200',
            iconColor: 'text-amber-600',
            textColor: 'text-amber-900',
        },
        error: {
            icon: AlertCircle,
            bg: 'bg-red-50',
            border: 'border-red-200',
            iconColor: 'text-red-600',
            textColor: 'text-red-900',
        },
        success: {
            icon: CheckCircle2,
            bg: 'bg-green-50',
            border: 'border-green-200',
            iconColor: 'text-green-600',
            textColor: 'text-green-900',
        },
        neutral: {
            icon: Info,
            bg: 'bg-gray-50',
            border: 'border-gray-200',
            iconColor: 'text-gray-600',
            textColor: 'text-gray-900',
        },
    };

    const config = variants[variant];
    const Icon = config.icon;

    return (
        <div className={cn(
            'rounded-lg border-2 p-4',
            config.bg,
            config.border,
            className
        )}>
            <div className="flex items-start gap-3">
                <Icon className={cn('w-5 h-5 flex-shrink-0 mt-0.5', config.iconColor)} />
                <div className="flex-1">
                    {title && (
                        <h4 className={cn('font-semibold mb-1', config.textColor)}>
                            {title}
                        </h4>
                    )}
                    <div className={cn('text-sm', config.textColor)}>
                        {children}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Alert;
