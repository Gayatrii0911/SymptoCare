import { useLanguage } from '../context/LanguageContext';
import { t } from '../i18n';
import type { Explanation } from '../types';

interface Props {
  explanation: Explanation;
}

export default function ExplanationPanel({ explanation }: Props) {
  const { language } = useLanguage();

  const sections = [
    { key: 'whatWeNoticed', emoji: '👁️', accent: 'border-blue-400/20 bg-blue-400/[0.04]', text: explanation.what_we_noticed },
    { key: 'whyItMatters',  emoji: '⚠️', accent: 'border-amber-400/20 bg-amber-400/[0.04]', text: explanation.why_it_matters },
    { key: 'whatThisMeans', emoji: '💡', accent: 'border-emerald-400/20 bg-emerald-400/[0.04]', text: explanation.what_this_means },
  ];

  return (
    <div className="card-3d overflow-hidden p-1">
      <div className="rounded-[calc(1.5rem-4px)] bg-surface-900/40 p-6">
        <div className="mb-5 flex items-center gap-2">
          <span className="text-lg">🔍</span>
          <h4 className="font-display text-lg font-bold">
            {t(language, 'results.explanation')}
          </h4>
        </div>

        <div className="grid gap-4 sm:grid-cols-3">
          {sections.map(({ key, emoji, accent, text }) => (
            <div
              key={key}
              className={`rounded-2xl border p-4 transition-all duration-200 hover:-translate-y-0.5 ${accent}`}
            >
              <div className="mb-2.5 flex items-center gap-2">
                <span className="text-lg">{emoji}</span>
                <span className="text-sm font-semibold">
                  {t(language, `results.${key}`)}
                </span>
              </div>
              <p className="text-sm leading-relaxed text-surface-200/70">{text}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
