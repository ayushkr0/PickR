"use client";

import { motion, useScroll, useTransform, AnimatePresence } from "motion/react";
import { useEffect, useRef, useState } from "react";
import ScrollReveal from "./ScrollReveal";
import { useTheme } from "@/lib/theme";
import DotGrid from "@/components/DotGrid";

const CATEGORIES = [
  {
    label: "Laptops",
    icon: (
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
        <rect x="2" y="3" width="20" height="14" rx="2" />
        <path d="M2 17h20" />
        <path d="M6 21h12" />
        <path d="M8 17v4" />
        <path d="M16 17v4" />
      </svg>
    ),
    query: "I'm looking for a laptop",
    desc: "Work, gaming, or creative projects",
  },
  {
    label: "Headphones",
    icon: (
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
        <path d="M3 18v-6a9 9 0 0 1 18 0v6" />
        <path d="M21 19a2 2 0 0 1-2 2h-1a2 2 0 0 1-2-2v-3a2 2 0 0 1 2-2h3zM3 19a2 2 0 0 0 2 2h1a2 2 0 0 0 2-2v-3a2 2 0 0 0-2-2H3z" />
      </svg>
    ),
    query: "I need headphones",
    desc: "Music, calls, or travel",
  },
  {
    label: "Cameras",
    icon: (
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
        <path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3z" />
        <circle cx="12" cy="13" r="3" />
      </svg>
    ),
    query: "I want a camera",
    desc: "Photography, video, or vlogging",
  },
];

const STEPS = [
  {
    num: "01",
    title: "Describe your needs",
    desc: "Tell us what you're looking for in plain language. No tech jargon required.",
  },
  {
    num: "02",
    title: "Smart follow-ups",
    desc: "Our AI asks targeted questions to understand your budget, use case, and preferences.",
  },
  {
    num: "03",
    title: "Curated results",
    desc: "Get personalized picks with honest pros, cons, and reasoning behind each recommendation.",
  },
];

interface Props {
  onStart: (query: string) => void;
}

// Logo — layered rounded shapes with checkmark (matches PickR brand icon)
function Logo({ size = 40, className = "" }: { size?: number; className?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 64 64" fill="none" className={className}>
      {/* Outer rounded square */}
      <rect width="64" height="64" rx="16" fill="var(--bg-elevated, #F0F1F5)" />
      {/* Cream/warm layer — top */}
      <rect x="4" y="4" width="56" height="32" rx="14" fill="#F2E6C9" />
      {/* Purple layer — middle */}
      <rect x="4" y="16" width="56" height="30" rx="14" fill="#9382F5" />
      {/* Dark pill — bottom with checkmark */}
      <rect x="4" y="30" width="56" height="30" rx="15" fill="#1A1D2E" />
      {/* White checkmark */}
      <path
        d="M22 46 L28 52 L42 38"
        stroke="white"
        strokeWidth="4.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}

export { Logo };

// Theme toggle button
function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();
  return (
    <motion.button
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5, delay: 0.1 }}
      onClick={toggleTheme}
      className="w-9 h-9 flex items-center justify-center rounded-full bg-nav-bg backdrop-blur-xl border border-border hover:border-border-dark transition-all cursor-pointer shadow-[var(--shadow-sm)]"
      aria-label={`Switch to ${theme === "light" ? "dark" : "light"} mode`}
    >
      <motion.div
        key={theme}
        initial={{ rotate: -30, scale: 0.5, opacity: 0 }}
        animate={{ rotate: 0, scale: 1, opacity: 1 }}
        transition={{ type: "spring", stiffness: 400, damping: 20 }}
      >
        {theme === "light" ? (
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-text-secondary">
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
          </svg>
        ) : (
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-amber">
            <circle cx="12" cy="12" r="5" />
            <line x1="12" y1="1" x2="12" y2="3" />
            <line x1="12" y1="21" x2="12" y2="23" />
            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
            <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
            <line x1="1" y1="12" x2="3" y2="12" />
            <line x1="21" y1="12" x2="23" y2="12" />
            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
            <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
          </svg>
        )}
      </motion.div>
    </motion.button>
  );
}

