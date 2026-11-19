export interface Product {
  id: string;
  name: string;
  category: string;
  brand: string;
  price: number;
  image_url: string | null;
  affiliate_url: string | null;
  specs: Record<string, unknown>;
  summary: string | null;
  pros: string[];
  cons: string[];
}

export interface Message {
  role: "user" | "assistant";
  content: string;
  products?: Product[];
  bestPickIndex?: number;
  stage?: "follow_up" | "recommendation" | "conversation";
  isStreaming?: boolean;
}

export interface ChatResponse {
  session_id: string;
  reply: string;
  products: Product[];
  best_pick_index: number;
  follow_up_questions: string[];
  stage: "follow_up" | "recommendation" | "conversation";
}
