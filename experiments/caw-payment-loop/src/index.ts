/**
 * CAW Payment Loop — Entry Point
 *
 * Orchestrates the full loop:
 *   1. Load active Pact or run authorization flow (P-002)
 *   2. Run N paid inference calls (P-003 + P-004)
 *   3. Print session summary (P-005)
 *
 * Prerequisites:
 *   - Stub server running: npm run stub
 *   - .env populated with AGENT_WALLET_API_KEY, AGENT_WALLET_WALLET_ID, STUB_SERVER_ADDRESS
 */

import { loadActivePact, requestAndSubmitPact } from './pactConfig.js';
import { runPaymentLoop } from './paymentLoop.js';
import { loadAuditRecords, printSessionSummary } from './auditLog.js';
import { config } from './config.js';

const CALL_COUNT = parseInt(process.env.CALL_COUNT ?? '3', 10);
const CALL_DELAY_MS = 2_000;

async function main(): Promise<void> {
  console.log('\n╔══════════════════════════════════════╗');
  console.log('║        CAW Payment Loop v0.1         ║');
  console.log('╚══════════════════════════════════════╝');
  console.log(`  CAW API:  ${config.caw.apiUrl}`);
  console.log(`  Wallet:   ${config.caw.walletId}`);
  console.log(`  Stub:     http://localhost:${config.stub.port}/api/inference`);
  console.log(`  Calls:    ${CALL_COUNT}`);
  console.log('═══════════════════════════════════════\n');

  // ── P-002: Get or create Pact ──────────────────────────────────────────────
  let pact;

  try {
    pact = loadActivePact();
    console.log(`[main] Loaded existing pact: ${pact.pactId}`);
    console.log(`[main]   expires: ${new Date(pact.expiresAt).toISOString()}`);
    console.log(`[main]   budget:  $${pact.sessionBudgetUsd} USD / session`);
  } catch (loadErr) {
    const msg = loadErr instanceof Error ? loadErr.message : String(loadErr);
    console.log(`[main] No active pact found: ${msg}`);
    console.log('[main] Starting authorization flow...\n');
    pact = await requestAndSubmitPact();
  }

  // ── P-003 + P-004: Run payment loop ────────────────────────────────────────
  console.log(`\n[main] Starting ${CALL_COUNT} paid inference calls...`);

  let successCount = 0;

  for (let i = 1; i <= CALL_COUNT; i++) {
    console.log(`\n──── Call ${i} / ${CALL_COUNT} ────────────────────────────────`);

    try {
      await runPaymentLoop(pact, i);
      successCount++;
    } catch (err) {
      const msg = err instanceof Error ? err.message : String(err);
      console.error(`[main] Call ${i} failed: ${msg}`);

      // Stop if it's a Pact violation — further calls will also fail
      if (msg.includes('TRANSFER_LIMIT_EXCEEDED') || msg.includes('Pact expired')) {
        console.error('[main] Stopping loop — Pact constraint hit.');
        break;
      }
      // Otherwise continue to next call
    }

    if (i < CALL_COUNT) {
      await new Promise(r => setTimeout(r, CALL_DELAY_MS));
    }
  }

  console.log(`\n[main] Loop complete: ${successCount}/${CALL_COUNT} calls succeeded`);

  // ── P-005: Session summary ─────────────────────────────────────────────────
  const allRecords = loadAuditRecords();
  printSessionSummary(allRecords);
}

main().catch(err => {
  const msg = err instanceof Error ? err.message : String(err);
  console.error(`\n[fatal] ${msg}`);

  if (msg.includes('Missing required environment variable')) {
    console.error('\nSetup checklist:');
    console.error('  1. cp .env.example .env');
    console.error('  2. Run `caw onboard` and fill AGENT_WALLET_API_KEY + AGENT_WALLET_WALLET_ID');
    console.error('  3. Set STUB_SERVER_ADDRESS to your funded Base Sepolia address');
    console.error('  4. Start the stub server: npm run stub');
  }

  process.exit(1);
});
