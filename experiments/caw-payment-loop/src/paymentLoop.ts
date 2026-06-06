/**
 * P-003 + P-004 — Agent Consumer Loop + Payment Execution
 *
 * Runs one full x402 payment cycle:
 *   1. Call /api/inference — expect 402
 *   2. Extract PAYMENT-REQUIRED header (base64 JSON challenge)
 *   3. Check Pact constraints (fail fast before calling CAW)
 *   4. Sign EIP-712 (EIP-3009) via CAW message-sign API → build PAYMENT-SIGNATURE
 *   5. Retry /api/inference with PAYMENT-SIGNATURE header — expect 200
 *   6. Append audit record
 *
 * NOTE (2026-06-06): Step 4 normally uses txApi.payment() but is temporarily
 * replaced by txApi.messageSign() due to a Cobo Base Sepolia node indexing
 * issue. See the comment block in step 2 below for details.
 */

import crypto from 'crypto';
import axios, { isAxiosError } from 'axios';
import { appendAuditRecord } from './auditLog.js';
import { type PactConfig } from './pactConfig.js';
import { config } from './config.js';
import { Configuration, TransactionsApi, TransactionRecordsApi } from '@cobo/agentic-wallet';
import { localSignEip3009, localSignerAddress } from './localSigner.js';

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

