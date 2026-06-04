/**
 * P-002 — CAW Pact Authorization
 *
 * Two exports:
 *   requestAndSubmitPact() — CLI prompt → human approves → submits Pact → polls until active
 *   loadActivePact()       — reads pact-config.json, throws if missing or expired
 *
 * The approved Pact issues a pact-scoped API key. All subsequent TransactionsApi
 * calls must use that key — not the owner key.
 */

import readline from 'node:readline/promises';
import { stdin as input, stdout as output } from 'node:process';
import { writeFileSync, existsSync, readFileSync } from 'node:fs';
import {
  Configuration,
  PactsApi,
  PactSubmitRequest,
  type PactSpecInput,
} from '@cobo/agentic-wallet';
import { config } from './config.js';

const PACT_CONFIG_PATH = './pact-config.json';

export interface PactConfig {
  pactId: string;
  /** Pact-scoped API key — use this for all payment transactions */
  pactApiKey: string;
  walletId: string;
  /** USD ceiling per single payment call */
  perCallCeilingUsd: string;
  /** USD total session budget */
  sessionBudgetUsd: string;
  /** Unix ms timestamp — pact is expired after this */
  expiresAt: number;
  receiverAddress: string;
}

// ── Load ─────────────────────────────────────────────────────────────────────

export function loadActivePact(): PactConfig {
  if (!existsSync(PACT_CONFIG_PATH)) {
    throw new Error(
      `No ${PACT_CONFIG_PATH} found. Run the authorization step first (index.ts will do this).`,
    );
  }

  const pact = JSON.parse(readFileSync(PACT_CONFIG_PATH, 'utf8')) as PactConfig;

  if (Date.now() > pact.expiresAt) {
    throw new Error(
      `Pact ${pact.pactId} expired at ${new Date(pact.expiresAt).toISOString()}. ` +
        `Delete ${PACT_CONFIG_PATH} and run again to authorize a new pact.`,
    );
  }

  return pact;
}

// ── Submit ────────────────────────────────────────────────────────────────────

export async function requestAndSubmitPact(): Promise<PactConfig> {
  const {
    receiverAddress,
    perCallCeilingUsd,
    sessionBudgetUsd,
    windowSeconds,
  } = {
    receiverAddress: config.stub.receiverAddress,
    perCallCeilingUsd: config.pact.perCallCeilingUsd,
    sessionBudgetUsd: config.pact.sessionBudgetUsd,
    windowSeconds: config.pact.windowSeconds,
  };

  const expiresAt = Date.now() + windowSeconds * 1_000;
  const expiresIso = new Date(expiresAt).toISOString();

  // ── Human approval prompt ──────────────────────────────────────────────────
  console.log('\n╔═══════════════════════════════════════════╗');
  console.log('║      CAW Pact Authorization Request       ║');
  console.log('╚═══════════════════════════════════════════╝');
  console.log(`  Endpoint:          http://localhost:${config.stub.port}/api/inference`);
  console.log(`  Receiver address:  ${receiverAddress}`);
  console.log(`  Per-call ceiling:  $${perCallCeilingUsd} USD`);
  console.log(`  Session budget:    $${sessionBudgetUsd} USD`);
  console.log(`  Time window:       ${windowSeconds}s (expires ${expiresIso})`);
  console.log(`  Chain:             ${config.caw.chainId} (Base Sepolia)`);
  console.log(`  Network:           eip155:84532`);
  console.log('═══════════════════════════════════════════');

  const rl = readline.createInterface({ input, output });
  const answer = await rl.question('\nApprove this authorization? [y/N]: ');
  rl.close();

  if (answer.trim().toLowerCase() !== 'y') {
    throw new Error('Authorization rejected by operator. Exiting.');
  }

  // ── Build PactSpec ─────────────────────────────────────────────────────────
  // USD-denominated limits: works regardless of whether x402 settles in USDC or ETH
  const pactSpec: PactSpecInput = {
    policies: [
      {
        name: 'x402-inference-payment',
        type: 'transfer',
        rules: {
          effect: 'allow',
          when: {
            chain_in: [config.caw.chainId],
            destination_address_in: [
              { chain_id: config.caw.chainId, address: receiverAddress },
            ],
          },
          deny_if: {
            amount_usd_gt: perCallCeilingUsd,
            usage_limits: {
              rolling_24h: { amount_usd_gt: sessionBudgetUsd },
            },
          },
        },
      },
    ],
    completion_conditions: [
      { type: 'time_elapsed', threshold: String(windowSeconds) },
    ],
  };

  // ── Submit to CAW ──────────────────────────────────────────────────────────
  const ownerConfig = new Configuration({
    apiKey: config.caw.apiKey,
    basePath: config.caw.apiUrl,
  });
  const pactsApi = new PactsApi(ownerConfig);

  const pactSubmitRequest: PactSubmitRequest = {
    wallet_id: config.caw.walletId,
    intent:
      `Pay for x402-protected AI inference at localhost:${config.stub.port}/api/inference. ` +
      `Budget: $${sessionBudgetUsd} USD / session. Per-call cap: $${perCallCeilingUsd} USD.`,
    spec: pactSpec,
  };

  console.log('\n[pact] Submitting pact to Cobo...');
  console.log(`\n[pact] ${JSON.stringify(pactSubmitRequest)}`);

  const resp = await pactsApi.submitPact(pactSubmitRequest);

  const pactId = resp.data.result.pact_id;
  console.log(`[pact] Submitted: id=${pactId} — status=pending_approval`);
  console.log('[pact] Open the Cobo Agentic Wallet app on your phone and approve the pact...');

  // ── Poll until active ──────────────────────────────────────────────────────
  const pactApiKey = await waitForActivation(pactsApi, pactId);

  const pactConfig: PactConfig = {
    pactId,
    pactApiKey,
    walletId: config.caw.walletId,
    perCallCeilingUsd,
    sessionBudgetUsd,
    expiresAt,
    receiverAddress,
  };

  writeFileSync(PACT_CONFIG_PATH, JSON.stringify(pactConfig, null, 2));

  console.log(`\n[pact] ✓ Active. Config saved to ${PACT_CONFIG_PATH}`);
  console.log(`  Pact ID:       ${pactId}`);
  console.log(`  Per-call cap:  $${perCallCeilingUsd} USD`);
  console.log(`  Session budget: $${sessionBudgetUsd} USD`);
  console.log(`  Expires:       ${expiresIso}`);

  return pactConfig;
}

// ── Helpers ───────────────────────────────────────────────────────────────────

async function waitForActivation(pactsApi: PactsApi, pactId: string): Promise<string> {
  const terminal = new Set(['rejected', 'expired', 'revoked', 'completed']);
  let lastStatus = '';

  for (;;) {
    const pact = (await pactsApi.getPact(pactId)).data.result;
    const status = pact.status ?? '';

    if (status !== lastStatus) {
      process.stdout.write(`\r[pact] status → ${status}                    `);
      lastStatus = status;
    }

    if (status === 'active' && pact.api_key) {
      console.log(); // newline after the status line
      return pact.api_key;
    }

    if (terminal.has(status)) {
      throw new Error(`Pact reached terminal status before activation: ${status}`);
    }

    await new Promise(r => setTimeout(r, 5_000));
  }
}
