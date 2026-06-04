/**
 * P-001 — x402 Service Provider
 *
 * Express server with one x402-protected endpoint.
 * - No payment → 402 + PAYMENT-REQUIRED header (base64 JSON challenge)
 * - Valid payment proof → 200 mock AI inference response
 *
 * Uses @x402/express (current, non-legacy) with x402.org facilitator.
 * Network: Base Sepolia (eip155:84532)
 */

import express from 'express';
import { paymentMiddleware, x402ResourceServer } from '@x402/express';
import { ExactEvmScheme } from '@x402/evm/exact/server';
import { HTTPFacilitatorClient } from '@x402/core/server';
import { config } from './config.js';

const MOCK_RESULTS = [
  'Agentic systems require economic rails as much as they require intelligence.',
  'Decentralized trust enables autonomous coordination without intermediaries.',
  'Machine-to-machine payments unlock composable service markets.',
  'On-chain authorization creates auditable, enforceable permission boundaries.',
  'The x402 protocol turns HTTP into a native payment channel.',
];

const FACILITATOR_URI = 'https://x402.org/facilitator';

const app = express();

// ── x402 setup ──────────────────────────────────────────────────────────────
// x402.org/facilitator is the default testnet facilitator — handles verify + settle
const facilitatorClient = new HTTPFacilitatorClient({
  url: FACILITATOR_URI,
});

const resourceServer = new x402ResourceServer(facilitatorClient).register(
// const resourceServer = new x402ResourceServer().register(
  'eip155:84532', // Base Sepolia
  new ExactEvmScheme(),
);

app.use(
  paymentMiddleware(
    {
      'GET /api/inference': {
        accepts: [
          {
            scheme: 'exact',
            price: `$${config.stub.pricePerCallUsd}`,
            network: 'eip155:84532',
            payTo: config.stub.receiverAddress,
          }
        ],
        description: 'Mock AI inference — pay-per-call via x402',
      },
    },
    resourceServer,
  ),
);

// ── Protected endpoint ───────────────────────────────────────────────────────
app.get('/api/inference', (req, res) => {
  const result = MOCK_RESULTS[Math.floor(Math.random() * MOCK_RESULTS.length)];
  const response = {
    result,
    model: 'mock-inference-v1',
    timestamp: Date.now(),
    paymentVerified: true,
  };

  console.log(`[stub] ✓ Verified payment — serving response`);
  console.log(`[stub]   result: "${result}"`);

  res.json(response);
});

// ── Health check (unprotected) ───────────────────────────────────────────────
app.get('/health', (_req, res) => {
  res.json({ status: 'ok', protected: ['/api/inference'] });
});

// ── Start ────────────────────────────────────────────────────────────────────
const port = config.stub.port;
app.listen(port, () => {
  console.log(`\n[stub] x402 inference API running`);
  console.log(`[stub]   endpoint:  http://localhost:${port}/api/inference`);
  console.log(`[stub]   health:    http://localhost:${port}/health`);
  console.log(`[stub]   payTo:     ${config.stub.receiverAddress}`);
  console.log(`[stub]   price:     $${config.stub.pricePerCallUsd} USDC per call`);
  console.log(`[stub]   network:   Base Sepolia (eip155:84532)`);
  console.log(`[stub]   facilitator: ${FACILITATOR_URI}`);
  console.log('[stub] Waiting for requests...\n');
});
