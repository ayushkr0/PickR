import { getAuthHeaders } from "@/lib/auth";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export interface SessionSummary {
  id: string;
  category: string | null;
  preview: string;
  updated_at: string | null;
}

export interface SessionDetail {
  id: string;
  category: string | null;
  messages: { role: "user" | "assistant"; content: string; created_at: string | null }[];
}

export async function fetchSessions(): Promise<SessionSummary[]> {
  const res = await fetch(`${BASE_URL}/api/sessions`, {
    headers: getAuthHeaders(),
  });
  if (!res.ok) return [];
  return res.json();
}

export async function fetchSessionMessages(sessionId: string): Promise<SessionDetail> {
  const res = await fetch(`${BASE_URL}/api/sessions/${sessionId}`, {
    headers: getAuthHeaders(),
  });
  if (!res.ok) throw new Error("Failed to load session");
  return res.json();
}

export async function deleteSession(sessionId: string): Promise<void> {
  await fetch(`${BASE_URL}/api/sessions/${sessionId}`, {
    method: "DELETE",
    headers: getAuthHeaders(),
  });
}
