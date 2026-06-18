/**
 * Step 4 — CLIENT approves work (@a2a-js/sdk client)
 *
 * 1. Recompute keccak256 of the delivered content
 * 2. Fetch EAS attestation by UID on-chain and assert hash match
 * 3. Send A2A "accepted" message back to DEV (same contextId)
 * 4. Return DEV's review request (Step 5 — arrives as a direct Message reply)
 */

import { ethers } from 'ethers';
import { v4 as uuidv4 } from 'uuid';
import { ClientFactory } from '@a2a-js/sdk/client';
import type { Message, MessageSendParams, TextPart } from '@a2a-js/sdk';
import { DEV_SERVER_URL, CLIENT_ADDRESS, log } from './config.js';
import { verifyAttestation } from './attest-eas.js';
import type { DeliverableData } from './coordinate-a2a.js';

export async function approveDeliverable(
  artifactData: DeliverableData,
  deliverableContent: string,
  contextId: string,
): Promise<{ reviewRequestMessage: string }> {
  log('STEP 4', '=== CLIENT approving deliverable ===');

  const { deliverable_hash, eas_attestation_uid } = artifactData;

  // Recompute hash of received content and compare to attested hash
  const recomputedHash = ethers.keccak256(ethers.toUtf8Bytes(deliverableContent));
  log('STEP 4', `Recomputed hash:  ${recomputedHash}`);
  log('STEP 4', `Artifact hash:    ${deliverable_hash}`);

  if (recomputedHash.toLowerCase() !== deliverable_hash.toLowerCase()) {
    throw new Error(`REJECT: hash mismatch! got=${recomputedHash} expected=${deliverable_hash}`);
  }
  log('STEP 4', `Local hash check: ✅ MATCH`);

  // Fetch and verify EAS attestation on-chain
  await verifyAttestation(eas_attestation_uid, deliverable_hash);

  // Send A2A "accepted" in the same context (Step 4 → Step 5 handoff)
  log('STEP 4', `Sending A2A "accepted" message to DEV server...`);
  const factory = new ClientFactory();
  const client = await factory.createFromUrl(DEV_SERVER_URL);

  const acceptParams: MessageSendParams = {
    message: {
      kind: 'message',
      messageId: uuidv4(),
      role: 'user',
      contextId,
      parts: [{ kind: 'text', text: 'Accepted' }],
      metadata: {
        status: 'accepted',
        verified_hash: deliverable_hash,
        eas_attestation_uid,
        client_address: CLIENT_ADDRESS,
      },
    },
  };

  const result = await client.sendMessage(acceptParams);

  // DEV replies with a direct Message (review request)
  if (result.kind !== 'message') {
    throw new Error(`Expected message reply from DEV, got: ${result.kind}`);
  }

  const replyMsg = result as Message;
  const reviewRequestMessage = replyMsg.parts
    .filter((p): p is TextPart => p.kind === 'text')
    .map((p) => p.text)
    .join('');

  log('STEP 4', `✅ Acceptance sent. DEV replied:`);
  log('STEP 5', `DEV review request: "${reviewRequestMessage}"`);

  return { reviewRequestMessage };
}