// Animated text — each word fades in from below with stagger
function AnimatedHeading({ text, className, delay = 0 }: { text: string; className?: string; delay?: number }) {
  const words = text.split(" ");
  return (
    <span className={className}>
      {words.map((word, i) => (
        <motion.span
          key={i}
          initial={{ opacity: 0, y: 30, filter: "blur(8px)" }}
          animate={{ opacity: 1, y: 0, filter: "blur(0px)" }}
          transition={{
            delay: delay + i * 0.08,
            duration: 0.6,
            ease: [0.22, 1, 0.36, 1],
          }}
          className="inline-block mr-[0.3em]"
        >
          {word}
        </motion.span>
      ))}
    </span>
  );
}

// Animated rotating words
const ROTATING_WORDS = ["laptop", "headphones", "camera", "product"];

function RotatingWord() {
  const [index, setIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setIndex((prev) => (prev + 1) % ROTATING_WORDS.length);
    }, 2500);
    return () => clearInterval(interval);
  }, []);

  return (
    <span className="inline-block relative overflow-hidden h-[1.3em] align-bottom" style={{ minWidth: "6.5em" }}>
      <AnimatePresence mode="wait">
        <motion.span
          key={ROTATING_WORDS[index]}
          initial={{ y: "110%" }}
          animate={{ y: "0%" }}
          exit={{ y: "-110%" }}
          transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
          className="block text-accent"
        >
          {ROTATING_WORDS[index]}
        </motion.span>
      </AnimatePresence>
    </span>
  );
}

