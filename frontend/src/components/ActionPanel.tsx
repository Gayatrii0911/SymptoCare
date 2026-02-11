import { useLanguage } from '../context/LanguageContext';
import { t } from '../i18n';

interface Props {
  actionText: string;
}

export default function ActionPanel({ actionText }: Props) {
  const { language } = useLanguage();

  const lines = actionText.split('\n').filter((l) => l.trim());

  return (
    <div className="card-3d overflow-hidden p-1">
      <div className="rounded-[calc(1.5rem-4px)] bg-surface-900/40 p-6">
        <div className="mb-5 flex items-center gap-2">
          <span className="text-lg">💊</span>
          <h4 className="font-display text-lg font-bold">
            {t(language, 'results.recommendations')}
          </h4>
        </div>

        <div className="space-y-2.5">
          {lines.map((line, i) => {
            const trimmed = line.trim();
            const isHeader = /^[^\w\s]/.test(trimmed) && trimmed.includes(':');
            const isBullet = trimmed.startsWith('•') || trimmed.startsWith('-');

            if (isHeader) {
              return (
                <div key={i} className="mt-3 flex items-center gap-2 border-t border-white/[0.04] pt-3 first:mt-0 first:border-0 first:pt-0">
                  <span className="text-sm">⚡</span>
                  <span className="text-sm font-bold">{trimmed}</span>
                </div>
              );
            }

            if (isBullet) {
              return (
                <div key={i} className="flex items-start gap-2.5 pl-2 text-sm text-surface-200/70">
                  <span className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center
                    rounded-full bg-accent-primary/10 text-xs text-accent-glow">✓</span>
                  <span>{trimmed.replace(/^[•\-]\s*/, '')}</span>
                </div>
              );
            }

            return (
              <p key={i} className="text-sm text-surface-200/70">
                {trimmed}
              </p>
            );
          })}
        </div>
      </div>
    </div>
  );
}
