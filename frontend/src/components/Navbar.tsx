import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FiSun, FiMoon, FiClock, FiChevronDown } from 'react-icons/fi';
import { useTheme } from '../context/ThemeContext';
import { useLanguage } from '../context/LanguageContext';
import { t, LANGUAGE_LABELS } from '../i18n';
import type { Language } from '../types';

interface Props {
  onHistoryToggle: () => void;
}

export default function Navbar({ onHistoryToggle }: Props) {
  const { theme, toggle } = useTheme();
  const { language, setLanguage } = useLanguage();
  const [langOpen, setLangOpen] = useState(false);
  const langRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handler = (e: MouseEvent) => {
      if (langRef.current && !langRef.current.contains(e.target as Node)) {
        setLangOpen(false);
      }
    };
    document.addEventListener('mousedown', handler);
    return () => document.removeEventListener('mousedown', handler);
  }, []);

  return (
    <nav
      className="sticky top-0 z-50 border-b border-white/[0.06] bg-surface-950/70 backdrop-blur-2xl"
      role="navigation"
      aria-label="Main navigation"
    >
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Brand */}
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-gradient-to-br from-accent-primary to-accent-secondary shadow-lg shadow-accent-primary/20">
            <span className="text-xl">🏥</span>
          </div>
          <div>
            <h1 className="font-display text-lg font-bold leading-none tracking-tight">
              {t(language, 'nav.title')}
            </h1>
            <p className="text-xs text-surface-200/50">
              ✨ {t(language, 'nav.subtitle')}
            </p>
          </div>
        </div>

        {/* Right controls */}
        <div className="flex items-center gap-1.5">
          {/* Language selector */}
          <div className="relative" ref={langRef}>
            <button
              onClick={() => setLangOpen(!langOpen)}
              className="btn-ghost flex items-center gap-1.5 text-sm"
              aria-label={t(language, 'nav.language')}
              aria-expanded={langOpen}
            >
              <span>🌐</span>
              <span className="hidden sm:inline">{LANGUAGE_LABELS[language]}</span>
              <FiChevronDown
                className={`h-3 w-3 transition-transform duration-200 ${langOpen ? 'rotate-180' : ''}`}
              />
            </button>

            <AnimatePresence>
              {langOpen && (
                <motion.div
                  initial={{ opacity: 0, y: -8, scale: 0.95 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  exit={{ opacity: 0, y: -8, scale: 0.95 }}
                  transition={{ duration: 0.15 }}
                  className="absolute right-0 mt-2 w-40 overflow-hidden rounded-2xl border border-white/10
                    bg-surface-800/95 shadow-2xl backdrop-blur-xl"
                  role="listbox"
                >
                  {(Object.keys(LANGUAGE_LABELS) as Language[]).map((lang) => (
                    <button
                      key={lang}
                      onClick={() => { setLanguage(lang); setLangOpen(false); }}
                      className={`flex w-full items-center gap-2 px-4 py-3 text-sm transition-colors
                        hover:bg-accent-primary/10 ${
                          lang === language ? 'bg-accent-primary/15 text-accent-glow' : ''
                        }`}
                      role="option"
                      aria-selected={lang === language}
                    >
                      <span>{lang === 'en' ? '🇺🇸' : lang === 'hi' ? '🇮🇳' : '🇮🇳'}</span>
                      {LANGUAGE_LABELS[lang]}
                    </button>
                  ))}
                </motion.div>
              )}
            </AnimatePresence>
          </div>

          {/* Theme toggle
          <button
            onClick={toggle}
            className="btn-ghost p-2.5"
            aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
          >
            {theme === 'dark' ? <FiSun className="h-4 w-4" /> : <FiMoon className="h-4 w-4" />}
          </button> */}

          {/* History */}
          <button onClick={onHistoryToggle} className="btn-ghost gap-1.5 p-2.5" aria-label={t(language, 'nav.history')}>
            <FiClock className="h-4 w-4" />
          </button>
        </div>
      </div>
    </nav>
  );
}
