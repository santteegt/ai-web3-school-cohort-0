/**
 * Step 3 — DEV attests deliverable hash via EAS
 *
 * Uses direct ethers.js contract calls (no EAS SDK) to avoid the EAS SDK's
 * lodash ESM compatibility issue with Node 24.
 *
 * ABIs sourced from @ethereum-attestation-service/eas-contracts (installed as transitive dep).
 *
 * Schema: "bytes32 deliverableHash, string taskType, string a2aTaskId, address devAgent"
 * The attestation UID is returned and embedded in the A2A delivery artifact for CLIENT to verify.
 */

import { ethers } from 'ethers';
import { EAS_ABI, EAS_SCHEMA_REGISTRY_ABI } from './abis';
import {
  EAS_CONTRACT,
  SCHEMA_REGISTRY,
  EAS_SCHEMA,
  EAS_SCHEMA_TYPES,
  provider,
  devSigner,
  DEV_ADDRESS,
  log,
} from './config.js';
import { loadState, saveState } from './state.js';


// ─── Deterministic schema UID (matches on-chain computation) ─────────────────

export function computeSchemaUID(schema: string, resolver: string, revocable: boolean): string {
  return ethers.keccak256(
    ethers.solidityPacked(['string', 'address', 'bool'], [schema, resolver, revocable]),
  );
}

// ─── Schema registration (idempotent) ────────────────────────────────────────

export async function getOrRegisterSchema(): Promise<string> {
  const state = loadState();
  if (state.easSchemaUID) {
    log('SCHEMA', `Reusing existing EAS schema UID: ${state.easSchemaUID}`);
    return state.easSchemaUID;
  }

  const expectedUID = computeSchemaUID(EAS_SCHEMA, ethers.ZeroAddress, true);
  log('SCHEMA', `Expected schema UID (deterministic): ${expectedUID}`);

  // Check if schema already exists on-chain
  const schemaRegistry = new ethers.Contract(SCHEMA_REGISTRY, EAS_SCHEMA_REGISTRY_ABI, provider);
  try {
    const existing = await (schemaRegistry.getSchema as (uid: string) => Promise<{ schema: string }>)(expectedUID);
    if (existing.schema === EAS_SCHEMA) {
      log('SCHEMA', `Schema already on-chain: ${expectedUID}`);
      saveState({ easSchemaUID: expectedUID });
      return expectedUID;
    }
  } catch {
    /* schema not registered yet */
  }

  log('SCHEMA', `Registering EAS schema: "${EAS_SCHEMA}"`);
  const registryWithSigner = schemaRegistry.connect(devSigner) as ethers.Contract;
  const tx = await (registryWithSigner.register as (
    schema: string, resolver: string, revocable: boolean
  ) => Promise<ethers.ContractTransactionResponse>)(EAS_SCHEMA, ethers.ZeroAddress, true);

  log('SCHEMA', `Schema tx sent: https://sepolia.basescan.org/tx/${tx.hash}`);
  const receipt = await tx.wait();
  if (!receipt) throw new Error('Schema registration tx receipt is null');

  // Parse Registered event to get the UID
  const iface = new ethers.Interface(EAS_SCHEMA_REGISTRY_ABI as ethers.InterfaceAbi);
  let schemaUID: string | undefined;
  for (const evLog of receipt.logs) {
    try {
      const parsed = iface.parseLog({ topics: [...evLog.topics], data: evLog.data });
      if (parsed?.name === 'Registered') {
        schemaUID = parsed.args.uid as string;
        break;
      }
    } catch { /* skip */ }
  }
  schemaUID ??= expectedUID;

  log('SCHEMA', `✅ EAS schema registered: ${schemaUID}`);
  saveState({ easSchemaUID: schemaUID, easSchemaTxHash: tx.hash });
  return schemaUID;
}

// ─── Attestation ─────────────────────────────────────────────────────────────

export interface AttestResult {
  schemaUID: string;
  attestationUID: string;
  txHash: string;
}

