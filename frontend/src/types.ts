/* ── Triage API Types ── */

export interface UserProfile {
  age: number;
  gender: 'male' | 'female' | 'other';
}

export interface TriageRequest {
  symptoms: string;
  age: number;
  gender: string;
  language?: string;
}

export interface Explanation {
  what_we_noticed: string;
  why_it_matters: string;
  what_this_means: string;
}

export interface TriageResult {
  risk_level: string;
  confidence_band: string;
  explanation: Explanation;
  neglect_detected: string;
  neglect_reason: string;
  silent_emergency_flag: string;
  risk_pattern_explanation: string;
  what_if_ignored: {
    short_term: string;
    long_term: string;
  };
  recommended_action: string;
  predicted_condition: string;
  ml_confidence: number;
  top_3_conditions: Array<[string, number]>;
  caregiver_alert_suggestion: string;
  caregiver_reason: string;
  language: string;
  input_summary: {
    raw_symptoms: string;
    normalized_symptoms: string[];
    user_profile: UserProfile;
    input_language: string;
    input_method: string;
  };
  disclaimer: string;
}

export interface SymptomEntry {
  id: string;
  name: string;
}

export interface HistoryEntry {
  id: string;
  timestamp: string;
  symptoms: string;
  age: number;
  gender: string;
  result: TriageResult;
}

export type Language = 'en' | 'hi' | 'mr';
export type Theme = 'dark' | 'light';
