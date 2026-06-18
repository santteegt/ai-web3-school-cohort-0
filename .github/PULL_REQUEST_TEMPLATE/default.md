## What this PR does

<!-- One sentence. Link to the Definition issue. -->

Closes #

## Sprint Day

<!-- Day 8 / 9 / 10 / 11 / 12 -->

## 7D Checklist

### Definition → Design Gate
- [ ] Definition issue linked above
- [ ] Design issue exists and is approved (or this is a Day 8 probe — mark N/A)
- [ ] Implementation matches the Design spec

### GuildOS Constraints
- [ ] No hardcoded private keys, API keys, or seed phrases
- [ ] Only Base Sepolia testnet — no mainnet call path
- [ ] All A2A messages are logged to `./logs/a2a_trace_{date}.json`
- [ ] All GLM-5.1 calls are logged to `./logs/glm_trace_{date}.json`
- [ ] Human gate prompts halt execution and wait for `y/N` — no auto-proceed
- [ ] `giveFeedback()` is called from guild contract or Marco's EOA — NOT the Specialist wallet

### Diagnostics
- [ ] `pytest tests/` passes
- [ ] `ruff check src/` clean
- [ ] On-chain tx hashes saved to `./logs/tx_hashes.md` (if applicable)

### Documentation
- [ ] `docs/TECH_STACK.md` Decision Log updated if a library/API choice changed
- [ ] `docs/RISKS.md` Decision Log updated if a fallback was triggered
- [ ] `docs/VALIDATION_PLAN.md` check updated for the relevant section
