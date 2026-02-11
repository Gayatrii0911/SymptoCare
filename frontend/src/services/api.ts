import axios from 'axios';
import type { TriageRequest, TriageResult, SymptomEntry } from '../types';

const API_BASE = '/api';

const api = axios.create({
  baseURL: API_BASE,
  headers: { 'Content-Type': 'application/json' },
  timeout: 30000,
});

export async function submitTriage(data: TriageRequest): Promise<TriageResult> {
  const res = await api.post<TriageResult>('/triage', data);
  return res.data;
}

export async function fetchSymptoms(): Promise<SymptomEntry[]> {
  const res = await api.get<{ symptoms: SymptomEntry[]; total: number }>('/symptoms');
  return res.data.symptoms;
}

export async function fetchDiseases(): Promise<
  Array<{ name: string; description: string }>
> {
  const res = await api.get('/diseases');
  return res.data.diseases;
}

export async function healthCheck(): Promise<boolean> {
  try {
    const res = await api.get('/');
    return res.data.status !== undefined;
  } catch {
    return false;
  }
}
