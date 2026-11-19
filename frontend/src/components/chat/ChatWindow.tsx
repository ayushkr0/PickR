"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from "motion/react";
import { clearSession, whyThisPick } from "@/lib/api";
import { streamMessage } from "@/lib/stream";
import { useAuth } from "@/lib/auth";
import type { Message as MessageType, Product } from "@/types";
import ChatInput from "./ChatInput";
import Message from "./Message";
import ProductGrid from "@/components/products/ProductGrid";
import ProductGridSkeleton from "@/components/products/ProductSkeleton";
import LandingPage, { Logo } from "@/components/landing/LandingPage";
import WhyThisModal from "@/components/products/WhyThisModal";
import AuthModal from "@/components/auth/AuthModal";
import ChatSidebar from "./ChatSidebar";
import JourneyTracker from "./JourneyTracker";
import { useTheme } from "@/lib/theme";
import { useToast } from "@/components/ui/Toast";
import { fetchSessionMessages } from "@/lib/sessions";

// Quick reply suggestions based on conversation stage
const QUICK_REPLIES: Record<string, string[]> = {
  follow_up: [
    "I'm a student",
    "For professional work",
    "Under £500",
    "Under £1000",
    "No budget limit",
  ],
  recommendation: [
    "Show me cheaper options",
    "Anything more premium?",
    "Compare the top two",
    "Start over with new criteria",
  ],
  conversation: [
    "Tell me more",
    "What would you recommend?",
    "Thanks!",
  ],
};

function ChatHeader({ onReset, onNewChat, onSignIn, onToggleSidebar }: { onReset: () => void; onNewChat: () => void; onSignIn: () => void; onToggleSidebar: () => void }) {
  const { theme, toggleTheme } = useTheme();
  const { user, logout, loading: authLoading } = useAuth();

  const initials = user?.display_name
    ? user.display_name.split(" ").map((w) => w[0]).join("").toUpperCase().slice(0, 2)
    : user?.email?.[0]?.toUpperCase() ?? "?";

  return (
    <header className="flex items-center justify-between px-4 sm:px-6 py-3.5 shrink-0 border-b border-border bg-nav-bg backdrop-blur-xl sticky top-0 z-20">
      <div className="flex items-center gap-2.5">
        {user && (
          <button
            onClick={onToggleSidebar}
            className="w-8 h-8 flex items-center justify-center rounded-lg hover:bg-bg-secondary text-text-muted hover:text-text-primary transition-colors cursor-pointer"
            aria-label="Toggle history"
            title="Chat history"
          >
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <line x1="3" y1="6" x2="21" y2="6" /><line x1="3" y1="12" x2="21" y2="12" /><line x1="3" y1="18" x2="21" y2="18" />
            </svg>
          </button>
        )}
        <button onClick={onReset} className="flex items-center gap-2 cursor-pointer hover:opacity-80 transition-opacity">
          <Logo size={28} />
          <h1 className="font-[var(--font-display)] text-sm font-semibold text-text-primary tracking-tight">PickR</h1>
        </button>
      </div>
      <div className="flex items-center gap-1.5">
        <button
          onClick={toggleTheme}
          className="w-8 h-8 flex items-center justify-center rounded-lg hover:bg-bg-secondary text-text-muted hover:text-text-primary transition-colors cursor-pointer"
          aria-label={`Switch to ${theme === "light" ? "dark" : "light"} mode`}
        >
          {theme === "light" ? (
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
            </svg>
          ) : (
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" className="text-amber">
              <circle cx="12" cy="12" r="5" />
              <line x1="12" y1="1" x2="12" y2="3" /><line x1="12" y1="21" x2="12" y2="23" />
              <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" /><line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
              <line x1="1" y1="12" x2="3" y2="12" /><line x1="21" y1="12" x2="23" y2="12" />
              <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" /><line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
            </svg>
          )}
        </button>
        <motion.button
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          onClick={onNewChat}
          className="w-8 h-8 flex items-center justify-center rounded-lg hover:bg-bg-secondary text-text-muted hover:text-text-primary transition-colors cursor-pointer"
          aria-label="New chat"
          title="New chat"
        >
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M12 20h9" /><path d="M16.5 3.5a2.12 2.12 0 0 1 3 3L7 19l-4 1 1-4Z" />
          </svg>
        </motion.button>
        <motion.button
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          onClick={onReset}
          className="text-[11px] font-medium text-text-muted hover:text-text-primary transition-colors px-2.5 py-1.5 rounded-lg hover:bg-bg-secondary border border-transparent hover:border-border cursor-pointer hidden sm:block"
        >
          Home
        </motion.button>

        {/* Auth: user avatar or sign-in */}
        {!authLoading && (
          user ? (
            <div className="relative group ml-1">
              <button
                className="w-8 h-8 rounded-full bg-accent text-white text-[11px] font-bold flex items-center justify-center cursor-pointer hover:ring-2 hover:ring-accent/30 transition-all"
                aria-label="Account menu"
              >
                {initials}
              </button>
              <div className="absolute right-0 top-full mt-1.5 w-48 bg-bg-elevated border border-border rounded-xl shadow-[var(--shadow-lg)] opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-30 py-1.5">
                <div className="px-3 py-2 border-b border-border">
                  <p className="text-xs font-semibold text-text-primary truncate">{user.display_name || "User"}</p>
                  <p className="text-[10px] text-text-muted truncate">{user.email}</p>
                </div>
                <button
                  onClick={logout}
                  className="w-full text-left px-3 py-2 text-xs text-text-muted hover:text-red hover:bg-bg-secondary transition-colors cursor-pointer"
                >
                  Sign Out
                </button>
              </div>
            </div>
          ) : (
            <motion.button
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              onClick={onSignIn}
              className="text-[11px] font-semibold text-accent hover:text-accent-hover transition-colors px-2.5 py-1.5 rounded-lg hover:bg-accent-light border border-accent/20 hover:border-accent/40 cursor-pointer ml-1"
            >
              Sign In
            </motion.button>
          )
        )}
      </div>
    </header>
  );
}

