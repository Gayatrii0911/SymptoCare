import { useState } from 'react';
import { AnimatePresence } from 'framer-motion';
import Navbar from './components/Navbar';
import HeroSection from './components/HeroSection';
import SymptomForm from './components/SymptomForm';
import ResultsPanel from './components/ResultsPanel';
import HistoryPanel from './components/HistoryPanel';
import Footer from './components/Footer';
import type { TriageResult } from './types';

function App() {
  const [result, setResult] = useState<TriageResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [showHistory, setShowHistory] = useState(false);

  return (
    <div className="relative flex min-h-screen flex-col overflow-hidden">
      {/* Background mesh gradient */}
      <div className="pointer-events-none fixed inset-0 bg-mesh-dark opacity-60 dark:opacity-60" />
      <div className="pointer-events-none fixed inset-0">
        <div className="absolute -top-40 -right-40 h-96 w-96 rounded-full bg-accent-primary/[0.03] blur-3xl" />
        <div className="absolute top-1/3 -left-40 h-96 w-96 rounded-full bg-purple-500/[0.03] blur-3xl" />
        <div className="absolute bottom-0 right-1/4 h-96 w-96 rounded-full bg-cyan-500/[0.02] blur-3xl" />
      </div>

      <div className="relative z-10 flex min-h-screen flex-col">
        <Navbar onHistoryToggle={() => setShowHistory(!showHistory)} />

        <main className="mx-auto w-full max-w-6xl flex-1 px-4 py-8 sm:px-6 lg:px-8">
          <HeroSection />

          <section className="mt-14" aria-label="Symptom input">
            <SymptomForm
              onResult={setResult}
              isLoading={isLoading}
              setIsLoading={setIsLoading}
            />
          </section>

          <AnimatePresence mode="wait">
            {result && (
              <section className="mt-12" aria-label="Triage results" key="results">
                <ResultsPanel result={result} />
              </section>
            )}
          </AnimatePresence>

          <AnimatePresence>
            {showHistory && (
              <HistoryPanel
                key="history"
                onClose={() => setShowHistory(false)}
                onSelect={(r) => {
                  setResult(r);
                  setShowHistory(false);
                }}
              />
            )}
          </AnimatePresence>
        </main>

        <Footer />
      </div>
    </div>
  );
}

export default App;