export async function attestDeliverable(
  deliverableHash: string,
  a2aTaskId: string,
  taskType: string = 'code_delivery'
): Promise<AttestResult> {
  log('STEP 3', '=== DEV attesting deliverable hash via EAS ===');
  log('STEP 3', `Deliverable hash: ${deliverableHash}`);
  log('STEP 3', `A2A task ID: ${a2aTaskId}`);

  const schemaUID = await getOrRegisterSchema();

  // ABI-encode attestation data (replaces SchemaEncoder.encodeData)
  const abiCoder = ethers.AbiCoder.defaultAbiCoder();
  const encodedData = abiCoder.encode(
    [...EAS_SCHEMA_TYPES],
    [deliverableHash, taskType, a2aTaskId, DEV_ADDRESS],
  );

  const easContract = new ethers.Contract(EAS_CONTRACT, EAS_ABI, devSigner);
  log('STEP 3', `Calling EAS.attest() from DEV signer ${DEV_ADDRESS} ...`);

  const tx = await (easContract.attest as (req: object) => Promise<ethers.ContractTransactionResponse>)({
    schema: schemaUID,
    data: {
      recipient: DEV_ADDRESS,
      expirationTime: 0n,
      revocable: true,
      refUID: ethers.ZeroHash,
      data: encodedData,
      value: 0n,
    },
  });

  log('STEP 3', `EAS attest tx sent: https://sepolia.basescan.org/tx/${tx.hash}`);
  const receipt = await tx.wait();
  if (!receipt) throw new Error('EAS attest tx receipt is null');

  // Parse Attested event to get attestation UID
  const iface = new ethers.Interface(EAS_ABI as ethers.InterfaceAbi);
  let attestationUID: string | undefined;
  for (const evLog of receipt.logs) {
    try {
      const parsed = iface.parseLog({ topics: [...evLog.topics], data: evLog.data });
      if (parsed?.name === 'Attested') {
        attestationUID = parsed.args.uid as string;
        break;
      }
    } catch { /* skip */ }
  }
  if (!attestationUID) throw new Error('Could not parse Attested event — UID not found');

  log('STEP 3', `✅ EAS attestation confirmed!`);
  log('STEP 3', `   UID: ${attestationUID}`);
  log('STEP 3', `   easscan: https://base-sepolia.easscan.org/attestation/view/${attestationUID}`);
  log('STEP 3', `   basescan: https://sepolia.basescan.org/tx/${tx.hash}`);

  saveState({ easAttestationUID: attestationUID, easAttestTxHash: tx.hash });
  return { schemaUID, attestationUID, txHash: tx.hash };
}

// ─── Verification (Step 4) ───────────────────────────────────────────────────

export async function verifyAttestation(
  attestationUID: string,
  expectedHash: string,
): Promise<void> {
  log('STEP 4', `Fetching EAS attestation on-chain: ${attestationUID}`);
  // Give public RPC 2s to catch up after the tx was included
  await new Promise((r) => setTimeout(r, 2000));

  const easContract = new ethers.Contract(EAS_CONTRACT, EAS_ABI, provider);
  const attestation = await (easContract.getAttestation as (uid: string) => Promise<{
    uid: string; schema: string; attester: string; time: bigint; data: string;
  }>)(attestationUID);

  if (!attestation || attestation.uid === ethers.ZeroHash) {
    throw new Error(`Attestation ${attestationUID} not found on-chain`);
  }

  // Decode ABI-encoded data to extract deliverableHash
  const abiCoder = ethers.AbiCoder.defaultAbiCoder();
  const decoded = abiCoder.decode([...EAS_SCHEMA_TYPES], attestation.data);
  const attestedHash = decoded[0] as string; // deliverableHash is first field

  if (attestedHash.toLowerCase() !== expectedHash.toLowerCase()) {
    throw new Error(
      `Hash mismatch! attested=${attestedHash} expected=${expectedHash}`,
    );
  }

  log('STEP 4', `✅ EAS attestation verified on-chain`);
  log('STEP 4', `   attester=${attestation.attester}`);
  log('STEP 4', `   time=${new Date(Number(attestation.time) * 1000).toISOString()}`);
  log('STEP 4', `   attested hash matches recomputed hash ✅`);
}
