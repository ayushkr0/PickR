import type { Message as MessageType } from "@/types";

interface Props {
  message: MessageType;
}

export default function Message({ message }: Props) {
  const isUser = message.role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"} items-start gap-3`}>
      {!isUser && (
        <img src="/pickr-avatar.png" alt="PickR" className="w-8 h-8 rounded-lg shrink-0 mt-0.5 object-cover" />
      )}

      <div
        className={`max-w-[80%] rounded-2xl px-4 py-3 text-[14px] leading-[1.65] ${
          isUser
            ? "bg-bg-user-bubble text-text-on-dark rounded-tr-md shadow-[var(--shadow-sm)]"
            : "bg-bg-secondary text-text-primary border border-border rounded-tl-md"
        }`}
      >
        <p className="whitespace-pre-wrap">
          {message.content}
          {message.isStreaming && (
            <span className="inline-block w-[2px] h-[1em] bg-accent ml-0.5 align-middle animate-pulse" />
          )}
        </p>
        {message.stage === "recommendation" && !isUser && (
          <div className="mt-2.5 pt-2.5 border-t border-border flex items-center gap-1.5">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" className="text-accent">
              <path d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" fill="currentColor" />
            </svg>
            <span className="text-[11px] font-medium text-accent tracking-wide">
              Personalized picks below
            </span>
          </div>
        )}
      </div>

      {isUser && (
        <div className="w-8 h-8 rounded-lg bg-bg-secondary border border-border flex items-center justify-center shrink-0 mt-0.5">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" className="text-text-muted">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
            <circle cx="12" cy="7" r="4" stroke="currentColor" strokeWidth="2" />
          </svg>
        </div>
      )}
    </div>
  );
}
