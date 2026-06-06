/**
 * LOCAL SIGNER BYPASS — dev/test only.
 *
 * Signs an EIP-3009 TransferWithAuthorization payload using a local private
 * key via viem. Replaces the CAW messageSign flow when USE_LOCAL_SIGNER=true
 * in .env, allowing end-to-end testing of the x402 stub while Cobo's MPC
 * signing infrastructure is unavailable on Base Sepolia testnet.
 *
 * Never use a key that holds real funds.
 */

import { privateKeyToAccount } from 'viem/accounts';

/** Returns the EVM address for a given private key. */
export function localSignerAddress(privateKey: `0x${string}`): `0x${string}` {
  return privateKeyToAccount(privateKey).address;
}

export interface Eip3009SignInput {
  privateKey: `0x${string}`;
  domain: {
    name: string;
    version: string;
    chainId: number;
    verifyingContract: `0x${string}`;
  };
  message: {
    from: `0x${string}`;
    to: `0x${string}`;
    /** Decimal-string USDC amount in token units (e.g. "1000" = $0.001 USDC) */
    value: string;
    /** Unix timestamp string */
    validAfter: string;
    /** Unix timestamp string */
    validBefore: string;
    /** 0x-prefixed 32-byte random hex (bytes32) */
    nonce: `0x${string}`;
  };
}

const EIP3009_TYPES = {
  TransferWithAuthorization: [
    { name: 'from', type: 'address' },
    { name: 'to', type: 'address' },
    { name: 'value', type: 'uint256' },
    { name: 'validAfter', type: 'uint256' },
    { name: 'validBefore', type: 'uint256' },
    { name: 'nonce', type: 'bytes32' },
  ],
} as const;

export async function localSignEip3009(input: Eip3009SignInput): Promise<`0x${string}`> {
  const account = privateKeyToAccount(input.privateKey);

  return account.signTypedData({
    domain: input.domain,
    types: EIP3009_TYPES,
    primaryType: 'TransferWithAuthorization',
    message: {
      from: input.message.from,
      to: input.message.to,
      value: BigInt(input.message.value),
      validAfter: BigInt(input.message.validAfter),
      validBefore: BigInt(input.message.validBefore),
      nonce: input.message.nonce,
    },
  });
}
