import type { Product } from "@/types";
import { getAuthHeaders } from "@/lib/auth";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export interface StreamCallbacks {
  onToken: (text: string) => void;
  onNode: (node: string, status: string) => void;
  onProducts: (products: Product[], bestPickIndex: number) => void;
  onStage: (stage: "follow_up" | "recommendation" | "conversation") => void;
  onDone: (sessionId: string) => void;
  onError: (detail: string) => void;
}

export async function streamMessage(
  message: string,
  sessionId: string | null,
  callbacks: StreamCallbacks
): Promise<void> {
  const res = await fetch(`${BASE_URL}/api/chat/stream`, {
    method: "POST",
    headers: { "Content-Type": "application/json", ...getAuthHeaders() },
    body: JSON.stringify({ message, session_id: sessionId }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail ?? "Something went wrong. Please try again.");
  }

  const reader = res.body?.getReader();
  if (!reader) throw new Error("No response body");

  const decoder = new TextDecoder();
  let buffer = "";
  let currentEvent = "";

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });

    const lines = buffer.split("\n");
    buffer = lines.pop() ?? "";

    for (const line of lines) {
      if (line.startsWith("event: ")) {
        currentEvent = line.slice(7).trim();
      } else if (line.startsWith("data: ") && currentEvent) {
        const data = JSON.parse(line.slice(6));
        switch (currentEvent) {
          case "token":
            if (data.text != null) callbacks.onToken(data.text);
            break;
          case "node":
            callbacks.onNode(data.node, data.status);
            break;
          case "products":
            callbacks.onProducts(data.products, data.best_pick_index);
            break;
          case "stage":
            callbacks.onStage(data.stage);
            break;
          case "done":
            callbacks.onDone(data.session_id);
            break;
          case "error":
            callbacks.onError(data.detail);
            break;
        }
        currentEvent = "";
      }
    }
  }
}
