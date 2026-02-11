import { motion } from 'framer-motion';
import { useLanguage } from '../context/LanguageContext';
import { t } from '../i18n';

export default function HeroSection() {
  const { language } = useLanguage();

  return (
    <motion.div
      initial={{ opacity: 0, y: 30 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8, ease: [0.25, 0.46, 0.45, 0.94] }}
      className="relative text-center"
    >
      {/* Floating emojis decoration */}
      <div className="pointer-events-none absolute inset-0 -top-8">
        <span className="absolute left-[10%] top-4 animate-float text-3xl opacity-40">🩺</span>
        <span className="absolute right-[10%] top-0 animate-float-delayed text-2xl opacity-30">💊</span>
        <span className="absolute left-[25%] top-12 animate-bounce-soft text-2xl opacity-25">🧬</span>
        <span className="absolute right-[25%] top-8 animate-float text-2xl opacity-30">🫀</span>
      </div>

      {/* Badge */}
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.2, duration: 0.5 }}
      >
        <div className="badge-3d mb-8 border border-accent-primary/30 bg-accent-primary/10 text-accent-glow">
          <span className="animate-bounce-soft">⚡</span>
          {t(language, 'hero.badge')}
        </div>
      </motion.div>

      {/* Title */}
      <h2 className="font-display text-4xl font-extrabold leading-tight tracking-tight sm:text-5xl lg:text-6xl">
        <span className="inline-block">🏥</span>{' '}
        {t(language, 'hero.title')}
        <br />
        <span className="bg-gradient-to-r from-accent-primary via-accent-secondary to-purple-400
          bg-clip-text text-transparent animate-gradient bg-[length:200%_200%]">
          {t(language, 'hero.titleHighlight')}
        </span>
      </h2>

      {/* Description */}
      <p className="mx-auto mt-6 max-w-2xl text-lg leading-relaxed text-surface-200/60">
        {t(language, 'hero.description')}
      </p>

      {/* Decorative 3D divider */}
      <div className="mx-auto mt-12 flex items-center justify-center gap-4">
        <div className="h-px w-20 bg-gradient-to-r from-transparent to-accent-primary/30" />
        <span className="text-lg opacity-50">🔬</span>
        <div className="h-px w-20 bg-gradient-to-l from-transparent to-accent-primary/30" />
      </div>
    </motion.div>
  );
}
