"use client";

import { motion, AnimatePresence } from "motion/react";
import type { Product } from "@/types";

interface Props {
  open: boolean;
  onClose: () => void;
  products: Product[];
}

const SPEC_LABELS: Record<string, string> = {
  chip: "Processor",
  ram: "Memory",
  storage: "Storage",
  display: "Display",
  battery_hours: "Battery",
  weight_lbs: "Weight",
  os: "OS",
  gpu: "GPU",
  type: "Type",
  anc: "ANC",
  driver_size_mm: "Driver",
  multipoint: "Multipoint",
  codec: "Codecs",
  sensor: "Sensor",
  megapixels: "Megapixels",
  video: "Video",
  autofocus: "Autofocus",
  stabilization: "Stabilization",
  mount: "Mount",
  battery_shots: "Battery",
};

function formatSpecValue(key: string, val: unknown): string {
  if (val === true) return "Yes";
  if (val === false) return "No";
  if (Array.isArray(val)) return val.join(", ");
  if (key === "battery_hours") return `${val}h`;
  if (key === "weight_lbs") return `${val} lbs`;
  if (key === "driver_size_mm") return `${val}mm`;
  if (key === "megapixels") return `${val}MP`;
  if (key === "battery_shots") return `${val} shots`;
  return String(val ?? "—");
}

function getSharedSpecKeys(products: Product[]): string[] {
  if (products.length === 0) return [];
  const allKeys = products.map((p) => new Set(Object.keys(p.specs || {})));
  const shared = [...allKeys[0]].filter((k) => allKeys.every((s) => s.has(k)));
  const order = Object.keys(SPEC_LABELS);
  return shared.sort((a, b) => {
    const ia = order.indexOf(a);
    const ib = order.indexOf(b);
    return (ia === -1 ? 999 : ia) - (ib === -1 ? 999 : ib);
  });
}

function isNumericSpec(key: string, products: Product[]): boolean {
  return products.every((p) => typeof p.specs?.[key] === "number");
}

function getBestNumericValue(key: string, products: Product[]): string | null {
  if (!isNumericSpec(key, products)) return null;
  const values = products.map((p) => Number(p.specs[key]));
  const higherIsBetter = !["weight_lbs", "price"].includes(key);
  const best = higherIsBetter ? Math.max(...values) : Math.min(...values);
  const bestProduct = products.find((p) => Number(p.specs[key]) === best);
  return bestProduct?.id ?? null;
}

