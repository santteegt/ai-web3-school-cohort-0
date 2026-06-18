/**
 * Steps 5-6 — Client provides ERC-8004 reputation feedback
 *
 * Step 5: DEV sent a review request (handled in approve.ts / dev-server.ts)
 * Step 6: CLIENT calls ReputationRegistry.giveFeedback() with:
 *   - devAgentId
 *   - value=100, valueDecimals=0
 *   - tag1="code", tag2="accepted"
 *   - feedbackURI = data: URI containing JSON with a2aTaskId + deliverableHash + easUID
 *   - feedbackHash = keccak256(JSON bytes)
 *
 * Proof: getSummary(devAgentId, [clientAddress], "code", "") count 0 → 1
 *
 * CRITICAL: caller must be CLIENT (not DEV owner). CLIENT and DEV are different EOAs. ✅
 */

import { ethers } from 'ethers';
import {
  REPUTATION_REGISTRY,
  clientSigner,
  CLIENT_ADDRESS,
  log,
} from './config.js';
import { REPUTATION_REGISTRY_ABI } from './abis.js';
import { saveState } from './state.js';

interface FeedbackResult {
  txHash: string;
  beforeCount: bigint;
  afterCount: bigint;
  beforeSummaryValue: bigint;
  afterSummaryValue: bigint;
}

export async function giveFeedback(
  devAgentId: bigint,
  a2aTaskId: string,
  deliverableHash: string,
  easAttestationUID: string,
): Promise<FeedbackResult> {
  log('STEP 6', '=== CLIENT giving ERC-8004 reputation feedback to DEV ===');
  log('STEP 6', `DEV agentId: ${devAgentId}`);
  log('STEP 6', `CLIENT address (caller): ${CLIENT_ADDRESS}`);

  const repRegistry = new ethers.Contract(
    REPUTATION_REGISTRY,
    REPUTATION_REGISTRY_ABI,
    clientSigner,
  );

  // Read reputation BEFORE feedback using CLIENT_ADDRESS directly
  // (getSummary with a client that hasn't given feedback yet returns count=0)
  const beforeResult = await repRegistry.getSummary(devAgentId, [CLIENT_ADDRESS], 'code', '');
  const beforeCount = beforeResult[0] as bigint;
  const beforeSummaryValue = beforeResult[1] as bigint;
  log('STEP 6', `Before feedback → getSummary count=${beforeCount} summaryValue=${beforeSummaryValue}`);

  // Build feedback JSON (feedbackURI content)
  const feedbackJSON = JSON.stringify({
    agentRegistry: `eip155:84532:${REPUTATION_REGISTRY}`,
    agentId: devAgentId.toString(),
    clientAddress: CLIENT_ADDRESS,
    createdAt: new Date().toISOString(),
    value: 100,
    valueDecimals: 0,
    tag1: 'code',
    tag2: 'accepted',
    a2a: { taskId: a2aTaskId },
    deliverableHash,
    eas: { attestationUID: easAttestationUID },
  });

  const feedbackHash = ethers.keccak256(ethers.toUtf8Bytes(feedbackJSON)) as string;
  const b64 = Buffer.from(feedbackJSON).toString('base64');
  const feedbackURI = `data:application/json;base64,${b64}`;

  log('STEP 6', `feedbackURI hash (keccak256): ${feedbackHash}`);
  log('STEP 6', `DEV A2A endpoint: http://localhost:${process.env.DEV_PORT ?? '3001'}`);

  // Call giveFeedback — CLIENT is caller, DEV is subject (required: different EOAs)
  const tx = await (repRegistry.giveFeedback as (...args: unknown[]) => Promise<ethers.ContractTransactionResponse>)(
    devAgentId,
    100n,        // value (int128): 100 = "accepted"
    0,           // valueDecimals: 0
    'code',      // tag1: task type
    'accepted',  // tag2: outcome
    `http://localhost:${process.env.DEV_PORT ?? '3001'}`, // endpoint
    feedbackURI, // feedbackURI
    feedbackHash as `0x${string}`, // feedbackHash (bytes32)
  );

  log('STEP 6', `giveFeedback tx sent: https://sepolia.basescan.org/tx/${tx.hash}`);
  await tx.wait();
  log('STEP 6', `giveFeedback confirmed!`);

  // Poll getSummary until the public RPC reflects the new state (may lag after tx.wait())
  let afterCount = 0n;
  let afterSummaryValue = 0n;
  for (let attempt = 0; attempt < 10; attempt++) {
    await new Promise((r) => setTimeout(r, 1500));
    const afterResult = await repRegistry.getSummary(devAgentId, [CLIENT_ADDRESS], 'code', '');
    afterCount = afterResult[0] as bigint;
    afterSummaryValue = afterResult[1] as bigint;
    if (afterCount > beforeCount) break;
    log('STEP 6', `  RPC not yet synced (attempt ${attempt + 1}/10) — retrying...`);
  }

  log('STEP 6', `After feedback  → getSummary count=${afterCount} summaryValue=${afterSummaryValue}`);
  log('STEP 6', `✅ Reputation delta: count ${beforeCount} → ${afterCount}`);

  saveState({ feedbackTxHash: tx.hash });

  return {
    txHash: tx.hash,
    beforeCount: BigInt(beforeCount),
    afterCount: BigInt(afterCount),
    beforeSummaryValue: BigInt(beforeSummaryValue),
    afterSummaryValue: BigInt(afterSummaryValue),
  };
}
