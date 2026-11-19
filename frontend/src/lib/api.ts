import type { ChatResponse } from "@/types";
import { getAuthHeaders } from "@/lib/auth";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export async function sendMessage(
  message: string,
  sessionId: string | null
): Promise<ChatResponse> {
  const res = await fetch(`${BASE_URL}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...getAuthHeaders() },
    body: JSON.stringify({ message, session_id: sessionId }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail ?? "Something went wrong. Please try again.");
  }

  return res.json();
}

export async function clearSession(sessionId: string): Promise<void> {
  await fetch(`${BASE_URL}/api/chat/${sessionId}`, { method: "DELETE" });
}

export async function whyThisPick(
  sessionId: string,
  productName: string
): Promise<string> {
  const res = await fetch(`${BASE_URL}/api/chat/why`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...getAuthHeaders() },
    body: JSON.stringify({ session_id: sessionId, product_name: productName }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail ?? "Could not get explanation.");
  }

  const data = await res.json();
  return data.explanation;
}
