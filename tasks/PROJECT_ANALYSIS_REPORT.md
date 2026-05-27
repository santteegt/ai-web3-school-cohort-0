
# AixWeb3 Project Analysis

> **Full analysis report**: https://docs.google.com/document/d/1BK_AuE9MxuxhBAYBE3pYMB9sK0zFe3U_n3gwaSlXHyQ/edit?usp=sharing \
> **Tools used**: Gemini Deep Research for Project Analysis

# Project Brief: Bankr.bot

### 1. What problem is it trying to solve?

Bankr.bot moves DeFi execution directly into conversational social feeds (such as X/Twitter and Farcaster) to simplify crypto transactions into intuitive, natural language commands.

### 2. What is the AI component?

* **Natural Language Command Processing:** A semantic translation engine parses plain-text messages (e.g., *"buy $50 of Ethereum"* or *"swap 100 USDC for ETH on Base"*) to extract execution variables like assets, quantities, slippage, and destination chains, generating structured on-chain payloads automatically.


* **Social Sentiment Analysis:** Monitors popularity, keyword mentions, and real-time shifts in social sentiment across channels like Twitter and Farcaster to aid trading decisions.


* **Automated Technical Indicators:** An analytical model evaluates hourly token data, calculating indicators like RSI, MACD, and moving average crossovers to generate automated, technical trading signals.



### 3. What is the Web3 component?

* **Embedded Custodial & Non-Custodial Wallets:** Partners with Privy to generate embedded wallets via email OTP, removing the need for manual seed phrase setups.


* **Multi-Chain Swaps and Anti-MEV Routing:** Integrates CoWSwap to protect users from front-running and MEV attacks while routing assets across Ethereum, Base, Polygon, Solana, and Unichain.


* **Doppler Protocol Launch Mechanics:** Employs the Doppler Protocol (designed by former Uniswap v4 core researcher Austin Adams) to enable non-linear bonding curves that prevent front-running by sniper bots while depositing tokenized LP fees straight into project treasuries.


* **Native Tokenomics ($BNKR$):** Deployed on Base with Solana interoperability, $BNKR$ powers premium subscriptions (Bankr Club), rewards copy-trading, and facilitates instant social airdrops.



### 4. What verifiable materials exist?

* **Consumer Platforms:** The main web terminal is active at `bankr.bot` and the API manager is live at `bankr.bot/api`.


* **Technical Documentation:** Official integration guides are hosted at `docs.bankr.bot` and CLI references at `docs.bankr.bot/cli`.