export default function LandingPage({ onStart }: Props) {
  const heroRef = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: heroRef,
    offset: ["start start", "end start"],
  });

  const heroOpacity = useTransform(scrollYProgress, [0, 0.8], [1, 0]);
  const heroScale = useTransform(scrollYProgress, [0, 0.8], [1, 0.97]);
  const heroY = useTransform(scrollYProgress, [0, 0.8], [0, -50]);

  return (
    <div className="w-full h-full overflow-y-auto bg-bg-primary transition-colors duration-300">
      {/* ── Nav ── */}
      <nav className="fixed top-0 left-0 right-0 z-50 px-6 py-4">
        <div className="max-w-5xl mx-auto flex items-center justify-between">
          <motion.div
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
            className="flex items-center gap-2.5 bg-nav-bg backdrop-blur-xl border border-border rounded-full pl-2 pr-4 py-1.5 shadow-[var(--shadow-sm)]"
          >
            <Logo size={28} />
            <span className="text-sm font-semibold text-text-primary tracking-tight">PickR</span>
          </motion.div>
          <div className="flex items-center gap-2">
            <ThemeToggle />
            <motion.button
              initial={{ opacity: 0, x: 10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5 }}
              onClick={() => onStart("")}
              className="text-sm font-medium text-text-secondary hover:text-text-primary bg-nav-bg backdrop-blur-xl border border-border px-4 py-2 rounded-full transition-colors cursor-pointer shadow-[var(--shadow-sm)] hover:shadow-[var(--shadow-md)]"
            >
              Open Chat
            </motion.button>
          </div>
        </div>
      </nav>

      {/* ── Hero Section ── */}
      <div ref={heroRef} className="relative min-h-[100vh] flex items-center justify-center overflow-hidden">
        {/* Mesh gradient background */}
        <div className="mesh-gradient" />

        {/* Interactive dot grid */}
        <DotGrid />

        {/* Extra animated blobs for depth */}
        <div className="mesh-blob w-[400px] h-[400px] top-[10%] left-[15%]" style={{ background: "var(--mesh-1)" }} />
        <div className="mesh-blob w-[350px] h-[350px] top-[20%] right-[10%]" style={{ background: "var(--mesh-2)", animationDelay: "-5s" }} />
        <div className="mesh-blob w-[300px] h-[300px] bottom-[15%] left-[40%]" style={{ background: "var(--mesh-3)", animationDelay: "-10s" }} />

        <motion.div
          style={{ opacity: heroOpacity, scale: heroScale, y: heroY }}
          className="relative z-10 text-center px-6 max-w-3xl mx-auto"
        >
          {/* Badge */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.5, ease: [0.22, 1, 0.36, 1] }}
            className="mb-8 inline-flex items-center gap-2 bg-accent-light border border-accent/10 rounded-full px-4 py-1.5"
          >
            <div className="w-1.5 h-1.5 rounded-full bg-accent animate-pulse" />
            <span className="text-xs font-medium text-accent tracking-wide">AI-Powered Recommendations</span>
          </motion.div>

          {/* Animated heading with rotating word */}
          <h1 className="font-[var(--font-display)] text-5xl sm:text-6xl lg:text-7xl font-bold text-text-primary leading-[1.1] tracking-[-0.04em] mb-6">
            <AnimatedHeading text="Find the right" delay={0.2} />
            <br />
            <motion.span
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.6, duration: 0.5 }}
            >
              <RotatingWord />
            </motion.span>
          </h1>

          {/* Underline that draws in */}
          <motion.div
            initial={{ scaleX: 0 }}
            animate={{ scaleX: 1 }}
            transition={{ delay: 1.0, duration: 0.8, ease: [0.22, 1, 0.36, 1] }}
            className="h-[3px] w-24 mx-auto bg-gradient-to-r from-accent via-blue to-pink rounded-full origin-left mb-8"
          />

          <motion.p
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.1, duration: 0.6 }}
            className="text-text-secondary text-lg sm:text-xl max-w-lg mx-auto leading-relaxed mb-10"
          >
            Describe what you need. Our AI finds the best match — with honest trade-offs.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 1.3, duration: 0.5 }}
            className="flex flex-col sm:flex-row items-center justify-center gap-3"
          >
            <button
              onClick={() => {
                document.getElementById("categories")?.scrollIntoView({ behavior: "smooth" });
              }}
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 px-7 py-3.5 bg-accent text-white font-semibold rounded-xl hover:bg-accent-hover transition-all duration-200 shadow-[var(--shadow-glow)] hover:shadow-[0_6px_24px_rgba(108,92,231,0.2)] active:scale-[0.97] cursor-pointer text-sm"
            >
              Get Started
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M12 5v14M5 12l7 7 7-7" />
              </svg>
            </button>
            <button
              onClick={() => onStart("")}
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-7 py-3.5 bg-bg-elevated text-text-primary font-semibold rounded-xl border border-border hover:border-border-dark hover:shadow-[var(--shadow-md)] transition-all duration-200 active:scale-[0.97] cursor-pointer text-sm"
            >
              Just Ask
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M5 12h14M12 5l7 7-7 7" />
              </svg>
            </button>
          </motion.div>
        </motion.div>

        {/* Scroll indicator */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1.8 }}
          className="absolute bottom-8 left-1/2 -translate-x-1/2"
        >
          <motion.div
            animate={{ y: [0, 8, 0] }}
            transition={{ repeat: Infinity, duration: 2, ease: "easeInOut" }}
            className="w-5 h-8 rounded-full border-2 border-border-dark flex items-start justify-center p-1.5"
          >
            <motion.div className="w-1 h-1 rounded-full bg-text-muted" />
          </motion.div>
        </motion.div>
      </div>

      {/* ── How It Works ── */}
      <section className="py-28 sm:py-36 px-6 bg-bg-secondary transition-colors duration-300">
        <div className="max-w-4xl mx-auto">
          <ScrollReveal>
            <p className="text-accent font-medium text-xs tracking-[0.2em] uppercase mb-4 text-center">
              How It Works
            </p>
          </ScrollReveal>
          <ScrollReveal delay={0.1}>
            <h2 className="text-3xl sm:text-4xl lg:text-[44px] font-[var(--font-display)] font-bold text-text-primary text-center leading-[1.1] tracking-[-0.03em] mb-20">
              Three steps. Zero guesswork.
            </h2>
          </ScrollReveal>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
            {STEPS.map((step, i) => (
              <ScrollReveal key={step.num} delay={i * 0.12} direction="up" distance={30}>
                <div className="relative p-6 rounded-2xl bg-bg-elevated border border-border hover:shadow-[var(--shadow-md)] transition-all duration-300">
                  <span className="text-[11px] font-bold tracking-wider text-accent bg-accent-light w-8 h-8 rounded-lg flex items-center justify-center mb-4">
                    {step.num}
                  </span>
                  <h3 className="font-[var(--font-display)] text-base font-semibold text-text-primary mb-2 tracking-tight">
                    {step.title}
                  </h3>
                  <p className="text-text-muted text-sm leading-relaxed">
                    {step.desc}
                  </p>
                </div>
              </ScrollReveal>
            ))}
          </div>
        </div>
      </section>

      {/* ── Categories ── */}
      <section id="categories" className="py-28 sm:py-36 px-6 transition-colors duration-300">
        <div className="max-w-4xl mx-auto">
          <ScrollReveal>
            <p className="text-accent font-medium text-xs tracking-[0.2em] uppercase mb-4 text-center">
              Browse Categories
            </p>
          </ScrollReveal>
          <ScrollReveal delay={0.1}>
            <h2 className="text-3xl sm:text-4xl lg:text-[44px] font-[var(--font-display)] font-bold text-text-primary text-center leading-[1.1] tracking-[-0.03em] mb-6">
              What are you looking for?
            </h2>
          </ScrollReveal>
          <ScrollReveal delay={0.15}>
            <p className="text-text-muted text-center text-base mb-14 max-w-md mx-auto">
              Pick a category to get started, or type your own question.
            </p>
          </ScrollReveal>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            {CATEGORIES.map((cat, i) => (
              <ScrollReveal key={cat.label} delay={i * 0.1} distance={20} className="h-full">
                <button
                  onClick={() => onStart(cat.query)}
                  className="group w-full h-full flex flex-col items-center justify-center gap-4 p-8 rounded-2xl bg-bg-elevated border border-border hover:border-accent/25 hover:shadow-[var(--shadow-lg)] transition-all duration-300 cursor-pointer"
                >
                  <div className="w-14 h-14 rounded-xl bg-bg-secondary border border-border group-hover:border-accent/20 group-hover:bg-accent-light flex items-center justify-center text-text-muted group-hover:text-accent transition-all duration-300">
                    {cat.icon}
                  </div>
                  <div className="text-center">
                    <span className="font-[var(--font-display)] text-base font-semibold text-text-primary block mb-1 tracking-tight">
                      {cat.label}
                    </span>
                    <span className="text-sm text-text-muted">{cat.desc}</span>
                  </div>
                  <div className="flex items-center gap-1.5 text-xs font-medium text-accent opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                    Explore
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M5 12h14M12 5l7 7-7 7" />
                    </svg>
                  </div>
                </button>
              </ScrollReveal>
            ))}
          </div>
        </div>
      </section>

      {/* ── CTA ── */}
      <section className="py-28 sm:py-36 px-6 bg-bg-secondary transition-colors duration-300">
        <div className="max-w-2xl mx-auto text-center">
          <ScrollReveal>
            <div className="w-12 h-12 rounded-xl bg-bg-elevated border border-border flex items-center justify-center mx-auto mb-6 shadow-[var(--shadow-xs)]">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="text-text-muted">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" strokeLinecap="round" strokeLinejoin="round" />
              </svg>
            </div>
          </ScrollReveal>
          <ScrollReveal delay={0.1}>
            <h2 className="text-3xl sm:text-4xl font-[var(--font-display)] font-bold text-text-primary leading-[1.1] tracking-[-0.03em] mb-4">
              Or just ask anything.
            </h2>
          </ScrollReveal>
          <ScrollReveal delay={0.2}>
            <p className="text-text-muted text-base mb-10 max-w-md mx-auto leading-relaxed">
              Not sure where to start? Describe what you need and we&apos;ll figure it out together.
            </p>
          </ScrollReveal>
          <ScrollReveal delay={0.3}>
            <button
              onClick={() => onStart("")}
              className="inline-flex items-center gap-2.5 px-7 py-3.5 bg-text-primary text-bg-primary font-semibold rounded-xl hover:opacity-90 transition-all duration-200 shadow-[var(--shadow-lg)] active:scale-[0.97] cursor-pointer text-sm"
            >
              Start a Conversation
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <path d="M5 12h14M12 5l7 7-7 7" />
              </svg>
            </button>
          </ScrollReveal>
        </div>
      </section>

      {/* ── Footer ── */}
      <footer className="py-8 px-6 border-t border-border transition-colors duration-300">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Logo size={22} />
            <span className="text-xs font-semibold text-text-muted tracking-tight">PickR</span>
          </div>
          <p className="text-[11px] text-text-muted">Powered by AI</p>
        </div>
      </footer>
    </div>
  );
}
