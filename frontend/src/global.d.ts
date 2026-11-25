// Global loaded by the Novus by Pendo install snippet in src/app/layout.tsx.
type PendoMetadataValue = string | number | boolean | null | undefined | string[];

interface PendoIdentity {
  visitor: { id: string } & Record<string, PendoMetadataValue>;
  account?: { id: string } & Record<string, PendoMetadataValue>;
}

interface PendoAgent {
  initialize(options: PendoIdentity & Record<string, unknown>): void;
  identify(options: PendoIdentity): void;
  // Not stubbed by the install snippet, so it's undefined until the agent loads.
  clearSession?: () => void;
}

declare const pendo: PendoAgent;
