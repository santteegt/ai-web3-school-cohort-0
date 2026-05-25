---
title: "Vibe Coding"
type: source
tags: [ai-foundations, vibe-coding, ai-coding, agent]
source_file: "raw/Vibe Coding.md"
source_hash: "sha256:8216d42de88af260f7c3873b5154953c646407403b85e01dc118f8b1ff9d5542"
date_ingested: "2026-05-24"
---

## Summary

This source reframes vibe coding from "coding by feeling" to a disciplined human-AI collaboration practice where humans own direction, constraints, and acceptance while agents handle generation and modification. Its core insight is that increased coding speed demands better engineering discipline, not less — feedback loops without tests, review, and version control only amplify disorder. The source provides concrete recommendations for integrating AI coding tools into the full engineering process.

## Key Concepts

- [[vibe-coding]] — human-AI software iteration; humans own direction/acceptance, agents handle generation/modification
- [[ai-coding]] — shortens the engineering feedback loop; requires small tasks, accurate context, and hard verification
- [[hallucination]] — AI coding tools hallucinate API signatures and methods; all output must be tested and reviewed
- [[tool-calling]] — AI coding agents call editors, terminals, and tools via tool use; require permission and log management
- [[guardrails]] — chain-related code is higher risk; must go through review, simulation, and multi-party confirmation before deployment

## Notable Points

- "AI cannot take over engineering judgment for you" — task description clarity, result review, change scope control, and bug verification are all human responsibilities.
- Vibe coding is not suitable for "rewriting the whole project" — prefer local patches and traceable small changes.
- In AI × Web3, vibe coding can speed up hackathon exploration, but smart contract code requires review, simulation, and multi-party confirmation regardless of how it was generated.
