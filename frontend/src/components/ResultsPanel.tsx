import { motion } from 'framer-motion';
import type { TriageResult } from '../types';
import RiskCard from './RiskCard';
import ExplanationPanel from './ExplanationPanel';
import OutcomePanel from './OutcomePanel';
import ActionPanel from './ActionPanel';
import CaregiverAlert from './CaregiverAlert';
import TopDiseases from './TopDiseases';
import { useLanguage } from '../context/LanguageContext';
import { t } from '../i18n';
import { getTranslatedSymptomName } from '../services/symptomTranslations';

interface Props {
  result: TriageResult;
}

const container = {
  hidden: { opacity: 0 },
  show: {
    opacity: 1,
    transition: { staggerChildren: 0.12 },
  },
};

const item = {
  hidden: { opacity: 0, y: 24, scale: 0.97 },
  show: { opacity: 1, y: 0, scale: 1, transition: { duration: 0.5, ease: [0.25, 0.46, 0.45, 0.94] } },
};

export default function ResultsPanel({ result }: Props) {
  const { language } = useLanguage();
  const isNeglect = result.neglect_detected !== 'No' && result.neglect_detected !== 'नहीं' && result.neglect_detected !== 'नाही';
  const isSilent = result.silent_emergency_flag === 'High' || result.silent_emergency_flag === 'उच्च';
  const showCaregiver = result.caregiver_alert_suggestion !== 'No' && result.caregiver_alert_suggestion !== 'नहीं' && result.caregiver_alert_suggestion !== 'नाही';

  // NLP metadata
  const nlp = (result as unknown as Record<string, unknown>).nlp as { extracted_symptoms?: string[]; negated_symptoms?: string[]; symptom_count?: number } | undefined;

  return (
    <motion.div
      variants={container}
      initial="hidden"
      animate="show"
      className="space-y-6"
    >
      {/* Section header */}
      <motion.div variants={item} className="flex items-center gap-3">
        <span className="text-2xl">📊</span>
        <h3 className="font-display text-2xl font-bold tracking-tight">
          {t(language, 'results.title')}
        </h3>
      </motion.div>

      {/* NLP extraction summary */}
      {nlp && nlp.extracted_symptoms && nlp.extracted_symptoms.length > 0 && (
        <motion.div
          variants={item}
          className="card-3d overflow-hidden p-1"
        >
          <div className="rounded-[calc(1.5rem-4px)] bg-surface-900/40 p-5">
            <div className="mb-3 flex items-center gap-2">
              <span className="text-lg">🧠</span>
              <span className="text-sm font-semibold text-accent-glow">{t(language, 'form.aiDetected')}</span>
              <span className="rounded-full bg-accent-primary/20 px-2.5 py-0.5 text-xs font-bold text-accent-glow">
                {nlp.symptom_count}
              </span>
            </div>
            <div className="flex flex-wrap gap-2">
              {nlp.extracted_symptoms.map((s) => (
                <span key={s} className="inline-flex items-center gap-1.5 rounded-xl border border-accent-primary/20
                  bg-accent-primary/[0.06] px-3 py-1.5 text-xs font-medium text-accent-glow/90">
                  ✅ {getTranslatedSymptomName(s, language)}
                </span>
              ))}
            </div>
            {nlp.negated_symptoms && nlp.negated_symptoms.length > 0 && (
              <div className="mt-3 flex flex-wrap gap-2">
                {nlp.negated_symptoms.map((s) => (
                  <span key={s} className="inline-flex items-center gap-1.5 rounded-xl border border-surface-200/10
                    bg-surface-200/[0.04] px-3 py-1.5 text-xs font-medium text-surface-200/40 line-through">
                    ❌ {getTranslatedSymptomName(s, language)}
                  </span>
                ))}
              </div>
            )}
          </div>
        </motion.div>
      )}

      {/* Alerts */}
      {isNeglect && (
        <motion.div
          variants={item}
          className="flex items-start gap-3 rounded-2xl border border-risk-medium/20
            bg-risk-medium/[0.06] p-5"
          role="alert"
        >
          <span className="mt-0.5 text-xl">⚠️</span>
          <p className="text-sm font-medium text-risk-medium">{t(language, 'results.neglectWarning')}</p>
        </motion.div>
      )}

      {isSilent && (
        <motion.div
          variants={item}
          className="flex items-start gap-3 rounded-2xl border border-risk-high/20
            bg-risk-high/[0.06] p-5"
          role="alert"
        >
          <span className="mt-0.5 text-xl">🚨</span>
          <p className="text-sm font-medium text-risk-high">{t(language, 'results.silentEmergency')}</p>
        </motion.div>
      )}

      {/* Risk card + Top diseases */}
      <motion.div variants={item} className="grid gap-6 md:grid-cols-2">
        <RiskCard result={result} />
        <TopDiseases diseases={result.top_3_conditions} />
      </motion.div>

      {/* Explanation */}
      <motion.div variants={item}>
        <ExplanationPanel explanation={result.explanation} />
      </motion.div>

      {/* Outcome + Recommendations */}
      <motion.div variants={item} className="grid gap-6 md:grid-cols-2">
        <OutcomePanel outcome={result.what_if_ignored} />
        <ActionPanel actionText={result.recommended_action} />
      </motion.div>

      {/* Caregiver */}
      {showCaregiver && (
        <motion.div variants={item}>
          <CaregiverAlert reason={result.caregiver_reason} />
        </motion.div>
      )}

      {/* Disclaimer */}
      <motion.div
        variants={item}
        className="rounded-2xl border border-white/[0.04] bg-white/[0.02] px-5 py-4 text-center"
      >
        <p className="text-xs text-surface-200/40">
          ⚕️ {result.disclaimer}
        </p>
      </motion.div>
    </motion.div>
  );
}
