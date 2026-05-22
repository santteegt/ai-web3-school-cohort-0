---
title: "Tokens"
type: concept
tags: [ai-foundations, llm]
source_count: 1
date_updated: "2026-05-22"
---

## Definition

A token is the basic unit of text that a language model processes, produced by a tokenizer that splits raw text into segments. Tokens are not words — a single word may be one or several tokens, and a single token may be a subword, punctuation mark, or special character.

## Key Points

- Tokens directly affect three things: **how much context can fit**, **how much a call costs**, and **whether the model can see key information completely**
- Token boundaries can split critical information (e.g. an Ethereum address may be tokenized across several tokens)
- Understanding tokenization helps predict why models sometimes "miss" things in long inputs — the token budget ran out or key data was split
- Technical content like code, addresses, and JSON tends to tokenize into more tokens than equivalent natural language
- Token count ≠ character count or word count; always check with a tokenizer tool when optimizing prompts

## Related Concepts

- [[large-language-model]] — the model that processes tokens
- [[context-window]] — measured in tokens; bounds how much can fit per request
- [[embeddings]] — tokens are converted to embeddings before processing
- [[transformer-architecture]] — operates on token representations via attention

## Sources

- [[sources/llms]] — token handling and its three effects