export default function ComparisonView({ open, onClose, products }: Props) {
  if (products.length < 2) return null;

  const cheapestId = products.reduce((min, p) => p.price < min.price ? p : min).id;
  const maxPrice = Math.max(...products.map((p) => p.price));
  const maxPros = Math.max(...products.map((p) => p.pros.length));
  const maxCons = Math.max(...products.map((p) => p.cons.length));
  const specKeys = getSharedSpecKeys(products);

  let rowIdx = 0;

  return (
    <AnimatePresence>
      {open && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.25 }}
          className="fixed inset-0 z-[60] bg-bg-primary/95 backdrop-blur-sm flex flex-col"
        >
          <div className="flex items-center justify-between px-6 py-4 border-b border-border shrink-0">
            <h2 className="text-base font-semibold text-text-primary tracking-tight">Product Comparison</h2>
            <button onClick={onClose} className="flex items-center gap-1.5 text-sm font-medium text-text-muted hover:text-text-primary transition-colors px-3 py-2 rounded-lg hover:bg-bg-secondary cursor-pointer">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />
              </svg>
              Close
            </button>
          </div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1, duration: 0.35 }}
            className="flex-1 overflow-y-auto px-6 py-6"
          >
            <div className="max-w-5xl mx-auto">
              <table className="w-full border-collapse">
                <thead>
                  <tr>
                    <th className="w-[100px]" />
                    {products.map((product) => (
                      <th key={product.id} className="text-center px-4 pb-4 align-bottom">
                        <div className="w-full h-28 bg-bg-secondary rounded-xl border border-border flex items-center justify-center mb-3 relative overflow-hidden">
                          {product.image_url ? (
                            // eslint-disable-next-line @next/next/no-img-element
                            <img src={product.image_url} alt={product.name} className="h-full w-full object-contain p-4" />
                          ) : (
                            <span className="text-3xl opacity-20">
                              {product.category === "laptop" ? "💻" : product.category === "headphone" ? "🎧" : "📷"}
                            </span>
                          )}
                          {product.id === cheapestId && (
                            <span className="absolute top-2 right-2 text-[9px] font-bold uppercase tracking-wider text-green bg-green-light px-2 py-0.5 rounded-md">Best value</span>
                          )}
                        </div>
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  <Row label="Name" i={rowIdx++}>{products.map((p) => <td key={p.id} className="px-4 py-3 text-sm font-semibold text-text-primary text-center">{p.name}</td>)}</Row>
                  <Row label="Brand" i={rowIdx++}>{products.map((p) => <td key={p.id} className="px-4 py-3 text-sm text-text-secondary text-center">{p.brand}</td>)}</Row>

                  {/* Price with visual bar */}
                  <Row label="Price" i={rowIdx++}>{products.map((p) => (
                    <td key={p.id} className="px-4 py-3 text-center">
                      <span className={`text-base font-bold block mb-1.5 ${p.id === cheapestId ? "text-green" : "text-text-primary"}`}>
                        £{p.price.toLocaleString()}
                      </span>
                      <div className="h-1.5 bg-bg-tertiary rounded-full overflow-hidden">
                        <motion.div
                          initial={{ width: 0 }}
                          animate={{ width: `${(p.price / maxPrice) * 100}%` }}
                          transition={{ duration: 0.5, delay: 0.2 }}
                          className={`h-full rounded-full ${p.id === cheapestId ? "bg-green" : "bg-accent-soft"}`}
                        />
                      </div>
                    </td>
                  ))}</Row>

                  {/* Spec rows */}
                  {specKeys.map((key) => {
                    const bestId = getBestNumericValue(key, products);
                    return (
                      <Row key={key} label={SPEC_LABELS[key] || key} i={rowIdx++}>
                        {products.map((p) => (
                          <td key={p.id} className={`px-4 py-3 text-sm text-center ${p.id === bestId ? "text-accent font-semibold" : "text-text-secondary"}`}>
                            {formatSpecValue(key, p.specs?.[key])}
                            {p.id === bestId && <span className="ml-1 text-[9px] text-accent">★</span>}
                          </td>
                        ))}
                      </Row>
                    );
                  })}

                  <Row label="Summary" i={rowIdx++}>{products.map((p) => <td key={p.id} className="px-4 py-3 text-xs text-text-secondary leading-relaxed text-center">{p.summary || "—"}</td>)}</Row>
                  <Row label="Pros" i={rowIdx++}>{products.map((p) => (
                    <td key={p.id} className="px-4 py-3 align-top">
                      <ul className="space-y-1">{p.pros.slice(0, Math.max(maxPros, 3)).map((pro, j) => (
                        <li key={j} className="text-xs text-text-secondary flex gap-1.5 items-start">
                          <span className="text-green shrink-0 mt-[2px]"><svg width="10" height="10" viewBox="0 0 16 16" fill="currentColor"><path d="M13.78 4.22a.75.75 0 0 1 0 1.06l-7.25 7.25a.75.75 0 0 1-1.06 0L2.22 9.28a.75.75 0 0 1 1.06-1.06L6 10.94l6.72-6.72a.75.75 0 0 1 1.06 0Z" /></svg></span>
                          {pro}
                        </li>
                      ))}</ul>
                    </td>
                  ))}</Row>
                  <Row label="Cons" i={rowIdx++}>{products.map((p) => (
                    <td key={p.id} className="px-4 py-3 align-top">
                      <ul className="space-y-1">{p.cons.slice(0, Math.max(maxCons, 3)).map((con, j) => (
                        <li key={j} className="text-xs text-text-secondary flex gap-1.5 items-start">
                          <span className="text-red shrink-0 mt-[2px]"><svg width="10" height="10" viewBox="0 0 16 16" fill="currentColor"><path d="M3.72 3.72a.75.75 0 0 1 1.06 0L8 6.94l3.22-3.22a.75.75 0 1 1 1.06 1.06L9.06 8l3.22 3.22a.75.75 0 1 1-1.06 1.06L8 9.06l-3.22 3.22a.75.75 0 0 1-1.06-1.06L6.94 8 3.72 4.78a.75.75 0 0 1 0-1.06Z" /></svg></span>
                          {con}
                        </li>
                      ))}</ul>
                    </td>
                  ))}</Row>
                </tbody>
              </table>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

function Row({ label, i, children }: { label: string; i: number; children: React.ReactNode }) {
  return (
    <tr className={i % 2 === 0 ? "bg-bg-secondary/50" : ""}>
      <td className="px-4 py-3 text-[10px] font-bold uppercase tracking-wider text-text-muted align-top whitespace-nowrap">{label}</td>
      {children}
    </tr>
  );
}
