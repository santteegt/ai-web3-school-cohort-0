import 'dotenv/config';
import { ethers } from 'ethers';

function requireEnv(name: string): string {
  const val = process.env[name];
  if (!val) throw new Error(`Missing required env var: ${name}`);
  return val;
}

export const RPC_URL = process.env.RPC_URL ?? 'https://sepolia.base.org';
export const CHAIN_ID = 84532;
export const DEV_PORT = parseInt(process.env.DEV_PORT ?? '3001', 10);
export const DEV_SERVER_URL = `http://localhost:${DEV_PORT}`;

// Base Sepolia contract addresses
export const IDENTITY_REGISTRY  = '0x8004A818BFB912233c491871b3d84c89A494BD9e';
export const REPUTATION_REGISTRY = '0x8004B663056A597Dffe9eCcC1965A193B7388713';
export const EAS_CONTRACT        = '0x4200000000000000000000000000000000000021';
export const SCHEMA_REGISTRY     = '0x4200000000000000000000000000000000000020';

// EAS schema for this PoC (registered once, reused)
export const EAS_SCHEMA = 'bytes32 deliverableHash, string taskType, string a2aTaskId, address devAgent';

//EAS Schema types for ABI encoding
export const EAS_SCHEMA_NAMES = ['deliverableHash', 'taskType', 'a2aTaskId', 'devAgent'];
export const EAS_SCHEMA_TYPES = ['bytes32', 'string', 'string', 'address'];


// Provider and signers (keys loaded from env; addresses are derived and safe to log)
export const provider = new ethers.JsonRpcProvider(RPC_URL, {
  chainId: CHAIN_ID,
  name: 'base-sepolia',
});

export const clientSigner = new ethers.Wallet(requireEnv('PRIVATE_KEY_CLIENT'), provider);
export const devSigner    = new ethers.Wallet(requireEnv('PRIVATE_KEY_DEV'), provider);

export const CLIENT_ADDRESS = clientSigner.address;
export const DEV_ADDRESS    = devSigner.address;

export function log(step: string, msg: string): void {
  console.log(`[${step}] ${msg}`);
}
