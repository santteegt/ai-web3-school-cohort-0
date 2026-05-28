---
title: "Sandbox"
type: concept
tags: [aixweb3-bridge, privacy-security, agent]
source_count: 1
date_updated: "2026-05-28"
---

## Definition

A Sandbox is an isolated execution environment used to run code, browse the web, process files, or call external tools. It restricts access to the file system, network, environment variables, and callable commands to prevent malicious input from accessing secrets or modifying projects.

## Key Points

- Must prohibit access to highly sensitive resources by default: `.env` files, SSH keys, wallet seeds, browser cookies, production database credentials
- Access to sensitive resources, when needed, must be through explicitly authorized tools
- For Web3 agents, browser sandboxing is critical: malicious DApp pages might induce agents to click signatures, download files, or copy addresses
- Browser automation should not be bound to wallet signing permissions without boundaries

## Related Concepts

- [[ai-security]]
- [[permission-isolation]]
- [[key-safety]]
- [[tool-permission]]
- [[agent-workflow]]
- [[malicious-context]]

## Sources

- [[sources/bridge-chapters]]
