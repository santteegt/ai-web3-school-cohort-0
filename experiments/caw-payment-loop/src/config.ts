import 'dotenv/config';

function requireEnv(name: string): string {
  const v = process.env[name];
  if (!v) throw new Error(`Missing required environment variable: ${name}`);
  return v;
}

export const config = {
  caw: {
    apiUrl: process.env.AGENT_WALLET_API_URL ?? 'https://api.agenticwallet.cobo.com',
    apiKey: requireEnv('AGENT_WALLET_API_KEY'),
    walletId: requireEnv('AGENT_WALLET_WALLET_ID'),
    // Cobo chain ID for Base Sepolia (TBASE_SETH) — confirmed via Cobo's chain registry
    chainId: process.env.CAW_CHAIN_ID ?? 'TBASE_SETH',
    // EVM address of the Cobo MPC wallet — required for EIP-712 `from` field
    walletAddress: requireEnv('AGENT_WALLET_ADDRESS') as `0x${string}`,
  },
  stub: {
    port: parseInt(process.env.STUB_SERVER_PORT ?? '3402', 10),
    // Address that receives x402 payments — must be funded on Base Sepolia
    receiverAddress: requireEnv('STUB_SERVER_ADDRESS') as `0x${string}`,
    // USD price per inference call (e.g. "0.001" = $0.001)
    pricePerCallUsd: process.env.PRICE_PER_CALL_USD ?? '0.001',
  },
  pact: {
    // USD-denominated limits (currency-agnostic — works for USDC or ETH)
    perCallCeilingUsd: process.env.PACT_PER_CALL_CEILING_USD ?? '0.01',
    sessionBudgetUsd: process.env.PACT_SESSION_BUDGET_USD ?? '0.10',
    windowSeconds: parseInt(process.env.PACT_WINDOW_SECONDS ?? '3600', 10),
  },
  audit: {
    basescanUrl: process.env.BASESCAN_URL ?? 'https://sepolia.basescan.org',
    logPath: './logs/audit.json',
  },
  localSigner: {
    // Set USE_LOCAL_SIGNER=true to bypass CAW messageSign (dev/test only).
    // Provide a funded Base Sepolia test key via LOCAL_SIGNER_PRIVATE_KEY.
    enabled: process.env.USE_LOCAL_SIGNER === 'true',
    privateKey: (process.env.LOCAL_SIGNER_PRIVATE_KEY ?? '0x0') as `0x${string}`,
  },
} as const;
