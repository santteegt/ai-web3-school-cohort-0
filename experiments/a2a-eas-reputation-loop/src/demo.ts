/**
 * demo.ts — Full 6-Step A2A × EAS × ERC-8004 Reputation Loop
 *
 * Run: pnpm demo
 *
 * Step 1: Register CLIENT + DEV on ERC-8004 IdentityRegistry
 * Step 2: CLIENT delegates task to DEV via A2A (resolves AgentCard, sends message/send)
 * Step 3: DEV generates hello_world.py, attests hash via EAS, returns artifact with UID embedded
 * Step 4: CLIENT verifies EAS attestation, sends A2A "accepted"
 * Step 5: DEV sends review request via A2A (embedded in acceptance reply)
 * Step 6: CLIENT calls ERC-8004 giveFeedback; proves reputation 0 → 1
 */

import { appendFileSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { CLIENT_ADDRESS, DEV_ADDRESS, DEV_PORT, log } from './config.js';
import { loadState } from './state.js';
import { startDevServer } from './dev-server.js';
import { registerIdentities } from './identity.js';
import { delegateTask } from './coordinate-a2a.js';
import { approveDeliverable } from './approve.js';
import { giveFeedback } from './feedback.js';

const __dirname = dirname(fileURLToPath(import.meta.url));
const RUN_LOG = resolve(__dirname, '../RUN_LOG.md');

function appendLog(text: string): void {
  appendFileSync(RUN_LOG, text + '\n', 'utf8');
}

async function waitForServer(url: string, maxWaitMs = 15000): Promise<void> {
  const start = Date.now();
  while (Date.now() - start < maxWaitMs) {
    try {
      const resp = await fetch(url);
      if (resp.ok) return;
    } catch { /* not ready yet */ }
    await new Promise((r) => setTimeout(r, 300));
  }
  throw new Error(`Server did not become ready at ${url} within ${maxWaitMs}ms`);
}

async function main(): Promise<void> {
  console.log('\n' + '═'.repeat(70));
  console.log('  A2A × EAS × ERC-8004 Reputation Loop — Base Sepolia PoC');
  console.log('═'.repeat(70));
  console.log(`  CLIENT address: ${CLIENT_ADDRESS}`);
  console.log(`  DEV    address: ${DEV_ADDRESS}`);
  console.log(`  Network: Base Sepolia (chain_id 84532)`);
  console.log('═'.repeat(70) + '\n');

  const runDate = new Date().toISOString();
  appendLog(`\n## Run ${runDate}\n`);
  appendLog(`- CLIENT address: \`${CLIENT_ADDRESS}\``);
  appendLog(`- DEV address: \`${DEV_ADDRESS}\``);

  // ─── Start DEV A2A server (inline in same process) ───────────────────────
  log('DEMO', `Starting DEV A2A server on port ${DEV_PORT}...`);
  const server = await startDevServer();
  await waitForServer(`http://localhost:${DEV_PORT}/.well-known/agent-card.json`);
  log('DEMO', 'DEV A2A server ready.');

  try {
    // ─── Step 1: Register identities ────────────────────────────────────────
    const { clientAgentId, devAgentId, clientRegTxHash, devRegTxHash } =
      await registerIdentities();

    appendLog(`\n### Step 1 — Register Identities`);
    appendLog(`- CLIENT agentId: \`${clientAgentId}\``);
    appendLog(`- CLIENT tx: https://sepolia.basescan.org/tx/${clientRegTxHash}`);
    appendLog(`- DEV agentId: \`${devAgentId}\``);
    appendLog(`- DEV tx: https://sepolia.basescan.org/tx/${devRegTxHash}`);

    // ─── Steps 2+3: Coordinate via A2A + EAS attestation ────────────────────
    const { task, taskId, contextId, artifactData, deliverableContent } =
      await delegateTask(clientAgentId, devAgentId);

    if (task.status.state !== 'completed' || !task.artifacts?.length) {
      throw new Error(`Task did not complete with artifacts. Status: ${task.status.state}`);
    }

    appendLog(`\n### Step 2 — A2A Task Delegation`);
    appendLog(`- A2A task ID: \`${taskId}\``);
    appendLog(`- A2A context ID: \`${contextId}\``);

    const state = loadState();
    appendLog(`\n### Step 3 — EAS Attestation`);
    appendLog(`- EAS schema UID: \`${state.easSchemaUID}\``);
    appendLog(`- EAS schema: https://base-sepolia.easscan.org/schema/view/${state.easSchemaUID}`);
    appendLog(`- Deliverable hash: \`${artifactData.deliverable_hash}\``);
    appendLog(`- EAS attestation UID: \`${artifactData.eas_attestation_uid}\``);
    appendLog(`- easscan: https://base-sepolia.easscan.org/attestation/view/${artifactData.eas_attestation_uid}`);
    if (state.easAttestTxHash) {
      appendLog(`- Attest tx: https://sepolia.basescan.org/tx/${state.easAttestTxHash}`);
    }

    // ─── Step 4: CLIENT approves + Step 5: DEV review request ───────────────
    const { reviewRequestMessage } = await approveDeliverable(
      artifactData,
      deliverableContent,
      contextId,
    );

    appendLog(`\n### Step 4 — CLIENT Approval`);
    appendLog(`- EAS attestation verified on-chain ✅`);
    appendLog(`- Hash match confirmed ✅`);
    appendLog(`- A2A "accepted" message sent`);
    appendLog(`\n### Step 5 — DEV Review Request`);
    appendLog(`- DEV sent review request via A2A: "${reviewRequestMessage.slice(0, 120)}..."`);

    // ─── Step 6: CLIENT gives reputation feedback ────────────────────────────
    const feedbackResult = await giveFeedback(
      devAgentId,
      taskId,
      artifactData.deliverable_hash,
      artifactData.eas_attestation_uid,
    );

    appendLog(`\n### Step 6 — ERC-8004 Reputation Feedback`);
    appendLog(`- giveFeedback tx: https://sepolia.basescan.org/tx/${feedbackResult.txHash}`);
    appendLog(`- getSummary BEFORE: count=${feedbackResult.beforeCount} value=${feedbackResult.beforeSummaryValue}`);
    appendLog(`- getSummary AFTER:  count=${feedbackResult.afterCount}  value=${feedbackResult.afterSummaryValue}`);
    appendLog(`- Reputation delta: ${feedbackResult.beforeCount} → ${feedbackResult.afterCount} ✅`);

    // ─── Summary ─────────────────────────────────────────────────────────────
    console.log('\n' + '═'.repeat(70));
    console.log('  ✅ DEMO COMPLETE — All 6 Steps Succeeded');
    console.log('═'.repeat(70));
    console.log(`  CLIENT agentId:      ${clientAgentId}`);
    console.log(`  DEV agentId:         ${devAgentId}`);
    console.log(`  EAS schema UID:      ${state.easSchemaUID}`);
    console.log(`  EAS attestation UID: ${artifactData.eas_attestation_uid}`);
    console.log(`  giveFeedback tx:     ${feedbackResult.txHash}`);
    console.log(`  Reputation count:    ${feedbackResult.beforeCount} → ${feedbackResult.afterCount}`);
    console.log('─'.repeat(70));
    console.log(`  basescan (CLIENT):   https://sepolia.basescan.org/tx/${clientRegTxHash}`);
    console.log(`  basescan (DEV):      https://sepolia.basescan.org/tx/${devRegTxHash}`);
    console.log(`  easscan (attest):    https://base-sepolia.easscan.org/attestation/view/${artifactData.eas_attestation_uid}`);
    console.log(`  basescan (feedback): https://sepolia.basescan.org/tx/${feedbackResult.txHash}`);
    console.log('═'.repeat(70) + '\n');

    appendLog(`\n### ✅ Demo Complete`);
    appendLog(`| Item | Value |`);
    appendLog(`|------|-------|`);
    appendLog(`| CLIENT agentId | \`${clientAgentId}\` |`);
    appendLog(`| DEV agentId | \`${devAgentId}\` |`);
    appendLog(`| EAS schema UID | \`${state.easSchemaUID}\` |`);
    appendLog(`| EAS attestation UID | \`${artifactData.eas_attestation_uid}\` |`);
    appendLog(`| giveFeedback tx | \`${feedbackResult.txHash}\` |`);
    appendLog(`| Reputation count | ${feedbackResult.beforeCount} → ${feedbackResult.afterCount} |`);

  } finally {
    server.close();
    log('DEMO', 'DEV A2A server stopped.');
  }
}

main().catch((err) => {
  console.error('\n❌ Demo failed:', err.message ?? err);
  process.exit(1);
});
