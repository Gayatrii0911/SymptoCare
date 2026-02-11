import { useState, useRef, useEffect } from 'react';
import { FiMic, FiMicOff } from 'react-icons/fi';
import { useLanguage } from '../context/LanguageContext';
import { t } from '../i18n';

// Web Speech API types (not all browsers ship declarations)
type SpeechRecognitionCompat = typeof window extends { SpeechRecognition: infer T } ? T : unknown;
interface IWindow extends Window {
  SpeechRecognition?: new () => SpeechRecognitionInstance;
  webkitSpeechRecognition?: new () => SpeechRecognitionInstance;
}

interface SpeechRecognitionInstance {
  lang: string;
  interimResults: boolean;
  continuous: boolean;
  onresult: ((e: { results: { [index: number]: { [index: number]: { transcript: string } } } }) => void) | null;
  onerror: (() => void) | null;
  onend: (() => void) | null;
  start(): void;
  stop(): void;
  abort(): void;
}

interface Props {
  onResult: (transcript: string) => void;
}

const LANG_MAP: Record<string, string> = {
  en: 'en-US',
  hi: 'hi-IN',
  mr: 'mr-IN',
};

export default function VoiceInput({ onResult }: Props) {
  const { language } = useLanguage();
  const [listening, setListening] = useState(false);
  const recognitionRef = useRef<SpeechRecognitionInstance | null>(null);

  const w = typeof window !== 'undefined' ? (window as unknown as IWindow) : null;
  const supported = !!(w && (w.SpeechRecognition || w.webkitSpeechRecognition));

  useEffect(() => {
    return () => {
      recognitionRef.current?.abort();
    };
  }, []);

  const toggle = () => {
    if (listening) {
      recognitionRef.current?.stop();
      setListening(false);
      return;
    }

    const w2 = window as unknown as IWindow;
    const Ctor = w2.SpeechRecognition || w2.webkitSpeechRecognition;
    if (!Ctor) return;
    const recognition = new Ctor();
    recognition.lang = LANG_MAP[language] || 'en-US';
    recognition.interimResults = false;
    recognition.continuous = false;

    recognition.onresult = (e) => {
      const transcript = e.results[0][0].transcript;
      onResult(transcript);
      setListening(false);
    };

    recognition.onerror = () => setListening(false);
    recognition.onend = () => setListening(false);

    recognitionRef.current = recognition;
    recognition.start();
    setListening(true);
  };

  if (!supported) return null;

  return (
    <button
      type="button"
      onClick={toggle}
      className={`rounded-lg p-2 transition-all duration-200 ${
        listening
          ? 'animate-pulse bg-risk-high/20 text-risk-high'
          : 'text-surface-200/50 hover:bg-surface-700/50 hover:text-surface-50'
      }`}
      aria-label={listening ? t(language, 'form.listening') : t(language, 'form.voiceInput')}
      title={listening ? t(language, 'form.listening') : t(language, 'form.voiceInput')}
    >
      {listening ? <FiMicOff className="h-4 w-4" /> : <FiMic className="h-4 w-4" />}
    </button>
  );
}
