"use client";

import { useEffect, useRef, useCallback } from "react";

const GAP = 24;
const BASE_R = 1.2;
const MAX_R = 4.5;
const INFLUENCE = 130;
const EASE = 0.1;

export default function DotGrid() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const mouseRef = useRef({ x: -1000, y: -1000 });
  const animRef = useRef<number>(0);
  const scalesRef = useRef<Float32Array | null>(null);
  const colorRef = useRef("");
  const lastThemeRef = useRef("");

  const draw = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const dpr = window.devicePixelRatio || 1;
    const w = canvas.clientWidth;
    const h = canvas.clientHeight;

    if (canvas.width !== w * dpr || canvas.height !== h * dpr) {
      canvas.width = w * dpr;
      canvas.height = h * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }

    const cols = Math.ceil(w / GAP) + 1;
    const rows = Math.ceil(h / GAP) + 1;
    const total = cols * rows;

    if (!scalesRef.current || scalesRef.current.length !== total) {
      scalesRef.current = new Float32Array(total);
    }

    const theme = document.documentElement.getAttribute("data-theme") || "light";
    if (theme !== lastThemeRef.current) {
      lastThemeRef.current = theme;
      colorRef.current = getComputedStyle(document.documentElement).getPropertyValue("--dot-color").trim();
    }

    // Convert mouse viewport coords to canvas-local coords
    const rect = canvas.getBoundingClientRect();
    const mx = mouseRef.current.x - rect.left;
    const my = mouseRef.current.y - rect.top;
    const scales = scalesRef.current;
    const baseColor = colorRef.current || "rgba(26, 29, 46, 0.07)";

    ctx.clearRect(0, 0, w, h);

    const match = baseColor.match(/rgba?\((\d+),\s*(\d+),\s*(\d+),?\s*([\d.]+)?\)/);
    const cr = match ? +match[1] : 26;
    const cg = match ? +match[2] : 29;
    const cb = match ? +match[3] : 46;
    const baseAlpha = match && match[4] ? +match[4] : 0.07;

    let idx = 0;
    for (let row = 0; row < rows; row++) {
      for (let col = 0; col < cols; col++) {
        const x = col * GAP;
        const y = row * GAP;

        const dx = x - mx;
        const dy = y - my;
        const dist = Math.sqrt(dx * dx + dy * dy);

        const target = dist < INFLUENCE ? 1 - dist / INFLUENCE : 0;

        scales[idx] += (target - scales[idx]) * EASE;
        if (scales[idx] < 0.001) scales[idx] = 0;

        const s = scales[idx];
        const r = BASE_R + (MAX_R - BASE_R) * s;
        const alpha = s > 0.01 ? baseAlpha + s * 0.55 : baseAlpha;

        ctx.beginPath();
        ctx.arc(x, y, r, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(${cr},${cg},${cb},${alpha.toFixed(3)})`;
        ctx.fill();

        idx++;
      }
    }

    animRef.current = requestAnimationFrame(draw);
  }, []);

  useEffect(() => {
    function handleMove(e: MouseEvent) {
      mouseRef.current = { x: e.clientX, y: e.clientY };
    }

    function handleLeave() {
      mouseRef.current = { x: -1000, y: -1000 };
    }

    window.addEventListener("mousemove", handleMove);
    document.addEventListener("mouseleave", handleLeave);
    animRef.current = requestAnimationFrame(draw);

    return () => {
      window.removeEventListener("mousemove", handleMove);
      document.removeEventListener("mouseleave", handleLeave);
      cancelAnimationFrame(animRef.current);
    };
  }, [draw]);

  return (
    <canvas
      ref={canvasRef}
      className="pointer-events-none absolute inset-0 z-[1]"
      style={{ width: "100%", height: "100%" }}
    />
  );
}