// Quick reply suggestion chips
function QuickReplies({ stage, onSelect, disabled }: { stage?: string; onSelect: (text: string) => void; disabled: boolean }) {
  const suggestions = QUICK_REPLIES[stage || "conversation"] || QUICK_REPLIES.conversation;

  if (disabled) return null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.3, duration: 0.3 }}
      className="flex flex-wrap gap-1.5 ml-11"
    >
      {suggestions.map((text) => (
        <button
          key={text}
          onClick={() => onSelect(text)}
          className="text-[11px] font-medium text-accent bg-accent-light hover:bg-accent/15 border border-accent/15 hover:border-accent/30 px-3 py-1.5 rounded-full transition-all duration-200 cursor-pointer active:scale-95"
        >
          {text}
        </button>
      ))}
    </motion.div>
  );
}

export default function ChatWindow() {
  const [messages, setMessages] = useState<MessageType[]>([]);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [streamPhase, setStreamPhase] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [hasInteracted, setHasInteracted] = useState(false);
  const [whyLoading, setWhyLoading] = useState<string | null>(null);
  const [whyModal, setWhyModal] = useState<{ product: Product; explanation: string | null } | null>(null);
  const [authOpen, setAuthOpen] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const whyCacheRef = useRef<Map<string, string>>(new Map());
  const bottomRef = useRef<HTMLDivElement>(null);
  const { toast } = useToast();

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const WELCOME_MESSAGE: MessageType = {
    role: "assistant",
    content: "Hey! I'm Orin, your personal product advisor. Tell me what you're looking for — whether it's a laptop, headphones, or a camera — and I'll find the perfect match for you.",
    stage: "conversation",
  };

  async function handleSend(text: string) {
    if (!hasInteracted) {
      setHasInteracted(true);
      if (!text.trim()) {
        setMessages([WELCOME_MESSAGE]);
        return;
      }
      setMessages([WELCOME_MESSAGE]);
    }
    if (!text.trim()) return;

    setError(null);
    const userMsg: MessageType = { role: "user", content: text };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);
    setStreamPhase("Orin is thinking...");

    const streamIdx = { current: -1 };

    try {
      await streamMessage(text, sessionId, {
        onToken(token) {
          setMessages((prev) => {
            const msgs = [...prev];
            if (streamIdx.current === -1) {
              streamIdx.current = msgs.length;
              msgs.push({ role: "assistant", content: token ?? "", isStreaming: true });
            } else {
              const msg = { ...msgs[streamIdx.current] };
              msg.content = (msg.content ?? "") + (token ?? "");
              msgs[streamIdx.current] = msg;
            }
            return msgs;
          });
          setStreamPhase(null);
        },
        onNode(node, status) {
          if (status === "completed") return;
          const labels: Record<string, string> = {
            extract_intent: "Understanding your request...",
            retrieve: "Searching products...",
            recommend: "Crafting recommendations...",
            validate: "Verifying picks...",
            converse: "Orin is responding...",
            follow_up: "Orin is responding...",
            fallback: "Orin is responding...",
          };
          setStreamPhase(labels[node] ?? "Orin is thinking...");
        },
        onProducts(products, bestPickIndex) {
          setMessages((prev) => {
            const msgs = [...prev];
            if (streamIdx.current >= 0) {
              const msg = { ...msgs[streamIdx.current] };
              msg.products = products;
              msg.bestPickIndex = bestPickIndex;
              msgs[streamIdx.current] = msg;
            }
            return msgs;
          });
        },
        onStage(stage) {
          setMessages((prev) => {
            const msgs = [...prev];
            if (streamIdx.current >= 0) {
              const msg = { ...msgs[streamIdx.current] };
              msg.stage = stage;
              msgs[streamIdx.current] = msg;
            }
            return msgs;
          });
        },
        onDone(sid) {
          if (!sessionId) setSessionId(sid);
          setMessages((prev) => {
            const msgs = [...prev];
            if (streamIdx.current >= 0) {
              const msg = { ...msgs[streamIdx.current] };
              msg.isStreaming = false;
              msgs[streamIdx.current] = msg;
            }
            return msgs;
          });
        },
        onError(detail) {
          setError(detail);
        },
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setLoading(false);
      setStreamPhase(null);
    }
  }

  const handleCloseWhyModal = useCallback(() => setWhyModal(null), []);

  async function handleWhyThisPick(product: Product) {
    if (!sessionId || whyLoading) return;

    const cached = whyCacheRef.current.get(product.id);
    if (cached) {
      setWhyModal({ product, explanation: cached });
      return;
    }

    setWhyModal({ product, explanation: null });
    setWhyLoading(product.id);
    try {
      const explanation = await whyThisPick(sessionId, product.name);
      whyCacheRef.current.set(product.id, explanation);
      setWhyModal({ product, explanation });
    } catch {
      toast("Couldn't get explanation. Try again.", "error");
      setWhyModal(null);
    } finally {
      setWhyLoading(null);
    }
  }

  async function handleReset() {
    if (sessionId) await clearSession(sessionId);
    setSessionId(null);
    setMessages([]);
    setError(null);
    setHasInteracted(false);
  }

  async function handleNewChat() {
    setSessionId(null);
    setMessages([WELCOME_MESSAGE]);
    setError(null);
  }

  async function handleSelectSession(sid: string) {
    try {
      const data = await fetchSessionMessages(sid);
      const loaded: MessageType[] = data.messages.map((m) => ({
        role: m.role as "user" | "assistant",
        content: m.content,
      }));
      setSessionId(sid);
      setMessages(loaded);
      setError(null);
      setHasInteracted(true);
    } catch {
      toast("Couldn't load session", "error");
    }
  }

  if (!hasInteracted) {
    return <LandingPage onStart={handleSend} />;
  }

  // Get the last assistant message's stage for quick replies
  const lastAssistantMsg = [...messages].reverse().find((m) => m.role === "assistant");
  const lastStage = lastAssistantMsg?.stage;
  const showQuickReplies = !loading && messages.length > 0 && lastAssistantMsg;

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.4 }}
      className="flex h-full w-full"
    >
      <ChatSidebar
        open={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        onSelectSession={handleSelectSession}
        onNewChat={handleNewChat}
        activeSessionId={sessionId}
      />

      <div className="flex flex-col flex-1 min-w-0 max-w-3xl mx-auto w-full">
      <ChatHeader onReset={handleReset} onNewChat={handleNewChat} onSignIn={() => setAuthOpen(true)} onToggleSidebar={() => setSidebarOpen((v) => !v)} />

      <div className="flex-1 overflow-y-auto px-4 sm:px-6 py-6 space-y-5">
        <AnimatePresence mode="popLayout">
          {messages.map((msg, i) => (
            <motion.div
              key={`${i}-${msg.role}`}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -6 }}
              transition={{ duration: 0.3, ease: [0.22, 1, 0.36, 1] }}
            >
              <Message message={msg} />
              {msg.products && msg.products.length > 0 && (
                <motion.div
                  initial={{ opacity: 0, y: 14 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.1, duration: 0.4 }}
                  className="mt-4 ml-11"
                >
                  <JourneyTracker messages={messages.slice(0, i + 1)} />
                  <ProductGrid
                    products={msg.products}
                    bestPickIndex={msg.bestPickIndex ?? 0}
                    onWhyThisPick={handleWhyThisPick}
                  />
                </motion.div>
              )}
            </motion.div>
          ))}
        </AnimatePresence>

        {/* Quick reply chips */}
        <AnimatePresence>
          {showQuickReplies && (
            <QuickReplies stage={lastStage} onSelect={handleSend} disabled={loading} />
          )}
        </AnimatePresence>

        {/* Loading / typing indicator — only show when loading AND no tokens have arrived yet */}
        <AnimatePresence>
          {loading && streamPhase && (
            <motion.div
              initial={{ opacity: 0, y: 6 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0 }}
              className="space-y-4"
            >
              <div className="flex items-start gap-3">
                <img src="/pickr-avatar.png" alt="PickR" className="w-8 h-8 rounded-lg shrink-0 object-cover animate-pulse" />
                <div className="bg-bg-secondary border border-border rounded-2xl rounded-tl-md px-4 py-3">
                  <div className="flex gap-1.5 items-center">
                    <span className="typing-dot w-1.5 h-1.5 bg-text-muted rounded-full" />
                    <span className="typing-dot w-1.5 h-1.5 bg-text-muted rounded-full" />
                    <span className="typing-dot w-1.5 h-1.5 bg-text-muted rounded-full" />
                    <span className="text-[11px] text-text-muted ml-2 font-medium">{streamPhase}</span>
                  </div>
                </div>
              </div>

              {messages.length >= 3 && (
                <div className="ml-11">
                  <ProductGridSkeleton />
                </div>
              )}
            </motion.div>
          )}
        </AnimatePresence>

        {/* Error */}
        <AnimatePresence>
          {error && (
            <motion.div
              initial={{ opacity: 0, scale: 0.97 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.97 }}
              className="flex items-center gap-2.5 text-sm text-red bg-red-light border border-red/15 rounded-xl px-4 py-3 font-medium"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" className="shrink-0">
                <circle cx="12" cy="12" r="10" />
                <line x1="12" y1="8" x2="12" y2="12" />
                <line x1="12" y1="16" x2="12.01" y2="16" />
              </svg>
              {error}
              <button
                onClick={() => {
                  setError(null);
                  // Retry last message
                  const lastUserMsg = [...messages].reverse().find((m) => m.role === "user");
                  if (lastUserMsg) {
                    setMessages((prev) => prev.slice(0, -1));
                    handleSend(lastUserMsg.content);
                  }
                }}
                className="ml-auto text-xs font-semibold text-red hover:underline cursor-pointer shrink-0"
              >
                Retry
              </button>
            </motion.div>
          )}
        </AnimatePresence>

        <div ref={bottomRef} />
      </div>

      <div className="px-4 sm:px-6 pt-2 pb-5 shrink-0 bg-nav-bg backdrop-blur-xl border-t border-border">
        <ChatInput onSend={handleSend} disabled={loading} />
      </div>

      <WhyThisModal
        product={whyModal?.product ?? null}
        explanation={whyModal?.explanation ?? null}
        loading={whyLoading !== null}
        onClose={handleCloseWhyModal}
      />
      <AuthModal open={authOpen} onClose={() => setAuthOpen(false)} />
      </div>
    </motion.div>
  );
}
