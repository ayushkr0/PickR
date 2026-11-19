import type { Product } from "@/types";
import ProductCard from "./ProductCard";

interface Props {
  products: Product[];
  bestPickIndex?: number;
  onWhyThisPick?: (product: Product) => void;
}

export default function ProductGrid({ products, bestPickIndex = 0, onWhyThisPick }: Props) {
  if (products.length === 0) return null;

  const bestPick = products[bestPickIndex];
  const others = products.filter((_, i) => i !== bestPickIndex);

  return (
    <div className="space-y-4">
      {/* Best Pick — full width */}
      {bestPick && (
        <div>
          <div className="flex items-center gap-3 mb-3">
            <div className="h-px flex-1 bg-accent/30" />
            <span className="text-[10px] font-bold uppercase tracking-[0.12em] text-accent px-1 flex items-center gap-1.5">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
              Best Recommendation
            </span>
            <div className="h-px flex-1 bg-accent/30" />
          </div>
          <ProductCard product={bestPick} index={0} isBestPick onWhyThisPick={onWhyThisPick} />
        </div>
      )}

      {/* Other options */}
      {others.length > 0 && (
        <div>
          <div className="flex items-center gap-3 mb-3">
            <div className="h-px flex-1 bg-border" />
            <span className="text-[10px] font-bold uppercase tracking-[0.12em] text-text-muted px-1">
              Other Options
            </span>
            <div className="h-px flex-1 bg-border" />
          </div>
          <div className="grid grid-cols-1 xs:grid-cols-2 gap-3">
            {others.map((product, i) => (
              <ProductCard key={product.id} product={product} index={i + 1} onWhyThisPick={onWhyThisPick} />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
