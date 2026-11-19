"use client";

import { motion } from "motion/react";
import type { Message } from "@/types";

interface Props {
  messages: Message[];
}

interface Step {
  label: string;
  type: "category" | "need" | "budget" | "result";
}

const CATEGORY_PATTERNS = /\b(laptops?|headphones?|cameras?|phones?|tablets?|monitors?|earbuds?|speakers?)\b/i;
const BUDGET_PATTERNS = /(?:under|below|around|about|max|up to|budget)?\s*[£$€]\s*[\d,]+|[\d,]+\s*(?:pounds|dollars|euros|£|\$|€)/i;

function extractSteps(messages: Message[]): Step[] {
  const steps: Step[] = [];
  const seen = new Set<string>();

  for (const msg of messages) {
    if (msg.role !== "user") continue;
    const text = msg.content;

    const catMatch = text.match(CATEGORY_PATTERNS);
    if (catMatch) {
      let cat = catMatch[1].toLowerCase().replace(/s$/, "");
      cat = cat.charAt(0).toUpperCase() + cat.slice(1);
      const key = `cat:${cat.toLowerCase()}`;
      if (!seen.has(key)) {
        seen.add(key);
        steps.push({ label: cat, type: "category" });
      }
    }

    const budgetMatch = text.match(BUDGET_PATTERNS);
    if (budgetMatch) {
      const key = `budget:${budgetMatch[0].toLowerCase().trim()}`;
      if (!seen.has(key)) {
        seen.add(key);
        steps.push({ label: budgetMatch[0].trim(), type: "budget" });
      }
    }

    const needWords = text.match(/\b(?:for|gaming|work|school|student|professional|running|travel|vlogging|photography|music|studio|office|portable)\b/gi);
    if (needWords) {
      for (const word of needWords) {
        if (word.toLowerCase() === "for") continue;
        const key = `need:${word.toLowerCase()}`;
        if (!seen.has(key)) {
          seen.add(key);
          steps.push({ label: word.charAt(0).toUpperCase() + word.slice(1).toLowerCase(), type: "need" });
        }
      }
    }
  }

  const lastMsg = messages.filter((m) => m.role === "assistant").pop();
  if (lastMsg?.products && lastMsg.products.length > 0) {
    steps.push({ label: `${lastMsg.products.length} ${lastMsg.products.length === 1 ? "pick" : "picks"}`, type: "result" });
  }

  return steps;
}

const TYPE_STYLES: Record<string, string> = {
  category: "bg-accent-light text-accent border-accent/20",
  need: "bg-blue-light text-blue border-blue/20",
  budget: "bg-green-light text-green border-green/20",
  result: "bg-pink-light text-pink border-pink/20",
};

export default function JourneyTracker({ messages }: Props) {
  const steps = extractSteps(messages);
  if (steps.length === 0) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: -6 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
      className="flex items-center gap-1.5 flex-wrap mb-3"
    >
      {steps.map((step, i) => (
        <span key={`${step.type}-${step.label}-${i}`} className="flex items-center gap-1.5">
          {i > 0 && (
            <svg width="10" height="10" viewBox="0 0 16 16" fill="none" className="text-text-muted/40 shrink-0">
              <path d="M6 4l4 4-4 4" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
          )}
          <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-md border ${TYPE_STYLES[step.type] || "bg-bg-secondary text-text-muted border-border"}`}>
            {step.label}
          </span>
        </span>
      ))}
    </motion.div>
  );
}
