"use client";

import { useEffect, useRef } from "react";
import { motion, AnimatePresence } from "motion/react";
import type { Product } from "@/types";

interface Props {
  product: Product | null;
  explanation: string | null;
  loading: boolean;
  onClose: () => void;
}

export default function WhyThisModal({ product, explanation, loading, onClose }: Props) {
  const overlayRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!product) return;
    function onKey(e: KeyboardEvent) {
      if (e.key === "Escape") onClose();
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [product, onClose]);

  return (
    <AnimatePresence>
      {product && (
        <motion.div
          ref={overlayRef}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.2 }}
          className="fixed inset-0 z-50 flex items-center justify-center p-4"
          onClick={(e) => { if (e.target === overlayRef.current) onClose(); }}
        >
          {/* Backdrop */}
          <div className="absolute inset-0 bg-black/40 backdrop-blur-sm" />

          {/* Modal */}
          <motion.div
            initial={{ opacity: 0, scale: 0.92, y: 12 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.92, y: 12 }}
            transition={{ duration: 0.25, ease: [0.22, 1, 0.36, 1] }}
            className="relative bg-bg-elevated border border-border rounded-2xl shadow-[var(--shadow-lg)] w-full max-w-md overflow-hidden"
          >
            {/* Header */}
            <div className="flex items-center justify-between px-5 pt-5 pb-3">
              <div className="flex items-center gap-3 min-w-0">
                {product.image_url ? (
                  // eslint-disable-next-line @next/next/no-img-element
                  <img
                    src={product.image_url}
                    alt={product.name}
                    className="w-10 h-10 rounded-lg object-contain bg-white border border-border shrink-0"
                  />
                ) : (
                  <div className="w-10 h-10 rounded-lg bg-accent-light flex items-center justify-center shrink-0">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="text-accent">
                      <circle cx="12" cy="12" r="10" /><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3" /><path d="M12 17h.01" />
                    </svg>
                  </div>
                )}
                <div className="min-w-0">
                  <h3 className="text-sm font-semibold text-text-primary truncate">Why this pick?</h3>
                  <p className="text-[11px] text-text-muted truncate">{product.name}</p>
                </div>
              </div>
              <button
                onClick={onClose}
                className="w-8 h-8 flex items-center justify-center rounded-lg hover:bg-bg-secondary text-text-muted hover:text-text-primary transition-colors cursor-pointer shrink-0"
                aria-label="Close"
              >
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round">
                  <path d="M18 6L6 18" /><path d="M6 6l12 12" />
                </svg>
              </button>
            </div>

            {/* Price badge */}
            <div className="px-5 pb-3">
              <span className="text-xs font-bold text-accent bg-accent-light px-2.5 py-1 rounded-md">
                £{product.price.toLocaleString()}
              </span>
            </div>

            {/* Divider */}
            <div className="border-t border-border" />

            {/* Content */}
            <div className="px-5 py-4 max-h-[50vh] overflow-y-auto">
              {loading ? (
                <div className="flex items-center gap-3 py-4">
                  <div className="flex gap-1.5">
                    <span className="typing-dot w-2 h-2 bg-accent/50 rounded-full" />
                    <span className="typing-dot w-2 h-2 bg-accent/50 rounded-full" />
                    <span className="typing-dot w-2 h-2 bg-accent/50 rounded-full" />
                  </div>
                  <span className="text-sm text-text-muted">Analyzing this pick for you...</span>
                </div>
              ) : explanation ? (
                <p className="text-sm text-text-secondary leading-relaxed whitespace-pre-wrap">{explanation}</p>
              ) : (
                <p className="text-sm text-text-muted italic">No explanation available.</p>
              )}
            </div>

            {/* Footer */}
            <div className="border-t border-border px-5 py-3 flex justify-end">
              <button
                onClick={onClose}
                className="text-xs font-semibold text-accent hover:bg-accent-light px-4 py-2 rounded-lg transition-colors cursor-pointer"
              >
                Got it
              </button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
