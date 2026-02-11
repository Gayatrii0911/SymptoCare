import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { useLanguage } from '../context/LanguageContext';
import { t } from '../i18n';
import type { TriageResult, HistoryEntry } from '../types';

interface Props {
  onClose: () => void;
  onSelect: (r: TriageResult) => void;
}

const RISK_EMOJI: Record<string, string> = {
  Low: '🟢',
  Medium: '🟡',
  High: '🔴',
};

function riskEmoji(riskLevel: string): string {
  if (['Low', 'कम'].includes(riskLevel)) return RISK_EMOJI.Low;
  if (['Medium', 'मध्यम'].includes(riskLevel)) return RISK_EMOJI.Medium;
  if (['High', 'उच्च'].includes(riskLevel)) return RISK_EMOJI.High;
  return '⚪';
}

export default function HistoryPanel({ onClose, onSelect }: Props) {
  const { language } = useLanguage();
  const [entries, setEntries] = useState<HistoryEntry[]>([]);

  useEffect(() => {
    const raw = localStorage.getItem('avalon-history');
    if (raw) {
      try {
        setEntries(JSON.parse(raw));
      } catch {
        setEntries([]);
      }
    }
  }, []);

  const clearAll = () => {
    localStorage.removeItem('avalon-history');
    setEntries([]);
  };

  const fmt = (iso: string) =>
    new Intl.DateTimeFormat(language === 'hi' ? 'hi-IN' : language === 'mr' ? 'mr-IN' : 'en-US', {
      dateStyle: 'medium',
      timeStyle: 'short',
    }).format(new Date(iso));

  return (
    <motion.div
      initial={{ opacity: 0, x: 300 }}
      animate={{ opacity: 1, x: 0 }}
      exit={{ opacity: 0, x: 300 }}
      transition={{ type: 'spring', damping: 25, stiffness: 200 }}
      className="fixed inset-y-0 right-0 z-50 w-full max-w-md border-l border-white/[0.06]
        bg-surface-950/95 backdrop-blur-2xl"
      role="dialog"
      aria-label={t(language, 'history.title')}
    >
      {/* Header */}
      <div className="flex items-center justify-between border-b border-white/[0.06] px-6 py-4">
        <div className="flex items-center gap-2.5">
          <span className="text-lg">📜</span>
          <h3 className="font-display text-lg font-bold">
            {t(language, 'history.title')}
          </h3>
        </div>
        <div className="flex items-center gap-2">
          {entries.length > 0 && (
            <button
              onClick={clearAll}
              className="flex items-center gap-1.5 rounded-xl border border-risk-high/20
                bg-risk-high/[0.06] px-3 py-1.5 text-xs font-medium text-risk-high
                transition-all hover:bg-risk-high/10"
              aria-label={t(language, 'history.clear')}
            >
              🗑️ {t(language, 'history.clear')}
            </button>
          )}
          <button
            onClick={onClose}
            className="flex h-9 w-9 items-center justify-center rounded-xl border border-white/[0.06]
              bg-white/[0.03] text-sm transition-all hover:bg-white/[0.08]"
            aria-label={t(language, 'history.close')}
          >
            ✕
          </button>
        </div>
      </div>

      {/* List */}
      <div className="h-[calc(100vh-65px)] overflow-y-auto p-4">
        {entries.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-20">
            <span className="mb-3 text-4xl">📋</span>
            <p className="text-sm text-surface-200/40">
              {t(language, 'history.empty')}
            </p>
          </div>
        ) : (
          <div className="space-y-2">
            {entries.map((entry) => (
              <button
                key={entry.id}
                onClick={() => onSelect(entry.result)}
                className="group flex w-full items-center gap-3 rounded-2xl border border-white/[0.04]
                  bg-white/[0.02] p-4 text-left transition-all duration-200
                  hover:-translate-y-0.5 hover:border-accent-primary/20 hover:bg-white/[0.04]
                  hover:shadow-lg hover:shadow-accent-primary/5"
              >
                <span className="text-lg">{riskEmoji(entry.result.risk_level)}</span>
                <div className="min-w-0 flex-1">
                  <p className="truncate text-sm font-semibold">
                    {entry.result.predicted_condition}
                  </p>
                  <p className="mt-0.5 truncate text-xs text-surface-200/40">
                    {entry.symptoms}
                  </p>
                  <p className="mt-1 text-xs text-surface-200/30">🕐 {fmt(entry.timestamp)}</p>
                </div>
                <span className="text-surface-200/20 transition-transform
                  group-hover:translate-x-0.5 group-hover:text-accent-glow">→</span>
              </button>
            ))}
          </div>
        )}
      </div>
    </motion.div>
  );
}
