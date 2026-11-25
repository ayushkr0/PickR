type PendoTrackValue = string | number | boolean | null;

interface PendoAgent {
  track: (eventName: string, properties?: Record<string, PendoTrackValue>) => void;
}

declare global {
  interface Window {
    pendo?: PendoAgent;
  }
}

/**
 * Sends a Pendo Track Event when the Pendo agent is loaded in the browser.
 * Tracking failures are swallowed so they never affect the app.
 */
export function trackEvent(eventName: string, properties: Record<string, PendoTrackValue> = {}): void {
  if (typeof window === "undefined") return;
  try {
    window.pendo?.track(eventName, properties);
  } catch {
    // Ignore tracking errors
  }
}
