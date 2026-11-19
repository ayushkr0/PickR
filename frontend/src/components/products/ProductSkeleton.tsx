"use client";

import { motion } from "motion/react";

function Shimmer({ className = "" }: { className?: string }) {
  return (
    <div className={`relative overflow-hidden rounded bg-bg-secondary ${className}`}>
      <div className="absolute inset-0 -translate-x-full animate-[shimmer_1.5s_ease-in-out_infinite] bg-gradient-to-r from-transparent via-bg-tertiary/60 to-transparent" />
    </div>
  );
}

function SkeletonCard({ isBestPick = false }: { isBestPick?: boolean }) {
  return (
    <div className={`rounded-xl border overflow-hidden flex flex-col ${
      isBestPick
        ? "bg-bg-elevated border-accent/20"
        : "bg-bg-elevated border-border"
    }`}>
      {/* Image area */}
      <div className={`${isBestPick ? "h-40" : "h-28"} bg-bg-secondary flex items-center justify-center`}>
        <Shimmer className={`${isBestPick ? "w-24 h-24" : "w-16 h-16"} rounded-lg`} />
      </div>

      {/* Content */}
      <div className="p-4 space-y-3">
        <div className="flex items-start justify-between gap-2">
          <div className="space-y-1.5 flex-1">
            <Shimmer className="h-2.5 w-12" />
            <Shimmer className="h-3.5 w-3/4" />
          </div>
          <Shimmer className="h-4 w-14" />
        </div>
        <div className="flex gap-1.5">
          <Shimmer className="h-5 w-28" />
          <Shimmer className="h-5 w-24" />
        </div>
        <Shimmer className="h-8 w-full rounded-lg" />
      </div>
    </div>
  );
}

export default function ProductGridSkeleton() {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.3 }}
      className="space-y-4"
    >
      {/* Best pick skeleton */}
      <div>
        <div className="flex items-center gap-3 mb-3">
          <div className="h-px flex-1 bg-accent/20" />
          <Shimmer className="h-3 w-32" />
          <div className="h-px flex-1 bg-accent/20" />
        </div>
        <SkeletonCard isBestPick />
      </div>

      {/* Other options skeleton */}
      <div>
        <div className="flex items-center gap-3 mb-3">
          <div className="h-px flex-1 bg-border" />
          <Shimmer className="h-3 w-24" />
          <div className="h-px flex-1 bg-border" />
        </div>
        <div className="grid grid-cols-1 xs:grid-cols-2 gap-3">
          {[1, 2, 3, 4].map((i) => (
            <SkeletonCard key={i} />
          ))}
        </div>
      </div>
    </motion.div>
  );
}
