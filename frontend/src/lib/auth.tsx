"use client";

import { createContext, useCallback, useContext, useEffect, useState } from "react";
import { trackEvent } from "@/lib/pendo";

const BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

interface AuthUser {
  id: string;
  email: string;
  display_name: string | null;
  is_admin: boolean;
}

interface AuthContextType {
  user: AuthUser | null;
  token: string | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, displayName?: string, honeypot?: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  token: null,
  loading: true,
  login: async () => {},
  register: async () => {},
  logout: () => {},
});

export function useAuth() {
  return useContext(AuthContext);
}

export function getAuthToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("pickr_token");
}

export function getAuthHeaders(): Record<string, string> {
  const token = getAuthToken();
  return token ? { Authorization: `Bearer ${token}` } : {};
}

function hasActiveChatSession(): boolean {
  try {
    return sessionStorage.getItem("pickr_session_id") !== null;
  } catch {
    return false;
  }
}

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const stored = localStorage.getItem("pickr_token");
    if (!stored) {
      // eslint-disable-next-line react-hooks/set-state-in-effect
      setLoading(false);
      return;
    }
    setToken(stored);
    fetch(`${BASE_URL}/api/auth/me`, {
      headers: { Authorization: `Bearer ${stored}` },
    })
      .then((r) => (r.ok ? r.json() : Promise.reject()))
      .then((data) => setUser(data))
      .catch(() => {
        localStorage.removeItem("pickr_token");
        setToken(null);
      })
      .finally(() => setLoading(false));
  }, []);

  const login = useCallback(async (email: string, password: string) => {
    const res = await fetch(`${BASE_URL}/api/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail ?? "Login failed");
    }
    const data = await res.json();
    localStorage.setItem("pickr_token", data.token);
    setToken(data.token);
    setUser(data.user);
    // Pendo: sign-in succeeded
    trackEvent("sign_in_completed", {
      user_id: data.user?.id ?? null,
      is_admin: Boolean(data.user?.is_admin),
      had_active_session: hasActiveChatSession(),
    });
  }, []);

  const register = useCallback(async (email: string, password: string, displayName?: string, honeypot?: string) => {
    const res = await fetch(`${BASE_URL}/api/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password, display_name: displayName, honeypot: honeypot || undefined }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail ?? "Registration failed");
    }
    const data = await res.json();
    localStorage.setItem("pickr_token", data.token);
    setToken(data.token);
    setUser(data.user);
    // Pendo: account registration succeeded
    trackEvent("account_registered", {
      user_id: data.user?.id ?? null,
      has_display_name: Boolean(data.user?.display_name),
      had_active_session: hasActiveChatSession(),
    });
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem("pickr_token");
    setToken(null);
    setUser(null);
  }, []);

  return (
    <AuthContext value={{ user, token, loading, login, register, logout }}>
      {children}
    </AuthContext>
  );
}
