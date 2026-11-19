"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "motion/react";
import { useAuth } from "@/lib/auth";

interface Stats {
  total_sessions: number;
  total_users: number;
  sessions_today: number;
  avg_messages: number;
  categories: { name: string; count: number; pct: number }[];
  recent_sessions: {
    id: string;
    category: string | null;
    preview: string;
    created_at: string | null;
    updated_at: string | null;
  }[];
}

const CATEGORY_ICONS: Record<string, string> = {
  laptop: "💻",
  headphone: "🎧",
  camera: "📷",
  phone: "📱",
  tablet: "📱",
  monitor: "🖥️",
};

function timeAgo(dateStr: string | null): string {
  if (!dateStr) return "";
  const diff = Date.now() - new Date(dateStr).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return "Just now";
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  const days = Math.floor(hrs / 24);
  if (days < 7) return `${days}d ago`;
  return new Date(dateStr).toLocaleDateString();
}

export default function AdminPage() {
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (authLoading) return;
    if (!user) {
      router.push("/");
      return;
    }

    const token = localStorage.getItem("pickr_token");
    if (!token) {
      router.push("/");
      return;
    }

    fetch(`${process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000"}/api/admin/stats`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((r) => {
        if (r.status === 403) throw new Error("not_admin");
        if (!r.ok) throw new Error("Failed to load stats");
        return r.json();
      })
      .then(setStats)
      .catch((e) => {
        if (e.message === "not_admin") router.push("/");
        else setError(e.message);
      })
      .finally(() => setLoading(false));
  }, [user, authLoading, router]);

  if (loading) {
    return (
      <div className="min-h-screen bg-bg-primary flex items-center justify-center">
        <div className="flex gap-1.5">
          <span className="typing-dot w-2 h-2 bg-accent rounded-full" />
          <span className="typing-dot w-2 h-2 bg-accent rounded-full" />
          <span className="typing-dot w-2 h-2 bg-accent rounded-full" />
        </div>
      </div>
    );
  }

  if (error || !stats) {
    return (
      <div className="min-h-screen bg-bg-primary flex items-center justify-center">
        <p className="text-text-muted">{error || "Failed to load"}</p>
      </div>
    );
  }

  const maxCategoryCount = Math.max(...stats.categories.map((c) => c.count), 1);

  return (
    <div className="min-h-screen bg-bg-primary">
      {/* Header */}
      <header className="border-b border-border bg-bg-card/80 backdrop-blur-md sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button
              onClick={() => router.push("/")}
              className="w-8 h-8 flex items-center justify-center rounded-lg hover:bg-bg-secondary transition-colors cursor-pointer"
            >
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M19 12H5" /><polyline points="12 19 5 12 12 5" />
              </svg>
            </button>
            <h1 className="text-lg font-semibold text-text-primary font-[family-name:var(--font-space)]">
              Admin Dashboard
            </h1>
          </div>
          <span className="text-xs text-text-muted">
            Logged in as {user?.display_name || user?.email}
          </span>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">
        {/* Stat Cards */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          {[
            { label: "Total Sessions", value: stats.total_sessions, icon: "💬" },
            { label: "Total Users", value: stats.total_users, icon: "👤" },
            { label: "Sessions Today", value: stats.sessions_today, icon: "📅" },
            { label: "Avg Messages", value: stats.avg_messages, icon: "📊" },
          ].map((card, i) => (
            <motion.div
              key={card.label}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.05 }}
              className="bg-bg-card border border-border rounded-[var(--radius-md)] p-5 shadow-[var(--shadow-sm)]"
            >
              <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-semibold text-text-muted uppercase tracking-wider">{card.label}</span>
                <span className="text-lg">{card.icon}</span>
              </div>
              <p className="text-3xl font-bold text-text-primary font-[family-name:var(--font-space)]">
                {card.value}
              </p>
            </motion.div>
          ))}
        </div>

        <div className="grid lg:grid-cols-2 gap-6">
          {/* Category Breakdown */}
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-bg-card border border-border rounded-[var(--radius-md)] p-6 shadow-[var(--shadow-sm)]"
          >
            <h2 className="text-sm font-semibold text-text-primary mb-5 font-[family-name:var(--font-space)]">
              Categories
            </h2>
            {stats.categories.length === 0 ? (
              <p className="text-xs text-text-muted text-center py-8">No category data yet</p>
            ) : (
              <div className="space-y-3.5">
                {stats.categories.map((cat) => (
                  <div key={cat.name}>
                    <div className="flex items-center justify-between mb-1.5">
                      <span className="text-xs font-medium text-text-primary flex items-center gap-1.5">
                        <span>{CATEGORY_ICONS[cat.name?.toLowerCase() ?? ""] ?? "📦"}</span>
                        {cat.name || "Unknown"}
                      </span>
                      <span className="text-xs text-text-muted">{cat.count} ({cat.pct}%)</span>
                    </div>
                    <div className="h-2 bg-bg-secondary rounded-full overflow-hidden">
                      <motion.div
                        initial={{ width: 0 }}
                        animate={{ width: `${(cat.count / maxCategoryCount) * 100}%` }}
                        transition={{ duration: 0.6, delay: 0.3 }}
                        className="h-full bg-accent rounded-full"
                      />
                    </div>
                  </div>
                ))}
              </div>
            )}
          </motion.div>

          {/* Recent Sessions */}
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="bg-bg-card border border-border rounded-[var(--radius-md)] p-6 shadow-[var(--shadow-sm)]"
          >
            <h2 className="text-sm font-semibold text-text-primary mb-5 font-[family-name:var(--font-space)]">
              Recent Sessions
            </h2>
            {stats.recent_sessions.length === 0 ? (
              <p className="text-xs text-text-muted text-center py-8">No sessions yet</p>
            ) : (
              <div className="space-y-1">
                {stats.recent_sessions.map((s) => (
                  <div
                    key={s.id}
                    className="flex items-center gap-3 px-3 py-2.5 rounded-[var(--radius-sm)] hover:bg-bg-secondary transition-colors"
                  >
                    <span className="text-sm shrink-0">
                      {CATEGORY_ICONS[s.category?.toLowerCase() ?? ""] ?? "💬"}
                    </span>
                    <div className="flex-1 min-w-0">
                      <p className="text-xs font-medium text-text-primary truncate">
                        {s.preview || s.category || "Chat"}
                      </p>
                      <p className="text-[10px] text-text-muted">
                        {s.category && <span className="capitalize">{s.category} · </span>}
                        {timeAgo(s.updated_at)}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </motion.div>
        </div>
      </main>
    </div>
  );
}
