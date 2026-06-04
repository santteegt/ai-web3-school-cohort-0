/**
 * P-003 + P-004 — Agent Consumer Loop + Payment Execution
 *
 * Runs one full x402 payment cycle:
 *   1. Call /api/inference — expect 402
 *   2. Extract PAYMENT-REQUIRED header (base64 JSON challenge)
 *   3. Check Pact constraints (fail fast before calling CAW)
 *   4. POST to CAW /payment — CAW signs, returns retry_headers
 *   5. Retry /api/inference with PAYMENT-SIGNATURE header — expect 200
 *   6. Append audit record
 *
 * The agent never signs transactions directly. CAW enforces all Pact limits
 * server-side; we do a client-side pre-check for a clear error message.
 */

import axios, { isAxiosError } from 'axios';
import { appendAuditRecord } from './auditLog.js';
import { type PactConfig } from './pactConfig.js';
import { config } from './config.js';
import { Configuration, TransactionsApi } from '@cobo/agentic-wallet';

export interface InferenceResponse {
  result: string;
  model: string;
  timestamp: number;
  paymentVerified: boolean;
}

export interface LoopResult {
  response: InferenceResponse;
  txHash: string | null;
  amountPaidUsd: string;
}

// ── Main loop ─────────────────────────────────────────────────────────────────

export async function runPaymentLoop(
  pact: PactConfig,
  callIndex: number,
): Promise<LoopResult> {
  const endpoint = `http://localhost:${config.stub.port}/api/inference`;

  // ── Client-side Pact pre-check ─────────────────────────────────────────────
  if (Date.now() > pact.expiresAt) {
    throw new Error(
      `Pact ${pact.pactId} expired at ${new Date(pact.expiresAt).toISOString()}. ` +
        'Delete pact-config.json and run again.',
    );
  }

  console.log(`\n[loop:${callIndex}] → GET ${endpoint}`);

  // ── Step 1: initial request ────────────────────────────────────────────────
  let paymentRequired: string;

  try {
    // If somehow we get 200 (stub not protecting route), warn and return
    const initial = await axios.get<InferenceResponse>(endpoint);
    console.warn('[loop] WARNING: Got 200 without payment — stub may be misconfigured');
    return { response: initial.data, txHash: null, amountPaidUsd: '0' };
  } catch (err) {
    if (!isAxiosError(err) || err.response?.status !== 402) throw err;

    // Extract PAYMENT-REQUIRED header (base64 JSON)
    const pr =
      (err.response.headers as Record<string, string>)['payment-required'] ??
      (err.response.headers as Record<string, string>)['PAYMENT-REQUIRED'];

    if (!pr) {
      // Log the actual headers for debugging
      console.error('[loop] 402 headers received:', Object.keys(err.response.headers));
      throw new Error(
        'Got 402 but PAYMENT-REQUIRED header is missing. ' +
          'Check that @x402/express is wired up correctly on the stub server.',
      );
    }

    paymentRequired = pr;
    console.log(`[loop:${callIndex}] ← 402 Payment Required`);
    console.log(`[loop:${callIndex}]   PAYMENT-REQUIRED: ${paymentRequired.slice(0, 40)}…`);
  }

  // ── Step 2: call CAW to sign the payment ───────────────────────────────────
  console.log(`[loop:${callIndex}] → CAW /payment (protocol: x402)`);

  const requestId = `caw-x402-${callIndex}-${Date.now()}`;

  // ── Submit to CAW ──────────────────────────────────────────────────────────
  // Pact is active; switching to pact-scoped API key
  const ownerConfig = new Configuration({
    // apiKey: config.caw.apiKey,
    apiKey: pact.pactApiKey,
    basePath: config.caw.apiUrl,
  });
  const txApi = new TransactionsApi(ownerConfig);

  try {
    const decoded = JSON.parse(Buffer.from(paymentRequired, 'base64').toString('utf-8'));
    console.log(`[loop:${callIndex}]   paymentRequired (decoded):`, JSON.stringify(decoded, null, 2));
  } catch {
    console.warn(`[loop:${callIndex}]   paymentRequired could not be decoded as base64 JSON`);
  }

  let paymentResp: Awaited<ReturnType<typeof txApi.payment>>;
  try {
    paymentResp = await txApi.payment(config.caw.walletId, {
      x402_payment_required: paymentRequired,
      protocol: 'x402',
      request_id: requestId,
    });
  } catch (err) {
    if (isAxiosError(err) && err.response?.status === 422) {
      console.error(
        `[loop:${callIndex}] CAW 422 Validation Error:`,
        JSON.stringify(err.response.data, null, 2),
      );
    }
    throw err;
  }
  // const paymentResp = await axios.post<{
  //   success: boolean;
  //   result: {
  //     status: string;
  //     retry_headers: Record<string, string>;
  //     tx_hash: string | null;
  //     idempotent?: boolean;
  //   };
  // }>(
  //   `${config.caw.apiUrl}/api/v1/wallets/${pact.walletId}/payment`,
  //   {
  //     protocol: 'x402',
  //     x402_payment_required: paymentRequired,
  //     request_id: requestId,
  //   },
  //   {
  //     headers: {
  //       'X-API-Key': pact.pactApiKey,
  //       'Content-Type': 'application/json',
  //     },
  //   },
  // );

  const {
    id,
    idempotent,
    status,
    retry_headers,
    tx_hash
  } = paymentResp.data.result;

  if (status !== 'completed' && status !== 'submitted') {
    throw new Error(
      `CAW payment returned unexpected status: "${status}". ` +
        'Expected "completed" or "submitted".',
    );
  }

  const txHash = tx_hash ?? null;
  console.log(`[loop:${callIndex}] ← x402 Request - id: ${id} (requestId: ${requestId}; idempotent: ${idempotent})`);
  console.log(`[loop:${callIndex}] ← CAW payment ${status}`);
  console.log(`[loop:${callIndex}]   tx_hash: ${txHash ?? '(pending)'}`);
  console.log(`[loop:${callIndex}]   retry_headers: ${JSON.stringify(Object.keys(retry_headers || {}))}`);

  // ── Step 3: retry with payment proof ──────────────────────────────────────
  console.log(`[loop:${callIndex}] → GET ${endpoint} (with payment proof)`);

  const paid = await axios.get<InferenceResponse>(endpoint, {
    headers: retry_headers, // contains PAYMENT-SIGNATURE
  });

  console.log(`[loop:${callIndex}] ← 200 OK`);
  console.log(`[loop:${callIndex}]   result: "${paid.data.result}"`);
  console.log(`[loop:${callIndex}]   model:  ${paid.data.model}`);

  // ── Step 4: write audit record ─────────────────────────────────────────────
  appendAuditRecord({
    pactId: pact.pactId,
    endpoint,
    amountPaidUsd: config.stub.pricePerCallUsd,
    txHash,
    receiverAddress: pact.receiverAddress,
    responseStatus: 200,
    resultSnippet: paid.data.result.slice(0, 100),
  });

  return {
    response: paid.data,
    txHash,
    amountPaidUsd: config.stub.pricePerCallUsd,
  };
}
