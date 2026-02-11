import { useLanguage } from '../context/LanguageContext';
import { t } from '../i18n';

interface Props {
  outcome: { short_term: string; long_term: string };
}

export default function OutcomePanel({ outcome }: Props) {
  const { language } = useLanguage();

  return (
    <div className="card-3d overflow-hidden p-1">
      <div className="rounded-[calc(1.5rem-4px)] bg-surface-900/40 p-6">
        <div className="mb-5 flex items-center gap-2">
          <span className="text-lg">⏳</span>
          <h4 className="font-display text-lg font-bold">
            {t(language, 'results.outcomeAwareness')}
          </h4>
        </div>

        <div className="space-y-4">
          <div className="rounded-2xl border border-amber-400/15 bg-amber-400/[0.04] p-4
            transition-all duration-200 hover:-translate-y-0.5">
            <div className="mb-2 flex items-center gap-2">
              <span className="text-base">⏰</span>
              <span className="text-sm font-semibold">
                {t(language, 'results.shortTerm')}
              </span>
            </div>
            <p className="text-sm leading-relaxed text-surface-200/70">
              {outcome.short_term}
            </p>
          </div>

          <div className="rounded-2xl border border-red-400/15 bg-red-400/[0.04] p-4
            transition-all duration-200 hover:-translate-y-0.5">
            <div className="mb-2 flex items-center gap-2">
              <span className="text-base">📅</span>
              <span className="text-sm font-semibold">
                {t(language, 'results.longTerm')}
              </span>
            </div>
            <p className="text-sm leading-relaxed text-surface-200/70">
              {outcome.long_term}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
