import { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { FiSearch, FiX, FiChevronDown, FiChevronUp, FiSend } from 'react-icons/fi';
import { useLanguage } from '../context/LanguageContext';
import { t } from '../i18n';
import { submitTriage, fetchSymptoms } from '../services/api';
import { getTranslatedSymptomName } from '../services/symptomTranslations';
import VoiceInput from './VoiceInput';
import type { TriageResult, SymptomEntry, HistoryEntry } from '../types';

interface Props {
  onResult: (r: TriageResult) => void;
  isLoading: boolean;
  setIsLoading: (l: boolean) => void;
}

type InputMode = 'select' | 'describe';

const POPULAR_WITH_EMOJI: Array<{ id: string; emoji: string }> = [
  { id: 'headache', emoji: '🤕' },
  { id: 'high_fever', emoji: '🌡️' },
  { id: 'cough', emoji: '😷' },
  { id: 'fatigue', emoji: '😴' },
  { id: 'nausea', emoji: '🤢' },
  { id: 'chest_pain', emoji: '💔' },
  { id: 'back_pain', emoji: '🔙' },
  { id: 'breathlessness', emoji: '😤' },
  { id: 'dizziness', emoji: '😵' },
  { id: 'vomiting', emoji: '🤮' },
  { id: 'skin_rash', emoji: '🔴' },
  { id: 'joint_pain', emoji: '🦴' },
  { id: 'stomach_pain', emoji: '🤒' },
  { id: 'muscle_pain', emoji: '💪' },
  { id: 'diarrhoea', emoji: '😣' },
  { id: 'anxiety', emoji: '😰' },
  { id: 'sweating', emoji: '💦' },
  { id: 'itching', emoji: '🫳' },
];

// Emoji map for all_symptoms browsing
const SYMPTOM_EMOJI: Record<string, string> = {
  abdominal_pain: '🤰', abnormal_menstruation: '🩸', acidity: '🔥', anxiety: '😰',
  back_pain: '🔙', belly_pain: '🤰', blackheads: '⚫', bladder_discomfort: '🚽',
  blister: '💧', blood_in_sputum: '🩸', bloody_stool: '🩸', blurred_and_distorted_vision: '👓',
  breathlessness: '😤', brittle_nails: '💅', bruising: '🟣', burning_micturition: '🔥',
  chest_pain: '💔', chills: '🥶', cold_hands_and_feets: '🧊', coma: '😵',
  congestion: '🤧', constipation: '😣', continuous_sneezing: '🤧', cough: '😷',
  cramps: '⚡', dark_urine: '🟤', dehydration: '🏜️', depression: '😔',
  diarrhoea: '😣', dizziness: '😵', enlarged_thyroid: '🦋',
  excessive_hunger: '🍽️', fatigue: '😴', fast_heart_rate: '💓',
  headache: '🤕', high_fever: '🌡️', hip_joint_pain: '🦿',
  indigestion: '😖', irritability: '😤', itching: '🫳',
  joint_pain: '🦴', knee_pain: '🦵', lack_of_concentration: '🧠',
  lethargy: '😪', loss_of_appetite: '🍽️', loss_of_balance: '🏃', loss_of_smell: '👃',
  malaise: '🤒', mild_fever: '🤒', mood_swings: '🎭', movement_stiffness: '🦿',
  muscle_pain: '💪', muscle_weakness: '💪', muscle_wasting: '💪',
  nausea: '🤢', neck_pain: '🦒', nodal_skin_eruptions: '🔴',
  obesity: '⚖️', pain_behind_the_eyes: '👁️', palpitations: '💓',
  phlegm: '🫁', polyuria: '🚽', puffy_face_and_eyes: '🫧',
  restlessness: '😤', runny_nose: '🤧', skin_rash: '🔴', skin_peeling: '🧴',
  slurred_speech: '🗣️', shivering: '🥶', stomach_pain: '🤒', sweating: '💦',
  swelling_joints: '🫧', swollen_legs: '🦵',
  throat_irritation: '😷', ulcers_on_tongue: '👅',
  visual_disturbances: '👁️', vomiting: '🤮',
  watering_from_eyes: '😢', weakness_in_limbs: '💪',
  weight_gain: '⬆️', weight_loss: '⬇️',
  yellow_urine: '🟡', yellowing_of_eyes: '🟡', yellowish_skin: '🟡',
};

function getEmoji(id: string): string {
  return SYMPTOM_EMOJI[id] || '🩺';
}

export default function SymptomForm({ onResult, isLoading, setIsLoading }: Props) {
  const { language } = useLanguage();
  const [mode, setMode] = useState<InputMode>('select');
  const [describeText, setDescribeText] = useState('');
  const [selectedSymptoms, setSelectedSymptoms] = useState<string[]>([]);
  const [age, setAge] = useState('');
  const [gender, setGender] = useState('male');
  const [allSymptoms, setAllSymptoms] = useState<SymptomEntry[]>([]);
  const [showAll, setShowAll] = useState(false);
  const [filter, setFilter] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    fetchSymptoms().then(setAllSymptoms).catch(() => {});
  }, []);

  const allSymptomIds = allSymptoms.map((s) => s.id);

  const toggleSymptom = (s: string) => {
    setSelectedSymptoms((prev) =>
      prev.includes(s) ? prev.filter((x) => x !== s) : [...prev, s],
    );
  };

  const format = (s: string) => s.replace(/_/g, ' ');

  const handleVoiceResult = useCallback((transcript: string) => {
    if (mode === 'describe') {
      setDescribeText((prev) => (prev ? prev + '. ' + transcript : transcript));
    }
  }, [mode]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    let symptoms: string;
    if (mode === 'select') {
      symptoms = selectedSymptoms.length > 0
        ? selectedSymptoms.map(format).join(', ')
        : '';
    } else {
      symptoms = describeText.trim();
    }

    if (!symptoms) {
      setError(mode === 'select'
        ? '🔍 Please select at least one symptom.'
        : '✏️ Please describe how you feel.');
      return;
    }
    if (!age || isNaN(Number(age)) || Number(age) < 1 || Number(age) > 120) {
      setError('📅 Please enter a valid age (1-120).');
      return;
    }

    setIsLoading(true);
    try {
      const payload = mode === 'describe'
        ? { symptoms, age: Number(age), gender, language }
        : { symptoms, age: Number(age), gender, language };
      
      const result = await submitTriage(payload);
      onResult(result);

      // Save to history
      const entry: HistoryEntry = {
        id: crypto.randomUUID(),
        timestamp: new Date().toISOString(),
        symptoms,
        age: Number(age),
        gender,
        result,
      };
      const history: HistoryEntry[] = JSON.parse(
        localStorage.getItem('avalon-history') || '[]',
      );
      history.unshift(entry);
      localStorage.setItem('avalon-history', JSON.stringify(history.slice(0, 50)));
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Request failed';
      setError('❌ ' + msg);
    } finally {
      setIsLoading(false);
    }
  };

  const clearAll = () => {
    setDescribeText('');
    setSelectedSymptoms([]);
    setAge('');
    setGender('male');
    setError('');
  };

  const filteredAll = showAll
    ? allSymptomIds.filter((s) => s.toLowerCase().includes(filter.toLowerCase()))
    : [];

  return (
    <motion.form
      onSubmit={handleSubmit}
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6, delay: 0.2, ease: [0.25, 0.46, 0.45, 0.94] }}
      className="card-3d p-1"
    >
      {/* Inner content with padding */}
      <div className="rounded-[calc(1.5rem-4px)] bg-surface-900/40 p-6 sm:p-8">

        {/* Title */}
        <div className="mb-6 flex items-center gap-3">
          <span className="text-2xl">🩺</span>
          <h3 className="font-display text-xl font-bold tracking-tight">
            {t(language, 'form.title')}
          </h3>
        </div>

        {/* ── Mode Switcher (3D tabs) ── */}
        <div className="mb-6 flex items-center gap-1 rounded-2xl border border-white/[0.06] bg-white/[0.03] p-1">
          <button
            type="button"
            onClick={() => setMode('select')}
            className={`flex flex-1 items-center justify-center gap-2 rounded-xl px-4 py-3 text-sm font-semibold transition-all duration-300 ${
              mode === 'select'
                ? 'bg-gradient-to-b from-accent-primary/30 to-accent-primary/10 text-accent-glow shadow-lg shadow-accent-primary/10'
                : 'text-surface-200/50 hover:text-surface-200/80 hover:bg-white/[0.04]'
            }`}
          >
            <span className="text-lg">🎯</span>
            {t(language, 'form.selectMode')}
          </button>
          <button
            type="button"
            onClick={() => setMode('describe')}
            className={`flex flex-1 items-center justify-center gap-2 rounded-xl px-4 py-3 text-sm font-semibold transition-all duration-300 ${
              mode === 'describe'
                ? 'bg-gradient-to-b from-accent-primary/30 to-accent-primary/10 text-accent-glow shadow-lg shadow-accent-primary/10'
                : 'text-surface-200/50 hover:text-surface-200/80 hover:bg-white/[0.04]'
            }`}
          >
            <span className="text-lg">💬</span>
            {t(language, 'form.describeMode')}
          </button>
        </div>

        {/* ══════════════════════════════════════════════ */}
        {/* ── MODE: SELECT (chip-based) ── */}
        {/* ══════════════════════════════════════════════ */}
        <AnimatePresence mode="wait">
          {mode === 'select' && (
            <motion.div
              key="select-mode"
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -12 }}
              transition={{ duration: 0.25 }}
            >
              {/* Selected chips */}
              {selectedSymptoms.length > 0 && (
                <div className="mb-5">
                  <div className="mb-2 flex items-center gap-2 text-xs font-semibold uppercase tracking-widest text-accent-glow/60">
                    <span>✅</span> {t(language, 'form.selected')} ({selectedSymptoms.length})
                  </div>
                  <div className="flex flex-wrap gap-2" role="list" aria-label="Selected symptoms">
                    {selectedSymptoms.map((s) => (
                      <motion.button
                        key={s}
                        type="button"
                        layout
                        initial={{ opacity: 0, scale: 0.8 }}
                        animate={{ opacity: 1, scale: 1 }}
                        exit={{ opacity: 0, scale: 0.8 }}
                        onClick={() => toggleSymptom(s)}
                        className="chip chip-active"
                        role="listitem"
                      >
                        <span>{getEmoji(s)}</span>
                        {getTranslatedSymptomName(s, language)}
                        <FiX className="h-3.5 w-3.5 opacity-60" />
                      </motion.button>
                    ))}
                  </div>
                </div>
              )}

              {/* Popular symptoms grid */}
              <div className="mb-5">
                <div className="mb-3 flex items-center gap-2 text-xs font-semibold uppercase tracking-widest text-surface-200/40">
                  <span>🔥</span> {t(language, 'form.popularSymptoms')}
                </div>
                <div className="grid grid-cols-2 gap-2 sm:grid-cols-3 lg:grid-cols-4">
                  {POPULAR_WITH_EMOJI.map(({ id, emoji }) => (
                    <button
                      key={id}
                      type="button"
                      onClick={() => toggleSymptom(id)}
                      className={`chip justify-start ${selectedSymptoms.includes(id) ? 'chip-active' : ''}`}
                    >
                      <span className="text-base">{emoji}</span>
                      <span className="truncate">{getTranslatedSymptomName(id, language)}</span>
                    </button>
                  ))}
                </div>
              </div>

              {/* Browse all toggle */}
              <button
                type="button"
                onClick={() => setShowAll(!showAll)}
                className="mb-4 flex items-center gap-2 text-sm font-semibold text-accent-glow/80 transition-colors
                  hover:text-accent-glow"
              >
                <span>📋</span>
                {t(language, 'form.allSymptoms')} ({allSymptomIds.length})
                {showAll ? <FiChevronUp className="h-4 w-4" /> : <FiChevronDown className="h-4 w-4" />}
              </button>

              <AnimatePresence>
                {showAll && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    transition={{ duration: 0.3 }}
                    className="mb-6 overflow-hidden"
                  >
                    {/* Search filter */}
                    <div className="relative mb-3">
                      <FiSearch className="absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-surface-200/30" />
                      <input
                        type="text"
                        value={filter}
                        onChange={(e) => setFilter(e.target.value)}
                        placeholder={`🔍 ${t(language, 'form.filterPlaceholder')}`}
                        className="input-3d pl-11 py-3 text-sm"
                      />
                    </div>
                    <div className="max-h-64 overflow-y-auto rounded-2xl border border-white/[0.06] bg-white/[0.02] p-3">
                      <div className="grid grid-cols-2 gap-1.5 sm:grid-cols-3">
                        {filteredAll.map((s) => (
                          <button
                            key={s}
                            type="button"
                            onClick={() => toggleSymptom(s)}
                            className={`chip justify-start text-xs ${selectedSymptoms.includes(s) ? 'chip-active' : ''}`}
                          >
                            <span>{getEmoji(s)}</span>
                            <span className="truncate">{getTranslatedSymptomName(s, language)}</span>
                          </button>
                        ))}
                        {filteredAll.length === 0 && (
                          <p className="col-span-full py-6 text-center text-sm text-surface-200/30">
                            😕 {t(language, 'form.noMatch')} "{filter}"
                          </p>
                        )}
                      </div>
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.div>
          )}

          {/* ══════════════════════════════════════════════ */}
          {/* ── MODE: DESCRIBE (free text NLP) ── */}
          {/* ══════════════════════════════════════════════ */}
          {mode === 'describe' && (
            <motion.div
              key="describe-mode"
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -12 }}
              transition={{ duration: 0.25 }}
            >
              {/* NLP info badge */}
              <div className="mb-4 flex items-center gap-2 rounded-xl border border-accent-primary/20
                bg-accent-primary/[0.05] px-4 py-2.5 text-xs text-accent-glow/80">
                <span className="text-base">🧠</span>
                <span>{t(language, 'form.nlpInfo')}</span>
              </div>

              {/* Text area with voice input */}
              <div className="relative mb-4">
                <textarea
                  value={describeText}
                  onChange={(e) => setDescribeText(e.target.value)}
                  placeholder="💭 Tell us how you feel… e.g. &quot;I have a terrible headache, feeling dizzy, and I've been throwing up since morning&quot;"
                  rows={4}
                  className="input-3d resize-none pr-14 text-base leading-relaxed"
                  autoComplete="off"
                />
                <div className="absolute right-3 top-3 flex flex-col gap-1">
                  <VoiceInput onResult={handleVoiceResult} />
                  {describeText && (
                    <button
                      type="button"
                      onClick={() => setDescribeText('')}
                      className="rounded-lg p-2 text-surface-200/40 transition-colors hover:bg-white/[0.06]
                        hover:text-surface-50"
                      aria-label="Clear"
                    >
                      <FiX className="h-4 w-4" />
                    </button>
                  )}
                </div>
              </div>

              {/* Example phrases */}
              <div className="mb-4">
                <p className="mb-2 flex items-center gap-2 text-xs font-semibold uppercase tracking-widest text-surface-200/30">
                  <span>💡</span> {t(language, 'form.tryExamples')}
                </p>
                <div className="flex flex-wrap gap-2">
                  {[
                    { text: "I feel dizzy and nauseous", emoji: "😵" },
                    { text: "chest pain and can't breathe", emoji: "💔" },
                    { text: "high fever with body ache", emoji: "🌡️" },
                    { text: "mujhe bahut tez bukhar hai", emoji: "🇮🇳" },
                  ].map(({ text, emoji }) => (
                    <button
                      key={text}
                      type="button"
                      onClick={() => setDescribeText(text)}
                      className="chip text-xs"
                    >
                      <span>{emoji}</span>
                      {text}
                    </button>
                  ))}
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        {/* ── Age + Gender row ── */}
        <div className="mb-6 grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div>
            <label htmlFor="age" className="mb-2 flex items-center gap-2 text-sm font-semibold text-surface-200/60">
              <span>📅</span> {t(language, 'form.age')}
            </label>
            <input
              id="age"
              type="number"
              min={1}
              max={120}
              value={age}
              onChange={(e) => setAge(e.target.value)}
              placeholder={t(language, 'form.agePlaceholder')}
              className="input-3d"
              required
            />
          </div>
          <div>
            <label htmlFor="gender" className="mb-2 flex items-center gap-2 text-sm font-semibold text-surface-200/60">
              <span>👤</span> {t(language, 'form.gender')}
            </label>
            <select
              id="gender"
              value={gender}
              onChange={(e) => setGender(e.target.value)}
              className="input-3d cursor-pointer"
            >
              <option value="male">👨 {t(language, 'form.genderOptions.male')}</option>
              <option value="female">👩 {t(language, 'form.genderOptions.female')}</option>
              <option value="other">🧑 {t(language, 'form.genderOptions.other')}</option>
            </select>
          </div>
        </div>

        {/* Error */}
        <AnimatePresence>
          {error && (
            <motion.div
              initial={{ opacity: 0, y: -8 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -8 }}
              className="mb-4 rounded-2xl border border-risk-high/20 bg-risk-high/[0.06] px-5 py-3.5
                text-sm text-risk-high"
              role="alert"
            >
              {error}
            </motion.div>
          )}
        </AnimatePresence>

        {/* Submit + Clear buttons */}
        <div className="flex items-center gap-3">
          <button
            type="submit"
            disabled={isLoading}
            className="btn-primary flex-1 text-base"
          >
            {isLoading ? (
              <>
                <span className="inline-block h-5 w-5 animate-spin rounded-full border-2 border-white/30
                  border-t-white" />
                <span>🔬 {t(language, 'form.analyzing')}</span>
              </>
            ) : (
              <>
                <FiSend className="h-4 w-4" />
                <span>🚀 {t(language, 'form.submit')}</span>
              </>
            )}
          </button>
          {(selectedSymptoms.length > 0 || describeText) && (
            <button
              type="button"
              onClick={clearAll}
              className="btn-ghost px-5 py-4"
              aria-label={t(language, 'form.clear')}
            >
              🗑️
            </button>
          )}
        </div>
      </div>
    </motion.form>
  );
}
