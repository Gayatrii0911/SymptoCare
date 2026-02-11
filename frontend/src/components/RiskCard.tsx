import { useLanguage } from '../context/LanguageContext';
import { t } from '../i18n';
import type { TriageResult } from '../types';

interface Props {
  result: TriageResult;
}

const RISK_CONFIG: Record<string, { emoji: string; border: string; bg: string; text: string; bar: string; glow: string }> = {
  Low: {
    emoji: '🟢',
    border: 'border-risk-low/30',
    bg: 'bg-risk-low/[0.08]',
    text: 'text-risk-low',
    bar: 'from-risk-low to-emerald-400',
    glow: 'shadow-[0_0_20px_rgba(52,211,153,0.15)]',
  },
  Medium: {
    emoji: '🟡',
    border: 'border-risk-medium/30',
    bg: 'bg-risk-medium/[0.08]',
    text: 'text-risk-medium',
    bar: 'from-risk-medium to-amber-400',
    glow: 'shadow-[0_0_20px_rgba(251,191,36,0.15)]',
  },
  High: {
    emoji: '🔴',
    border: 'border-risk-high/30',
    bg: 'bg-risk-high/[0.08]',
    text: 'text-risk-high',
    bar: 'from-risk-high to-rose-400',
    glow: 'shadow-[0_0_20px_rgba(248,113,113,0.15)]',
  },
};

function getRiskKey(riskLevel: string): string {
  if (['Low', 'कम'].includes(riskLevel)) return 'Low';
  if (['Medium', 'मध्यम'].includes(riskLevel)) return 'Medium';
  if (['High', 'उच्च'].includes(riskLevel)) return 'High';
  return 'Medium';
}

export default function RiskCard({ result }: Props) {
  const { language } = useLanguage();
  const riskKey = getRiskKey(result.risk_level);
  const cfg = RISK_CONFIG[riskKey] || RISK_CONFIG.Medium;
  const riskLabelKey = riskKey.toLowerCase() as 'low' | 'medium' | 'high';
  const confPct = result.ml_confidence * 100;

  return (
    <div className={`card-3d overflow-hidden p-1 ${cfg.glow}`}>
      <div className="rounded-[calc(1.5rem-4px)] bg-surface-900/40">
        {/* Risk level header */}
        <div className={`${cfg.bg} px-6 py-4 ${cfg.border} border-b`}>
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <span className="text-lg">🛡️</span>
              <span className="text-sm font-medium text-surface-200/70">
                {t(language, 'results.riskLevel')}
              </span>
            </div>
            <div className="flex items-center gap-2">
              <span className="text-xl">{cfg.emoji}</span>
              <span className={`font-display text-2xl font-bold ${cfg.text}`}>
                {t(language, `results.${riskLabelKey}`)}
              </span>
            </div>
          </div>
        </div>

        <div className="space-y-5 p-6">
          {/* Predicted disease */}
          <div>
            <p className="mb-1 flex items-center gap-1.5 text-xs font-medium uppercase tracking-widest text-surface-200/40">
              <span>🔬</span>
              {t(language, 'results.predictedCondition')}
            </p>
            <p className="font-display text-xl font-bold">{result.predicted_condition}</p>
          </div>

          {/* Confidence */}
          <div>
            <div className="mb-2 flex items-center justify-between">
              <div className="flex items-center gap-1.5">
                <span className="text-sm">📈</span>
                <span className="text-xs font-medium uppercase tracking-widest text-surface-200/40">
                  {t(language, 'results.confidence')}
                </span>
              </div>
              <span className={`font-mono text-sm font-semibold ${cfg.text}`}>
                {confPct.toFixed(1)}%
              </span>
            </div>
            <div className="h-2.5 overflow-hidden rounded-full bg-surface-700/50 shadow-inner">
              <div
                className={`h-full rounded-full bg-gradient-to-r ${cfg.bar}
                  transition-all duration-700 ease-out`}
                style={{ width: `${confPct}%` }}
              />
            </div>
            <p className="mt-1.5 text-right text-xs text-surface-200/30">
              {result.confidence_band}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
