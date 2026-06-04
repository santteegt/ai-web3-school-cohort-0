/**
 * P-005 — Auditable Settlement Records
 *
 * Appends one JSON record per successful payment to logs/audit.json.
 * Prints a Basescan link after each record.
 * Prints a session summary at end of run.
 */

import { writeFileSync, readFileSync, existsSync, mkdirSync } from 'node:fs';
import { dirname } from 'node:path';
import { config } from './config.js';

export interface AuditRecord {
  timestamp: string;
  pactId: string;
  endpoint: string;
  /** USD amount paid for this call */
  amountPaidUsd: string;
  txHash: string | null;
  receiverAddress: string;
  responseStatus: number;
  /** First 100 chars of the inference result */
  resultSnippet: string;
}

// ── Write ─────────────────────────────────────────────────────────────────────

export function appendAuditRecord(record: Omit<AuditRecord, 'timestamp'>): void {
  const entry: AuditRecord = {
    timestamp: new Date().toISOString(),
    ...record,
  };

  const logPath = config.audit.logPath;
  mkdirSync(dirname(logPath), { recursive: true });

  const existing: AuditRecord[] = existsSync(logPath)
    ? (JSON.parse(readFileSync(logPath, 'utf8')) as AuditRecord[])
    : [];

  existing.push(entry);
  writeFileSync(logPath, JSON.stringify(existing, null, 2));

  console.log(`[audit] ✓ Record saved to ${logPath}`);

  if (entry.txHash) {
    console.log(`[audit]   Basescan: ${config.audit.basescanUrl}/tx/${entry.txHash}`);
  } else {
    console.log('[audit]   tx_hash pending (may appear in Basescan shortly)');
  }
}

// ── Summary ───────────────────────────────────────────────────────────────────

export function loadAuditRecords(): AuditRecord[] {
  if (!existsSync(config.audit.logPath)) return [];
  return JSON.parse(readFileSync(config.audit.logPath, 'utf8')) as AuditRecord[];
}

export function printSessionSummary(records: AuditRecord[]): void {
  const successful = records.filter(r => r.responseStatus === 200);
  const totalUsd = successful.reduce((sum, r) => sum + parseFloat(r.amountPaidUsd), 0);

  console.log('\n╔════════════════════════════════╗');
  console.log('║       Session Summary          ║');
  console.log('╚════════════════════════════════╝');
  console.log(`  Successful calls: ${successful.length}`);
  console.log(`  Total spent:      $${totalUsd.toFixed(4)} USD`);

  if (successful.length > 0) {
    const last = successful[successful.length - 1]!;
    console.log(`  Last result:      "${last.resultSnippet}"`);
    if (last.txHash) {
      console.log(`  Last tx:          ${config.audit.basescanUrl}/tx/${last.txHash}`);
    }
  }

  console.log(`  Audit log:        ${config.audit.logPath}`);
  console.log('════════════════════════════════');
}
