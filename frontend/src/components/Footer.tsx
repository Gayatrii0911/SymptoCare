import { useLanguage } from '../context/LanguageContext';
import { t } from '../i18n';

export default function Footer() {
  const { language } = useLanguage();

  return (
    <footer className="border-t border-white/[0.04] py-8">
      <div className="mx-auto max-w-6xl px-4 text-center sm:px-6 lg:px-8">
        <p className="text-sm leading-relaxed text-surface-200/50">
          ⚕️ {t(language, 'footer.disclaimer')}
        </p>
        <p className="mt-3 flex items-center justify-center gap-1.5 text-xs text-surface-200/30">
          <span>❤️</span>
          {t(language, 'footer.builtWith')}
        </p>
      </div>
    </footer>
  );
}
