"use client";

import { useEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { useAuth } from "@/lib/auth";
import { fetchSessions, deleteSession, type SessionSummary } from "@/lib/sessions";

interface Props {
  open: boolean;
  onClose: () => void;
  onSelectSession: (sessionId: string) => void;
  onNewChat: () => void;
  activeSessionId: string | null;
}

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

function groupSessions(sessions: SessionSummary[]) {
  const now = new Date();
  const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
  const yesterday = new Date(today.getTime() - 86400000);
  const weekAgo = new Date(today.getTime() - 7 * 86400000);

  const groups: { label: string; items: SessionSummary[] }[] = [
    { label: "Today", items: [] },
    { label: "Yesterday", items: [] },
    { label: "This Week", items: [] },
    { label: "Older", items: [] },
  ];

  for (const s of sessions) {
    const d = s.updated_at ? new Date(s.updated_at) : new Date(0);
    if (d >= today) groups[0].items.push(s);
    else if (d >= yesterday) groups[1].items.push(s);
    else if (d >= weekAgo) groups[2].items.push(s);
    else groups[3].items.push(s);
  }

  return groups.filter((g) => g.items.length > 0);
}

const CATEGORY_ICONS: Record<string, string> = {
  laptop: "💻",
  headphone: "🎧",
  camera: "📷",
  phone: "📱",
  tablet: "📱",
  monitor: "🖥️",
};

export default function ChatSidebar({ open, onClose, onSelectSession, onNewChat, activeSessionId }: Props) {
  const { user } = useAuth();
  const [sessions, setSessions] = useState<SessionSummary[]>([]);
  const [loading, setLoading] = useState(false);
  const [deletingId, setDeletingId] = useState<string | null>(null);

  const refreshRef = useRef(0);

  useEffect(() => {
    if (!open || !user) return;
    const id = ++refreshRef.current;
    setLoading(true);
    fetchSessions()
      .then((data) => { if (id === refreshRef.current) setSessions(data); })
      .catch(() => {})
      .finally(() => { if (id === refreshRef.current) setLoading(false); });
  }, [open, user]);

  async function handleDelete(e: React.MouseEvent, id: string) {
    e.stopPropagation();
    setDeletingId(id);
    try {
      await deleteSession(id);
      setSessions((prev) => prev.filter((s) => s.id !== id));
    } catch {
      // silent
    } finally {
      setDeletingId(null);
    }
  }

  const groups = groupSessions(sessions);

  return (
    <>
      {/* Mobile overlay */}
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/30 z-30 md:hidden"
            onClick={onClose}
          />
        )}
      </AnimatePresence>

      {/* Sidebar */}
      <motion.aside
        initial={false}
        animate={{ x: open ? 0 : -300 }}
        transition={{ type: "spring", damping: 25, stiffness: 300 }}
        className={`fixed md:relative z-40 md:z-auto top-0 left-0 h-full w-[280px] bg-bg-primary border-r border-border flex flex-col shrink-0 ${
          !open ? "md:hidden" : ""
        }`}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-4 py-3.5 border-b border-border shrink-0">
          <span className="text-xs font-semibold text-text-muted uppercase tracking-wider">History</span>
          <div className="flex items-center gap-1">
            <button
              onClick={() => { onNewChat(); onClose(); }}
              className="w-7 h-7 flex items-center justify-center rounded-lg hover:bg-bg-secondary text-text-muted hover:text-text-primary transition-colors cursor-pointer"
              title="New chat"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="12" y1="5" x2="12" y2="19" /><line x1="5" y1="12" x2="19" y2="12" />
              </svg>
            </button>
            <button
              onClick={onClose}
              className="w-7 h-7 flex items-center justify-center rounded-lg hover:bg-bg-secondary text-text-muted hover:text-text-primary transition-colors cursor-pointer md:hidden"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>
          </div>
        </div>

        {/* Session list */}
        <div className="flex-1 overflow-y-auto py-2">
          {!user && (
            <p className="text-xs text-text-muted px-4 py-8 text-center">Sign in to see your chat history</p>
          )}

          {user && loading && sessions.length === 0 && (
            <div className="flex justify-center py-8">
              <span className="typing-dot w-1.5 h-1.5 bg-text-muted rounded-full" />
              <span className="typing-dot w-1.5 h-1.5 bg-text-muted rounded-full ml-1" />
              <span className="typing-dot w-1.5 h-1.5 bg-text-muted rounded-full ml-1" />
            </div>
          )}

          {user && !loading && sessions.length === 0 && (
            <p className="text-xs text-text-muted px-4 py-8 text-center">No chats yet. Start a conversation!</p>
          )}

          {groups.map((group) => (
            <div key={group.label} className="mb-2">
              <p className="text-[10px] font-semibold text-text-muted uppercase tracking-wider px-4 py-1.5">{group.label}</p>
              {group.items.map((s) => (
                <div
                  key={s.id}
                  role="button"
                  tabIndex={0}
                  onClick={() => { onSelectSession(s.id); onClose(); }}
                  onKeyDown={(e) => { if (e.key === "Enter") { onSelectSession(s.id); onClose(); } }}
                  className={`group w-full text-left px-4 py-2.5 flex items-center gap-2.5 hover:bg-bg-secondary transition-colors cursor-pointer ${
                    s.id === activeSessionId ? "bg-accent-light border-r-2 border-accent" : ""
                  }`}
                >
                  <span className="text-sm shrink-0">{CATEGORY_ICONS[s.category?.toLowerCase() ?? ""] ?? "💬"}</span>
                  <div className="flex-1 min-w-0">
                    <p className="text-xs font-medium text-text-primary truncate">
                      {s.preview || s.category || "Chat"}
                    </p>
                    <p className="text-[10px] text-text-muted">{timeAgo(s.updated_at)}</p>
                  </div>
                  <button
                    onClick={(e) => handleDelete(e, s.id)}
                    disabled={deletingId === s.id}
                    className="opacity-0 group-hover:opacity-100 w-6 h-6 flex items-center justify-center rounded hover:bg-red-light text-text-muted hover:text-red transition-all cursor-pointer shrink-0"
                    title="Delete"
                  >
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <polyline points="3 6 5 6 21 6" /><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2" />
                    </svg>
                  </button>
                </div>
              ))}
            </div>
          ))}
        </div>
      </motion.aside>
    </>
  );
}
