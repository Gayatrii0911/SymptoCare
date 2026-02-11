import { useLanguage } from '../context/LanguageContext';
import { t } from '../i18n';

interface Props {
  diseases: Array<[string, number]>;
}

const MEDAL = ['🥇', '🥈', '🥉'];

export default function TopDiseases({ diseases }: Props) {
  const { language } = useLanguage();

  return (
    <div className="card-3d overflow-hidden p-1">
      <div className="rounded-[calc(1.5rem-4px)] bg-surface-900/40 p-6">
        <div className="mb-5 flex items-center gap-2">
          <span className="text-lg">🏆</span>
          <h4 className="font-display text-lg font-bold">
            {t(language, 'results.topDiseases')}
          </h4>
        </div>

        <div className="space-y-4">
          {diseases.map(([name, prob], i) => {
            const pct = prob * 100;
            return (
              <div key={name} className="rounded-xl border border-white/[0.04] bg-white/[0.02] p-3.5">
                <div className="mb-2 flex items-center justify-between">
                  <span className="flex items-center gap-2 text-sm font-semibold">
                    <span className="text-base">{MEDAL[i] ?? '🔹'}</span>
                    {name}
                  </span>
                  <span className="rounded-lg bg-accent-primary/10 px-2 py-0.5 font-mono text-xs font-bold text-accent-glow">
                    {pct.toFixed(1)}%
                  </span>
                </div>
                <div className="h-2 overflow-hidden rounded-full bg-surface-700/50 shadow-inner">
                  <div
                    className="h-full rounded-full bg-gradient-to-r from-accent-primary to-accent-secondary
                      transition-all duration-700 ease-out"
                    style={{ width: `${pct}%` }}
                  />
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