// Shape of one entry in the PAYMENT-REQUIRED accepts array
interface PaymentAccept {
  scheme: string;
  network: string;
  amount: string;
  asset: string;
  payTo: string;
  maxTimeoutSeconds: number;
  extra: { name: string; version: string };
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
    const initial = await axios.get<InferenceResponse>(endpoint);
    console.warn('[loop] WARNING: Got 200 without payment — stub may be misconfigured');
    return { response: initial.data, txHash: null, amountPaidUsd: '0' };
  } catch (err) {
    if (!isAxiosError(err) || err.response?.status !== 402) throw err;

    const pr =
      (err.response.headers as Record<string, string>)['payment-required'] ??
      (err.response.headers as Record<string, string>)['PAYMENT-REQUIRED'];

    if (!pr) {
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

  // ── Step 2: sign payment ───────────────────────────────────────────────────
  //
  // WORKAROUND ACTIVE (2026-06-06): Cobo's Base/Base Sepolia indexing nodes are
  // down. Their internal balance cache shows TBASE_USDC available=0 even though
  // the wallet holds on-chain USDC, causing txApi.payment() to return:
  //   X402_INSUFFICIENT_BALANCE / available: "0"
  //
  // Cobo team suggestion: use POST /wallets/{id}/message-sign to sign the raw
  // EIP-712 (EIP-3009 TransferWithAuthorization) typed data directly, then build
  // the PAYMENT-SIGNATURE header manually — bypassing the balance check.
  //
  // TO RESTORE the normal flow once Cobo confirms nodes are recovered:
  //   1. Delete everything from "WORKAROUND START" to "WORKAROUND END" below.
  //   2. Uncomment the txApi.payment() block further below.
  //
  // ── WORKAROUND START ──────────────────────────────────────────────────────

  const requestId = `caw-x402-${callIndex}-${Date.now()}`;

  // Debug: show decoded payment requirements
  try {
    const decoded = JSON.parse(Buffer.from(paymentRequired, 'base64').toString('utf-8'));
    console.log(`[loop:${callIndex}]   paymentRequired (decoded):`, JSON.stringify(decoded, null, 2));
  } catch {
    console.warn(`[loop:${callIndex}]   paymentRequired could not be decoded as base64 JSON`);
  }

  const paymentReq = JSON.parse(Buffer.from(paymentRequired, 'base64').toString('utf-8')) as {
    x402Version: number;
    accepts: PaymentAccept[];
  };
  const accept = paymentReq.accepts[0];
  if (!accept) throw new Error('[loop] No accepts entry in PAYMENT-REQUIRED payload');

  // ── Building EIP-712 TransferWithAuthorization typed message for signing

  // EIP-3009 validity window: 10-min past grace + maxTimeoutSeconds future
  const now = Math.floor(Date.now() / 1000);
  const validAfter = (now - 600).toString();
  const validBefore = (now + accept.maxTimeoutSeconds).toString();
  // 32-byte random nonce as bytes32 hex string
  const nonce = '0x' + crypto.randomBytes(32).toString('hex');
  // Parse numeric chain ID from CAIP-2 network string "eip155:<chainId>"
  const chainId = parseInt(accept.network.split(':')[1]!, 10);

  // EIP-712 typed data for USDC TransferWithAuthorization (EIP-3009)
  const eip712TypedData = {
    domain: {
      name: accept.extra.name,         // "USDC"
      version: accept.extra.version,   // "2"
      chainId,                         // 84532 (Base Sepolia)
      verifyingContract: accept.asset, // USDC contract address
    },
    types: {
      TransferWithAuthorization: [
        { name: 'from', type: 'address' },
        { name: 'to', type: 'address' },
        { name: 'value', type: 'uint256' },
        { name: 'validAfter', type: 'uint256' },
        { name: 'validBefore', type: 'uint256' },
        { name: 'nonce', type: 'bytes32' },
      ],
    },
    primaryType: 'TransferWithAuthorization',
    message: {
      from: config.caw.walletAddress,
      to: accept.payTo,
      value: accept.amount,   // decimal string, e.g. "1000" (6-decimal USDC units)
      validAfter,
      validBefore,
      nonce,
    },
  };

  // ── Signature acquisition — local bypass or CAW messageSign ─────────────────
  // `fromAddress` is the EIP-3009 `from` — derived from the local key when
  // bypassing CAW, otherwise the Cobo MPC wallet address.
  const fromAddress: `0x${string}` = config.localSigner.enabled
    ? localSignerAddress(config.localSigner.privateKey)
    : config.caw.walletAddress;

  let signature: string;

  if (config.localSigner.enabled) {
    // ── LOCAL SIGNER (dev/test, USE_LOCAL_SIGNER=true) ────────────────────────
    // Signs locally with LOCAL_SIGNER_PRIVATE_KEY via viem — no CAW round-trip.
    // The signing key must own the wallet address used as the `from` field.
    console.log(`[loop:${callIndex}] → local EIP-712 sign (USE_LOCAL_SIGNER=true, from: ${fromAddress})`);
    signature = await localSignEip3009({
      privateKey: config.localSigner.privateKey,
      domain: {
        name: accept.extra.name,
        version: accept.extra.version,
        chainId,
        verifyingContract: accept.asset as `0x${string}`,
      },
      message: {
        from: fromAddress,
        to: accept.payTo as `0x${string}`,
        value: accept.amount,
        validAfter,
        validBefore,
        nonce: nonce as `0x${string}`,
      },
    });
    console.log(`[loop:${callIndex}] ← locally signed: ${signature.slice(0, 20)}…`);
  } else {
    // ── CAW MESSAGESIGN (production path, disabled while Cobo MPC is broken) ──
    // Use pact-scoped key: Cobo enforces pact permissions on messageSign too.
    const signerCfg = new Configuration({
      apiKey: pact.pactApiKey,
      basePath: config.caw.apiUrl,
    });
    const signerApi = new TransactionsApi(signerCfg);

    console.log(`[loop:${callIndex}] → CAW /message-sign`);

    // Submit with sync=false — CAW returns immediately; we poll live status via
    // TransactionRecordsApi (idempotent replays return cached snapshot, not current state).
    let submitResp: Awaited<ReturnType<typeof signerApi.messageSign>>;
    try {
      submitResp = await signerApi.messageSign(config.caw.walletId, {
        chain_id: config.caw.chainId,
        destination_type: 'eip712',
        eip712_typed_data: eip712TypedData,
        source_address: config.caw.walletAddress,
        request_id: requestId,
        sync: false,
      });
    } catch (err) {
      if (isAxiosError(err) && err.response) {
        console.error(
          `[loop:${callIndex}] CAW messageSign ${err.response.status} error:`,
          JSON.stringify(err.response.data, null, 2),
        );
      }
      throw err;
    }

    const submitResult = submitResp.data.result;
    console.log(
      `[loop:${callIndex}] ← submitted (id: ${submitResult.id ?? 'n/a'}; ` +
        `status: ${submitResult.status} ${submitResult.status_display ?? ''}` +
        (submitResult.idempotent ? '; idempotent' : '') + ')',
    );

    const recordsApi = new TransactionRecordsApi(signerCfg);
    const TERMINAL_FAIL = new Set([901, 902]);
    const POLL_INTERVAL_MS = 3_000;
    const POLL_TIMEOUT_MS = 60_000;
    const pollDeadline = Date.now() + POLL_TIMEOUT_MS;

    for (;;) {
      const record = (
        await recordsApi.getUserTransactionByRequestId(config.caw.walletId, requestId)
      ).data.result;

      const { status, status_display, sub_status, data: txData } = record;
      console.log(
        `[loop:${callIndex}] ← poll status ${status} (${status_display ?? '?'})` +
          (sub_status ? ` sub: ${sub_status}` : ''),
      );

      if (status === 900) {
        if (!txData.signature) throw new Error('Status 900 but data.signature is null.');
        signature = txData.signature;
        break;
      }

      if (status === 100) {
        throw new Error('CAW messageSign requires human approval (status 100 pending_approval).');
      }

      if (TERMINAL_FAIL.has(status)) {
        throw new Error(
          `CAW messageSign failed: status ${status} (${status_display ?? 'unknown'})` +
            (txData.failed_reason ? `, reason: ${txData.failed_reason}` : ''),
        );
      }

      if (Date.now() >= pollDeadline) {
        throw new Error(
          `CAW messageSign still status ${status} after ${POLL_TIMEOUT_MS / 1000}s. ` +
            (txData.failed_reason ? `reason: ${txData.failed_reason}` : 'Giving up.'),
        );
      }

      await new Promise(r => setTimeout(r, POLL_INTERVAL_MS));
    }

    console.log(`[loop:${callIndex}] ← CAW EIP-712 signed (id: ${submitResult.id})`);
    console.log(`[loop:${callIndex}]   signature: ${signature.slice(0, 20)}…`);
  }

  // Build x402 PaymentPayload → base64 PAYMENT-SIGNATURE header.
  // This mirrors the structure txApi.payment() returns in retry_headers["PAYMENT-SIGNATURE"].
  const eip3009Payload = {
    signature,
    authorization: {
      from: fromAddress,
      to: accept.payTo,
      value: accept.amount,
      validAfter,
      validBefore,
      nonce,
    },
  };
  // x402 v2 PAYMENT-SIGNATURE format: accepted = full payment requirements object
  // (not top-level scheme/network — those live inside accepted).
  const paymentPayload = {
    x402Version: 2,
    accepted: accept,
    payload: eip3009Payload,
  };
  const retry_headers: Record<string, string> = {
    'PAYMENT-SIGNATURE': Buffer.from(JSON.stringify(paymentPayload), 'utf-8').toString('base64'),
  };
  const txHash = null; // no on-chain tx hash in message-sign flow

  // ── WORKAROUND END ────────────────────────────────────────────────────────
  //
  // ── NORMAL FLOW (disabled while Cobo nodes are down) ─────────────────────
  //
  // const ownerConfig = new Configuration({
  //   apiKey: pact.pactApiKey,
  //   basePath: config.caw.apiUrl,
  // });
  // const txApi = new TransactionsApi(ownerConfig);
  //
  // let paymentResp: Awaited<ReturnType<typeof txApi.payment>>;
  // try {
  //   paymentResp = await txApi.payment(config.caw.walletId, {
  //     x402_payment_required: paymentRequired,
  //     protocol: 'x402',
  //     request_id: requestId,
  //   });
  // } catch (err) {
  //   if (isAxiosError(err) && err.response?.status === 422) {
  //     console.error(
  //       `[loop:${callIndex}] CAW 422 Validation Error:`,
  //       JSON.stringify((err as import('axios').AxiosError).response?.data, null, 2),
  //     );
  //   }
  //   throw err;
  // }
  //
  // const { id, idempotent, status, retry_headers, tx_hash } = paymentResp.data.result;
  // if (status !== 'completed' && status !== 'submitted') {
  //   throw new Error(
  //     `CAW payment returned unexpected status: "${status}". ` +
  //       'Expected "completed" or "submitted".',
  //   );
  // }
  // const txHash = tx_hash ?? null;
  // console.log(`[loop:${callIndex}] ← x402 Request - id: ${id} (requestId: ${requestId}; idempotent: ${idempotent})`);
  // console.log(`[loop:${callIndex}] ← CAW payment ${status}`);
  // console.log(`[loop:${callIndex}]   tx_hash: ${txHash ?? '(pending)'}`);
  // console.log(`[loop:${callIndex}]   retry_headers: ${JSON.stringify(Object.keys(retry_headers || {}))}`);

  // Debug: show the full decoded PAYMENT-SIGNATURE so we can verify the payload
  try {
    const decoded = JSON.parse(
      Buffer.from(retry_headers['PAYMENT-SIGNATURE']!, 'base64').toString('utf-8'),
    );
    console.log(
      `[loop:${callIndex}]   PAYMENT-SIGNATURE (decoded):`,
      JSON.stringify(decoded, null, 2),
    );
  } catch {
    console.warn(`[loop:${callIndex}]   PAYMENT-SIGNATURE could not be decoded`);
  }

  // ── Step 3: retry with payment proof ──────────────────────────────────────
  console.log(`[loop:${callIndex}] → GET ${endpoint} (with payment proof)`);

  let paid: Awaited<ReturnType<typeof axios.get<InferenceResponse>>>;
  try {
    paid = await axios.get<InferenceResponse>(endpoint, { headers: retry_headers });
  } catch (err) {
    if (isAxiosError(err) && err.response?.status === 402) {
      console.error(
        `[loop:${callIndex}] ← 402 on retry (facilitator rejected payment proof)`,
      );
      const respHeaders = err.response.headers as Record<string, string>;
      const pr2 = respHeaders['payment-required'] ?? respHeaders['PAYMENT-REQUIRED'];
      if (pr2) {
        try {
          console.error(
            `[loop:${callIndex}]   PAYMENT-REQUIRED (rejection details):`,
            JSON.stringify(JSON.parse(Buffer.from(pr2, 'base64').toString('utf-8')), null, 2),
          );
        } catch {
          console.error(`[loop:${callIndex}]   PAYMENT-REQUIRED raw: ${pr2}`);
        }
      }
      console.error(`[loop:${callIndex}]   response body:`, JSON.stringify(err.response.data));
    }
    throw err;
  }

  // Extract settlement tx hash from PAYMENT-RESPONSE header (base64 JSON settle result).
  // Field: { success, transaction, network, payer, amount, ... }
  const paymentResponseHeader =
    (paid.headers as Record<string, string>)['payment-response'] ??
    (paid.headers as Record<string, string>)['PAYMENT-RESPONSE'] ??
    null;
  let settleTxHash: string | null = txHash; // fall back to CAW tx_hash when available
  if (paymentResponseHeader) {
    try {
      const settleResult = JSON.parse(
        Buffer.from(paymentResponseHeader, 'base64').toString('utf-8'),
      ) as { success: boolean; transaction?: string };
      settleTxHash = settleResult.transaction ?? null;
    } catch {
      console.warn(`[loop:${callIndex}] Could not decode PAYMENT-RESPONSE header`);
    }
  }

  console.log(`[loop:${callIndex}] ← 200 OK`);
  console.log(`[loop:${callIndex}]   result: "${paid.data.result}"`);
  console.log(`[loop:${callIndex}]   model:  ${paid.data.model}`);
  console.log(`[loop:${callIndex}]   tx:     ${settleTxHash ?? '(not yet settled)'}`);

  // ── Step 4: write audit record ─────────────────────────────────────────────
  appendAuditRecord({
    pactId: pact.pactId,
    endpoint,
    amountPaidUsd: config.stub.pricePerCallUsd,
    txHash: settleTxHash,
    receiverAddress: pact.receiverAddress,
    responseStatus: 200,
    resultSnippet: paid.data.result.slice(0, 100),
  });

  return {
    response: paid.data,
    txHash: settleTxHash,
    amountPaidUsd: config.stub.pricePerCallUsd,
  };
}