* **GitHub Repository Assets (`github.com/BankrBot`):** Contains open repositories including `/skills` (the primary agent Skill.md framework), `/claude-plugins` (TypeScript plugins connecting Claude Code to Bankr's trading rails), and `/token-strategist` (token deployment code).


* **On-Chain Deployments:** The Doppler Protocol's CreatorCoin deployment can be verified on BaseScan (contract: [0x7b67f8e45f91e043f80eeaea52f3dc8ff1e55a5a](https://basescan.org/address/0x7b67f8e45f91e043f80eeaea52f3dc8ff1e55a5a#code)).


* **Public Exploit Case Study:** A SlowMist audit details a real-world prompt injection vulnerability on X. An attacker bypassed input sanitization by sending a Morse code prompt to @grok, triggering @grok to output a transaction instruction that was read and executed by @bankrbot's custodial wallet system.

### 5. What did you learn, and what questions still remain?

* **Key Learning:** Embedding transaction triggers directly into public social environments allows social sentiment and trading to merge seamlessly. However, this architectural design creates highly complex threat vectors; delegating on-chain execution to autonomous agents reading raw, public social media feeds can result in severe cross-application prompt injection attacks (as highlighted by the Grok-to-Bankr Morse code exploit).


* **Remaining Questions:**
1. How does Bankr plan to implement robust, standardized safety sandboxes to insulate its NLP parsers from multi-agent prompt injection attacks without sacrificing natural language flexibility?

---

# Project Brief: Venice.ai

### 1. What problem is it trying to solve?

Traditional generative AI providers (e.g., OpenAI, Google) operate under centralized SaaS models where they log, profile, and permanently store highly sensitive user prompts—such as proprietary code, corporate strategies, and financial research. These logs are exposed to regulatory overreach, hardware breaches, and corporate data-mining. Venice.ai resolves this by designing a private, uncensored, zero-knowledge AI inference layer that removes user identities entirely.

### 2. What is the AI component?

* **Decentralized Multi-Modal Inference:** Runs more than 250 open-source text, image, audio, and video foundation models (including Claude 4.7, GPT-5.5, Qwen 3.7 Max, and DeepSeek V4) on decentralized GPU nodes running custom Venice client software.


* **Zero-Knowledge Architecture:** Prompts and outputs are processed strictly in transient GPU RAM and purged immediately upon streaming back to the browser; no data persists on remote disks.


* **Local-First Storage:** Chat histories and custom system instructions are stored exclusively on the user's browser, meaning data is encrypted locally and cannot be accessed if a server is breached.



### 3. What is the Web3 component?

* **Dual-Token Capital and Utility Model:** Built on the Base Layer 2 network :

  * **Venice Token ($VVV$):** The primary capital asset. Staking $VVV$ grants Venice Pro access, offers a 15% APR yield, and utilizes platform revenues for monthly buy-and-burn operations.

  * **DIEM Token:** A liquid compute credit minted by locking staked $VVV$. Each $DIEM$ represents $1 of renewing daily AI credit, turning compute costs from a recurring SaaS rent into an investable, sovereign asset.


* **Agent-Native Payments (x402):** Integrates the open-source x402 protocol. This embeds micropayments into standard HTTP 402 "Payment Required" responses, enabling autonomous agents to buy AI inference per request in USDC without an API key or account registration.


* **Crypto RPC:** Embeds direct JSON-RPC 2.0 proxy capabilities, allowing developers to query 11 supported blockchains directly using their Venice API keys.



### 4. What verifiable materials exist?

* **User and Token Portals:** Chat access is live at `venice.ai/chat` and token staking is active at `venice.ai/token`.


* **Technical Documentation:** API references are at `docs.venice.ai`, with a public LLM-readable index map available directly at `docs.venice.ai/llms.txt`.


* **GitHub Repository Assets (`github.com/veniceai`):** Public directories include `/api-docs` (Mintlify documents), `/venice-mcp-server` (Model Context Protocol linking private inference directly with Claude Code/Cursor), and `/x402-client` (TypeScript client facilitating wallet-funded inference).


* **On-Chain Contracts (Base):**
* $VVV$ Capital Token: [0xacfE6019Ed1A7Dc6f7B508C02d1b04ec88cC21bf](https://basescan.org/address/0xacfE6019Ed1A7Dc6f7B508C02d1b04ec88cC21bf#code)


* $DIEM$ Compute Credit Token: [0xf4d97f2da56e8c3098f3a8d538db630a2606a024](https://basescan.org/address/0xf4d97f2da56e8c3098f3a8d538db630a2606a024#code)


* sVVV Staking Registry: [0x321b7ff75154472b18edb199033ff4d116f340ff](https://basescan.org/address/0xe37a7920dbc11253ac6d031c29f592f71b348dca#code)


### 5. What did you learn, and what questions still remain?

* **Key Learning:** The staking-and-minting mechanics of the $VVV \rightarrow sVVV \rightarrow DIEM$ pipeline offer a viable model for utility-backed cryptoeconomics. By defining compute capacity as a renewing asset ($DIEM$), developers can escape the rent-seeking cycle of Web2 subscriptions.


* **Remaining Questions:**
1. What is the real-world performance overhead (in terms of latency and cost) of implementing homomorphic encryption or zero-knowledge computational proofs for high-throughput LLM inference across the decentralized GPU network?
