import { createContext, useContext, useState, type ReactNode } from 'react';
import type { Language } from '../types';

interface LangCtx {
  language: Language;
  setLanguage: (l: Language) => void;
}

const LanguageContext = createContext<LangCtx>({ language: 'en', setLanguage: () => {} });

export function LanguageProvider({ children }: { children: ReactNode }) {
  const [language, setLang] = useState<Language>(() => {
    const stored = localStorage.getItem('avalon-lang');
    if (stored === 'en' || stored === 'hi' || stored === 'mr') return stored;
    return 'en';
  });

  const setLanguage = (l: Language) => {
    setLang(l);
    localStorage.setItem('avalon-lang', l);
  };

  return (
    <LanguageContext.Provider value={{ language, setLanguage }}>
      {children}
    </LanguageContext.Provider>
  );
}

export const useLanguage = () => useContext(LanguageContext);
