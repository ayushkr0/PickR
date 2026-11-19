"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { useWishlist } from "@/lib/wishlist";
import ComparisonView from "./ComparisonView";

interface Props {
  open: boolean;
  onClose: () => void;
}

export default function WishlistDrawer({ open, onClose }: Props) {
  const { savedProducts, toggleProduct, clearAll } = useWishlist();
  const [showComparison, setShowComparison] = useState(false);

  const canCompare = savedProducts.length >= 2 && savedProducts.length <= 3;

  return (
    <>
      <AnimatePresence>
        {open && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
              onClick={onClose}
              className="fixed inset-0 bg-overlay backdrop-blur-[2px] z-50"
            />

            <motion.div
              initial={{ x: "100%" }}
              animate={{ x: 0 }}
              exit={{ x: "100%" }}
              transition={{ type: "spring", stiffness: 350, damping: 35 }}
              className="fixed top-0 right-0 h-full w-full max-w-md bg-bg-primary border-l border-border z-50 flex flex-col shadow-[var(--shadow-xl)]"
            >
              <div className="flex items-center justify-between px-5 py-4 border-b border-border shrink-0">
                <div className="flex items-center gap-2.5">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" className="text-accent">
                    <path d="M11.995 7.233c1.178-2.14 3.476-3.233 5.755-3.233C20.643 4 23 6.357 23 9.25c0 4.178-4.488 7.67-9.397 11.41L12 21.855l-1.603-1.194C5.488 16.92 1 13.428 1 9.25 1 6.357 3.357 4 6.25 4c2.279 0 4.577 1.093 5.745 3.233z" />
                  </svg>
                  <h2 className="text-sm font-semibold text-text-primary">Saved Products</h2>
                  <span className="text-[11px] font-bold text-text-muted bg-bg-secondary px-2 py-0.5 rounded-md">{savedProducts.length}</span>
                </div>
                <button onClick={onClose} className="w-8 h-8 flex items-center justify-center rounded-lg hover:bg-bg-secondary text-text-muted hover:text-text-primary transition-colors cursor-pointer">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />
                  </svg>
                </button>
              </div>

              <div className="flex-1 overflow-y-auto px-5 py-4 space-y-3">
                {savedProducts.length === 0 ? (
                  <div className="flex flex-col items-center justify-center h-full text-text-muted">
                    <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" className="opacity-20 mb-3">
                      <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                    <p className="text-sm font-medium">No saved products yet</p>
                    <p className="text-xs mt-1">Tap the heart icon on any product to save it</p>
                  </div>
                ) : (
                  <AnimatePresence mode="popLayout">
                    {savedProducts.map((product) => (
                      <motion.div
                        key={product.id}
                        layout
                        initial={{ opacity: 0, x: 20 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: -20, scale: 0.95 }}
                        transition={{ duration: 0.25, ease: [0.22, 1, 0.36, 1] }}
                        className="flex items-center gap-3 p-3 bg-bg-secondary border border-border rounded-xl min-h-[72px]"
                      >
                        <div className="w-14 h-14 rounded-lg bg-white border border-border flex items-center justify-center shrink-0 overflow-hidden">
                          {product.image_url ? (
                            // eslint-disable-next-line @next/next/no-img-element
                            <img src={product.image_url} alt={product.name} className="w-full h-full object-contain p-1.5" />
                          ) : (
                            <span className="text-xl opacity-20">
                              {product.category === "laptop" ? "\uD83D\uDCBB" : product.category === "headphone" ? "\uD83C\uDFA7" : "\uD83D\uDCF7"}
                            </span>
                          )}
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="text-[10px] font-medium text-text-muted uppercase tracking-wider">{product.brand}</p>
                          <p className="text-sm font-semibold text-text-primary truncate leading-snug">{product.name}</p>
                          <div className="flex items-center gap-2 mt-0.5">
                            <span className="text-sm font-bold text-text-primary">£{product.price.toLocaleString()}</span>
                            <span className="text-[10px] font-medium uppercase tracking-wider text-accent bg-accent-light px-1.5 py-px rounded">{product.category}</span>
                          </div>
                        </div>
                        <button onClick={() => toggleProduct(product)} className="w-7 h-7 flex items-center justify-center rounded-lg hover:bg-red-light text-text-muted hover:text-red transition-colors shrink-0 cursor-pointer">
                          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />
                          </svg>
                        </button>
                      </motion.div>
                    ))}
                  </AnimatePresence>
                )}
              </div>

              {savedProducts.length > 0 && (
                <div className="px-5 py-4 border-t border-border shrink-0 space-y-2.5">
                  <button
                    onClick={() => setShowComparison(true)}
                    disabled={!canCompare}
                    className={`w-full flex items-center justify-center gap-2 text-sm font-semibold py-3 rounded-xl transition-all duration-200 cursor-pointer ${
                      canCompare
                        ? "bg-accent text-white hover:bg-accent-hover active:scale-[0.98] shadow-[var(--shadow-glow)]"
                        : "bg-bg-secondary text-text-muted cursor-not-allowed"
                    }`}
                  >
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <line x1="18" y1="20" x2="18" y2="10" /><line x1="12" y1="20" x2="12" y2="4" /><line x1="6" y1="20" x2="6" y2="14" />
                    </svg>
                    {canCompare ? `Compare ${savedProducts.length} Products` : savedProducts.length === 1 ? "Save 1 more to compare" : "Save 2\u20133 products to compare"}
                  </button>
                  <button onClick={clearAll} className="w-full text-xs font-medium text-text-muted hover:text-red transition-colors py-2 cursor-pointer">
                    Clear All
                  </button>
                </div>
              )}
            </motion.div>
          </>
        )}
      </AnimatePresence>

      <ComparisonView open={showComparison} onClose={() => setShowComparison(false)} products={savedProducts} />
    </>
  );
}
