import { useLanguage } from '../context/LanguageContext';
import { t } from '../i18n';

interface Props {
  reason: string;
}

export default function CaregiverAlert({ reason }: Props) {
  const { language } = useLanguage();

  return (
    <div className="card-3d overflow-hidden border border-risk-high/20 p-1
      shadow-[0_0_24px_rgba(248,113,113,0.12)]">
      <div className="rounded-[calc(1.5rem-4px)] bg-risk-high/[0.04] p-6">
        <div className="flex items-start gap-4">
          <div className="flex h-12 w-12 shrink-0 items-center justify-center
            rounded-2xl bg-risk-high/10 text-2xl shadow-inner">
            🚑
          </div>
          <div>
            <h4 className="flex items-center gap-2 font-display text-lg font-bold text-risk-high">
              <span>👨‍⚕️</span>
              {t(language, 'results.caregiverAlert')}
            </h4>
            <p className="mt-2 text-sm leading-relaxed text-surface-200/70">{reason}</p>
          </div>
        </div>
      </div>
    </div>
  );
}
