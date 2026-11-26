"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import type { Product } from "@/types";
import { useWishlist } from "@/lib/wishlist";
import { useToast } from "@/components/ui/Toast";
import { trackEvent } from "@/lib/pendo";

const CATEGORY_EMOJI: Record<string, string> = {
  laptop: "\uD83D\uDCBB",
  headphone: "\uD83C\uDFA7",
  camera: "\uD83D\uDCF7",
};

interface Props {
  product: Product;
  index?: number;
  isBestPick?: boolean;
  onWhyThisPick?: (product: Product) => void;
}

export default function ProductCard({ product, index = 0, isBestPick = false, onWhyThisPick }: Props) {
  const { savedProducts, toggleProduct, isProductSaved } = useWishlist();
  const { toast } = useToast();
  const saved = isProductSaved(product.id);
  const [imgError, setImgError] = useState(false);
  const [showWhy, setShowWhy] = useState(false);
  const [lightboxOpen, setLightboxOpen] = useState(false);
  const [priceCtx, setPriceCtx] = useState<{ diff_pct: number; verdict: string } | null>(null);

  useEffect(() => {
    const base = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";
    fetch(`${base}/api/products/${product.id}/price-context`)
      .then((r) => r.ok ? r.json() : null)
      .then((d) => { if (d) setPriceCtx(d); })
      .catch(() => {});
  }, [product.id]);

  return (
    <motion.div
      initial={{ opacity: 0, y: 14 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.06, duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
      className={`group rounded-xl border overflow-hidden flex flex-col hover:shadow-[var(--shadow-lg)] transition-all duration-300 ${
        isBestPick
          ? "bg-bg-elevated border-accent/40 ring-1 ring-accent/20 hover:border-accent/60"
          : "bg-bg-elevated border-border hover:border-border-dark"
      }`}
    >
      {/* Image */}
      <div className={`${isBestPick ? "h-48 p-6" : "h-36 p-4"} flex items-center justify-center relative overflow-hidden bg-white`}>
        {product.image_url && !imgError ? (
          <button
            type="button"
            onClick={() => setLightboxOpen(true)}
            className="h-full w-full cursor-zoom-in"
            aria-label={`View ${product.name} image`}
          >
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={product.image_url}
              alt={product.name}
              className="h-full w-full object-contain group-hover:scale-105 transition-transform duration-500"
              onError={() => setImgError(true)}
            />
          </button>
        ) : (
          <span className={`${isBestPick ? "text-5xl" : "text-3xl"} opacity-20 group-hover:scale-110 transition-transform duration-500`}>
            {CATEGORY_EMOJI[product.category] ?? "\uD83D\uDCE6"}
          </span>
        )}

        {/* Badges row */}
        <div className="absolute top-3 left-3 flex items-center gap-1.5">
          {isBestPick && (
            <span className="text-[10px] font-bold uppercase tracking-wider text-white bg-accent px-2 py-0.5 rounded-md flex items-center gap-1">
              <svg width="10" height="10" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
              Best Pick
            </span>
          )}
          <span className="text-[10px] font-medium uppercase tracking-wider text-accent bg-accent-light px-2 py-0.5 rounded-md">
            {product.category}
          </span>
        </div>

        <motion.button
          whileTap={{ scale: 0.75 }}
          onClick={(e) => {
            e.preventDefault();
            e.stopPropagation();
            const wasSaved = isProductSaved(product.id);
            toggleProduct(product);
            // Pendo: product saved to or removed from the wishlist
            trackEvent("wishlist_product_toggled", {
              action: wasSaved ? "removed" : "saved",
              product_id: product.id,
              product_category: product.category,
              product_brand: product.brand,
              product_price: product.price,
              wishlist_count: wasSaved ? Math.max(savedProducts.length - 1, 0) : savedProducts.length + 1,
            });
            toast(wasSaved ? `Removed ${product.name}` : `Saved ${product.name}`, wasSaved ? "info" : "success");
          }}
          className="absolute top-3 right-3 w-8 h-8 flex items-center justify-center rounded-lg bg-bg-elevated/90 backdrop-blur-sm border border-border hover:border-border-dark transition-colors cursor-pointer z-10 shadow-[var(--shadow-xs)]"
          aria-label={saved ? "Remove from wishlist" : "Add to wishlist"}
        >
          <motion.svg
            key={saved ? "saved" : "unsaved"}
            initial={{ scale: 0.5 }}
            animate={{ scale: 1 }}
            transition={{ type: "spring", stiffness: 500, damping: 20 }}
            width="14" height="14" viewBox="0 0 24 24"
            fill={saved ? "currentColor" : "none"} stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
            className={saved ? "text-accent" : "text-text-muted"}
          >
            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z" />
          </motion.svg>
        </motion.button>
      </div>

      {/* Content */}
      <div className="p-4 flex flex-col flex-1 gap-2">
        <div className="flex items-start justify-between gap-2">
          <div>
            <p className="text-[10px] font-medium text-text-muted uppercase tracking-wider mb-0.5">{product.brand}</p>
            <h3 className="font-[var(--font-display)] text-sm font-semibold text-text-primary leading-snug tracking-tight">{product.name}</h3>
          </div>
          <div className="text-right shrink-0">
            <p className="text-base font-bold text-text-primary tracking-tight">£{product.price.toLocaleString()}</p>
            {priceCtx && priceCtx.verdict !== "average" && (
              <p className={`text-[9px] font-semibold ${priceCtx.verdict === "below_average" ? "text-green" : "text-amber"}`}>
                {Math.abs(priceCtx.diff_pct)}% {priceCtx.verdict === "below_average" ? "below" : "above"} avg
              </p>
            )}
          </div>
        </div>

        <div className="flex flex-wrap gap-1.5 text-[10px]">
          {product.pros.slice(0, 2).map((pro, i) => (
            <span key={i} className="inline-flex items-center gap-1 text-green bg-green/[0.08] px-1.5 py-0.5 rounded max-w-[140px] truncate">
              <svg width="8" height="8" viewBox="0 0 16 16" fill="currentColor" className="shrink-0"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.75.75 0 0 1 1.06-1.06L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z" /></svg>
              {pro}
            </span>
          ))}
          {product.cons.slice(0, 1).map((con, i) => (
            <span key={i} className="inline-flex items-center gap-1 text-red bg-red/[0.08] px-1.5 py-0.5 rounded max-w-[140px] truncate">
              <svg width="8" height="8" viewBox="0 0 16 16" fill="currentColor" className="shrink-0"><path d="M3.72 3.72a.75.75 0 0 1 1.06 0L8 6.94l3.22-3.22a.75.75 0 1 1 1.06 1.06L9.06 8l3.22 3.22a.75.75 0 1 1-1.06 1.06L8 9.06l-3.22 3.22a.75.75 0 0 1-1.06-1.06L6.94 8 3.72 4.78a.75.75 0 0 1 0-1.06Z" /></svg>
              {con}
            </span>
          ))}
        </div>

        <div className="mt-auto flex gap-2">
          {onWhyThisPick && (
            <button
              onClick={(e) => { e.preventDefault(); e.stopPropagation(); onWhyThisPick(product); }}
              className="flex-1 flex items-center justify-center gap-1.5 text-[11px] font-medium text-accent hover:bg-accent-light active:scale-[0.98] transition-all duration-200 rounded-lg py-2 border border-accent/20 hover:border-accent/40 cursor-pointer"
            >
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="10" /><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3" /><path d="M12 17h.01" />
              </svg>
              Why this?
            </button>
          )}
          {product.affiliate_url && (
            <a href={product.affiliate_url} target="_blank" rel="noopener noreferrer"
              onClick={() => {
                // Pendo: visitor opened the affiliate retailer link
                trackEvent("retailer_link_opened", {
                  product_id: product.id,
                  product_category: product.category,
                  product_brand: product.brand,
                  product_price: product.price,
                  is_best_pick: isBestPick,
                  card_index: index,
                });
              }}
              className={`${onWhyThisPick ? "flex-1" : "w-full"} flex items-center justify-center gap-2 text-xs font-semibold text-white bg-accent hover:bg-accent-hover active:scale-[0.98] transition-all duration-200 rounded-lg py-2 shadow-[var(--shadow-glow)]`}>
              View Deal
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><path d="M7 17l9.2-9.2M17 17V7.8H7.8" /></svg>
            </a>
          )}
        </div>
      </div>
      {/* Image Lightbox */}
      <AnimatePresence>
        {lightboxOpen && product.image_url && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="fixed inset-0 z-[70] flex items-center justify-center p-4"
            onClick={() => setLightboxOpen(false)}
            onKeyDown={(e) => { if (e.key === "Escape") setLightboxOpen(false); }}
          >
            <div className="absolute inset-0 bg-black/80 backdrop-blur-sm" />
            <motion.div
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              transition={{ duration: 0.2 }}
              className="relative max-w-2xl max-h-[80vh] w-full"
              onClick={(e) => e.stopPropagation()}
            >
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src={product.image_url}
                alt={product.name}
                className="w-full h-full object-contain rounded-xl"
              />
              <button
                onClick={() => setLightboxOpen(false)}
                className="absolute top-3 right-3 w-9 h-9 flex items-center justify-center rounded-full bg-black/50 text-white hover:bg-black/70 transition-colors cursor-pointer"
                aria-label="Close image"
              >
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />
                </svg>
              </button>
              <p className="text-center text-white/80 text-sm mt-3 font-medium">{product.name}</p>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.div>
  );
}
