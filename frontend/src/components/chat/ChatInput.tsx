"use client";

import { KeyboardEvent, useEffect, useRef, useState } from "react";

interface Props {
  onSend: (message: string) => void;
  disabled: boolean;
}

export default function ChatInput({ onSend, disabled }: Props) {
  const [value, setValue] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-focus textarea when AI finishes responding
  useEffect(() => {
    if (!disabled && textareaRef.current) {
      textareaRef.current.focus();
    }
  }, [disabled]);

  function handleSend() {
    const trimmed = value.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setValue("");
    if (textareaRef.current) textareaRef.current.style.height = "auto";
  }

  function handleKeyDown(e: KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  function handleInput() {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = `${Math.min(el.scrollHeight, 160)}px`;
  }

  return (
    <div className="relative">
      <div className="flex items-end gap-2 bg-bg-elevated border border-border rounded-xl px-4 py-3 shadow-[var(--shadow-sm)] focus-within:border-accent/30 focus-within:shadow-[0_0_0_3px_rgba(108,92,231,0.06)] transition-all duration-200">
        <textarea
          ref={textareaRef}
          rows={1}
          value={value}
          onChange={(e) => setValue(e.target.value)}
          onKeyDown={handleKeyDown}
          onInput={handleInput}
          disabled={disabled}
          placeholder="Describe what you need..."
          className="flex-1 resize-none bg-transparent text-sm text-text-primary placeholder-text-muted outline-none leading-relaxed disabled:opacity-50"
        />
        <button
          onClick={handleSend}
          disabled={disabled || !value.trim()}
          aria-label="Send message"
          className="w-8 h-8 rounded-lg bg-accent text-white flex items-center justify-center shrink-0 transition-all duration-200 hover:bg-accent-hover disabled:opacity-25 disabled:cursor-not-allowed active:scale-95 cursor-pointer"
        >
          <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <path d="M5 12h14M12 5l7 7-7 7" />
          </svg>
        </button>
      </div>
      <p className="text-center text-[11px] text-text-muted mt-2">
        <kbd className="px-1.5 py-0.5 rounded bg-bg-secondary text-text-secondary text-[10px] font-medium border border-border">Enter</kbd> to send
        <span className="mx-1.5 text-border-dark">&middot;</span>
        <kbd className="px-1.5 py-0.5 rounded bg-bg-secondary text-text-secondary text-[10px] font-medium border border-border">Shift + Enter</kbd> new line
      </p>
    </div>
  );
}
