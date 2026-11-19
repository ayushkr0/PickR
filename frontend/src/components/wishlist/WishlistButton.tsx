"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { useWishlist } from "@/lib/wishlist";
import WishlistDrawer from "./WishlistDrawer";

export default function WishlistButton() {
  const { savedProducts } = useWishlist();
  const [drawerOpen, setDrawerOpen] = useState(false);

  const count = savedProducts.length;

  return (
    <>
      <AnimatePresence>
        {count > 0 && (
          <motion.button
            initial={{ scale: 0, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0, opacity: 0 }}
            transition={{ type: "spring", stiffness: 400, damping: 25 }}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setDrawerOpen(true)}
            className="fixed bottom-6 right-6 z-40 flex items-center gap-2 bg-accent text-white px-4 py-3 rounded-xl shadow-[var(--shadow-lg),var(--shadow-glow)] hover:bg-accent-hover transition-colors duration-200 cursor-pointer"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" stroke="none">
              <path d="M11.995 7.233c1.178-2.14 3.476-3.233 5.755-3.233C20.643 4 23 6.357 23 9.25c0 4.178-4.488 7.67-9.397 11.41L12 21.855l-1.603-1.194C5.488 16.92 1 13.428 1 9.25 1 6.357 3.357 4 6.25 4c2.279 0 4.577 1.093 5.745 3.233z" />
            </svg>
            <span className="text-sm font-bold">{count}</span>
          </motion.button>
        )}
      </AnimatePresence>

      <WishlistDrawer open={drawerOpen} onClose={() => setDrawerOpen(false)} />
    </>
  );
}
