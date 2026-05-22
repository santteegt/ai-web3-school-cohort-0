---
title: "Context"
type: source
tags: [ai-foundations, context, context-engineering, memory, knowledge-base]
source_file: "raw/Context.md"
source_hash: "sha256:51308fd924cb419e245d5d0f867ea6c077af25947b29466b80830d2a4df9db51"
date_ingested: "2026-05-22"
---

## Summary

This source frames context not as a simple text buffer, but as an information governance problem. Context is everything the model can see, use, and be influenced by in a session — and the system must decide what enters, with what identity, and how it exits after expiration. It introduces the five-layer agent context model (instruction, task, fact, knowledge, memory) and defines context engineering as the discipline of designing how information enters the model at the right layer.

## Key Concepts

- [[context-window]] — max amount of context a model can process per request; longer ≠ better focus
- [[context-engineering]] — design of how context enters the model; goal is working at the right information layer
- [[agent-memory]] — information retained across requests; must be revocable; cannot replace real-time authorization
- [[knowledge-base]] — external repository the system retrieves from; requires source, version, deprecation tracking
- [[five-layer-agent-context]] — instruction, task, fact, knowledge, memory layers
- [[prompt-injection]] — untrusted content treated as system instructions; defense via zone isolation
- [[information-governance]] — labeling information by source, freshness, permission, trust level

## Notable Points

- "Context is not simply long-text concatenation. It is an information governance problem."
- "Memory cannot replace real-time authorization — anything related to identity, permissions, assets, or external side effects must be rebound to the current session."
- "Trusted sources must be explicitly marked" — system state, user input, retrieved documents, and tool results must occupy separate zones.
