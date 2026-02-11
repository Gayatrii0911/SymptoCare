import en from './en.json';
import hi from './hi.json';
import mr from './mr.json';
import type { Language } from '../types';

const translations: Record<Language, typeof en> = { en, hi, mr };

type NestedKeyOf<T> = T extends object
  ? { [K in keyof T]: K extends string ? (T[K] extends object ? `${K}.${NestedKeyOf<T[K]>}` : K) : never }[keyof T]
  : never;

export type TranslationKey = NestedKeyOf<typeof en>;

export function t(lang: Language, key: string): string {
  const parts = key.split('.');
  let val: unknown = translations[lang] ?? translations.en;
  for (const p of parts) {
    if (val && typeof val === 'object' && p in val) {
      val = (val as Record<string, unknown>)[p];
    } else {
      // fallback to English
      let fallback: unknown = translations.en;
      for (const fp of parts) {
        if (fallback && typeof fallback === 'object' && fp in fallback) {
          fallback = (fallback as Record<string, unknown>)[fp];
        } else {
          return key;
        }
      }
      return typeof fallback === 'string' ? fallback : key;
    }
  }
  return typeof val === 'string' ? val : key;
}

export const LANGUAGE_LABELS: Record<Language, string> = {
  en: 'English',
  hi: 'हिन्दी',
  mr: 'मराठी',
};
