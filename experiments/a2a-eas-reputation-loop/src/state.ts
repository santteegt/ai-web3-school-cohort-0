import { readFileSync, writeFileSync, existsSync } from 'fs';
import { resolve } from 'path';

const STATE_FILE = resolve(process.cwd(), 'state.json');

export interface DemoState {
  clientAgentId?: string;
  devAgentId?: string;
  clientRegTxHash?: string;
  devRegTxHash?: string;
  easSchemaUID?: string;
  easSchemaTxHash?: string;
  a2aTaskId?: string;
  a2aContextId?: string;
  deliverableHash?: string;
  easAttestationUID?: string;
  easAttestTxHash?: string;
  feedbackTxHash?: string;
  clientAddress?: string;
  devAddress?: string;
}

export function loadState(): DemoState {
  if (!existsSync(STATE_FILE)) return {};
  try {
    return JSON.parse(readFileSync(STATE_FILE, 'utf8')) as DemoState;
  } catch {
    return {};
  }
}

export function saveState(patch: Partial<DemoState>): DemoState {
  const current = loadState();
  const next = { ...current, ...patch };
  writeFileSync(STATE_FILE, JSON.stringify(next, null, 2), 'utf8');
  return next;
}

export function clearState(): void {
  if (existsSync(STATE_FILE)) {
    writeFileSync(STATE_FILE, '{}', 'utf8');
  }
}
