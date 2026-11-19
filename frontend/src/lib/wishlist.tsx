"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";
import type { Product } from "@/types";

const STORAGE_KEY = "product-advisor-wishlist";

interface WishlistContextValue {
  savedProducts: Product[];
  toggleProduct: (product: Product) => void;
  isProductSaved: (id: string) => boolean;
  clearAll: () => void;
}

const WishlistContext = createContext<WishlistContextValue | null>(null);

export function WishlistProvider({ children }: { children: ReactNode }) {
  const [savedProducts, setSavedProducts] = useState<Product[]>([]);
  const [hydrated, setHydrated] = useState(false);

  // Hydrate from localStorage on mount
  useEffect(() => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        const parsed = JSON.parse(raw);
        if (Array.isArray(parsed)) {
          setSavedProducts(parsed);
        }
      }
    } catch {
      // ignore corrupted data
    }
    setHydrated(true);
  }, []);

  // Persist to localStorage whenever savedProducts changes (after hydration)
  useEffect(() => {
    if (hydrated) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(savedProducts));
    }
  }, [savedProducts, hydrated]);

  const toggleProduct = useCallback((product: Product) => {
    setSavedProducts((prev) => {
      const exists = prev.some((p) => p.id === product.id);
      if (exists) {
        return prev.filter((p) => p.id !== product.id);
      }
      return [...prev, product];
    });
  }, []);

  const isProductSaved = useCallback(
    (id: string) => savedProducts.some((p) => p.id === id),
    [savedProducts]
  );

  const clearAll = useCallback(() => {
    setSavedProducts([]);
  }, []);

  return (
    <WishlistContext.Provider
      value={{ savedProducts, toggleProduct, isProductSaved, clearAll }}
    >
      {children}
    </WishlistContext.Provider>
  );
}

export function useWishlist() {
  const ctx = useContext(WishlistContext);
  if (!ctx) {
    throw new Error("useWishlist must be used within a WishlistProvider");
  }
  return ctx;
}
