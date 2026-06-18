/**
 * Step 1 — Register identity (both agents)
 *
 * CLIENT calls IdentityRegistry.register(agentURI_client) → client agentId
 * DEV    calls IdentityRegistry.register(agentURI_dev)    → dev agentId
 *
 * Uses data: URIs (no hosting needed). DEV's registration JSON embeds A2A endpoint.
 * Idempotent: if agentIds are already in state.json, skip registration and reuse.
 */

import { ethers } from 'ethers';
import {
  IDENTITY_REGISTRY,
  DEV_SERVER_URL,
  clientSigner,
  devSigner,
  CLIENT_ADDRESS,
  DEV_ADDRESS,
  log,
} from './config.js';
import { IDENTITY_REGISTRY_ABI } from './abis.js';
import { loadState, saveState } from './state.js';

function buildAgentURI(json: object): string {
  const encoded = Buffer.from(JSON.stringify(json)).toString('base64');
  return `data:application/json;base64,${encoded}`;
}

async function registerAgent(
  label: string,
  signer: ethers.Wallet,
  agentURI: string,
): Promise<{ agentId: bigint; txHash: string }> {
  const registry = new ethers.Contract(IDENTITY_REGISTRY, IDENTITY_REGISTRY_ABI, signer);
  log(label, `Calling register() from ${signer.address} ...`);

  const tx = await registry.register(agentURI) as ethers.ContractTransactionResponse;
  log(label, `Tx sent: https://sepolia.basescan.org/tx/${tx.hash}`);

  const receipt = await tx.wait();
  if (!receipt) throw new Error(`${label}: tx receipt is null`);

  // Parse Registered event to extract agentId
  const iface = new ethers.Interface(IDENTITY_REGISTRY_ABI as ethers.InterfaceAbi);
  let agentId: bigint | undefined;
  for (const evLog of receipt.logs) {
    try {
      const parsed = iface.parseLog({ topics: [...evLog.topics], data: evLog.data });
      if (parsed?.name === 'Registered') {
        agentId = parsed.args.agentId as bigint;
        break;
      }
    } catch { /* skip non-matching logs */ }
  }
  if (agentId === undefined) throw new Error(`${label}: could not find Registered event`);

  log(label, `Registered! agentId=${agentId.toString()}  tx=${tx.hash}`);
  return { agentId, txHash: tx.hash };
}

export async function registerIdentities(): Promise<{
  clientAgentId: bigint;
  devAgentId: bigint;
  clientRegTxHash: string;
  devRegTxHash: string;
}> {
  const state = loadState();

  if (state.clientAgentId && state.devAgentId) {
    log('STEP 1', `Reusing existing identities from state.json`);
    log('STEP 1', `CLIENT agentId=${state.clientAgentId}  DEV agentId=${state.devAgentId}`);
    return {
      clientAgentId: BigInt(state.clientAgentId),
      devAgentId: BigInt(state.devAgentId),
      clientRegTxHash: state.clientRegTxHash!,
      devRegTxHash: state.devRegTxHash!,
    };
  }

  log('STEP 1', '=== Registering agent identities on ERC-8004 ===');
  log('STEP 1', `CLIENT address: ${CLIENT_ADDRESS}`);
  log('STEP 1', `DEV address:    ${DEV_ADDRESS}`);

  // DEV registration JSON — advertises its A2A endpoint (required link: identity → A2A endpoint)
  const devRegistrationJSON = {
    name: 'DEV Agent',
    description: 'TypeScript developer agent — writes code, attests deliverables via EAS, delivers via A2A',
    version: '1.0.0',
    services: [
      {
        name: 'A2A',
        endpoint: DEV_SERVER_URL,
        version: '1.0.0',
        skills: ['write_hello_world', 'code_delivery'],
      },
    ],
    trustModels: { reputation: true },
  };

  // CLIENT registration JSON — no A2A server (acts as client only)
  const clientRegistrationJSON = {
    name: 'CLIENT Agent',
    description: 'Client agent — requests code delivery, verifies EAS attestations, writes ERC-8004 reputation',
    version: '1.0.0',
    services: [],
    trustModels: { reputation: true },
  };

  const [devResult, clientResult] = await Promise.all([
    registerAgent('STEP 1 DEV', devSigner, buildAgentURI(devRegistrationJSON)),
    registerAgent('STEP 1 CLIENT', clientSigner, buildAgentURI(clientRegistrationJSON)),
  ]);

  saveState({
    devAgentId: devResult.agentId.toString(),
    devRegTxHash: devResult.txHash,
    clientAgentId: clientResult.agentId.toString(),
    clientRegTxHash: clientResult.txHash,
    clientAddress: CLIENT_ADDRESS,
    devAddress: DEV_ADDRESS,
  });

  log('STEP 1', `✅ Identities registered.`);
  log('STEP 1', `   CLIENT agentId=${clientResult.agentId}  tx=https://sepolia.basescan.org/tx/${clientResult.txHash}`);
  log('STEP 1', `   DEV    agentId=${devResult.agentId}    tx=https://sepolia.basescan.org/tx/${devResult.txHash}`);

  return {
    clientAgentId: clientResult.agentId,
    devAgentId: devResult.agentId,
    clientRegTxHash: clientResult.txHash,
    devRegTxHash: devResult.txHash,
  };
}
