# RUN_LOG.md — On-Chain Evidence

> Canonical evidence from the final clean run.
> Appended by demo.ts; earlier debug runs removed.

---

## Run 2026-06-17T05:53:50.371Z (canonical)

- CLIENT address: `0x10136Fa41B6522E4DBd068C6F7D80373aBbCFBe6`
- DEV address: `0x7C510aBf45c10a9aB949ef69ccBba5d77312d814`

### Step 1 — Register Identities
- CLIENT agentId: `7060`
- CLIENT tx: https://sepolia.basescan.org/tx/0x5164152e67d7a4c6fbaca0391213b7495a5717bee25015710126072c1b47034d
- DEV agentId: `7059`
- DEV tx: https://sepolia.basescan.org/tx/0x14a2c153ea867ff2baf7c26bc57bd6b708ef88734c7ea628eb2460914062f22b

### Step 2 — A2A Task Delegation
- A2A task ID: `4d406ff4-8182-4c95-8852-96a1de70c151`
- A2A context ID: `834fd25d-bf82-482c-bec7-c9de8e7ba313`

### Step 3 — EAS Attestation
- EAS schema UID: `0x2dba9942d1a8641e31f045580478f3f4af72ad54848e873fd67b4ec5b3129bab`
- EAS schema: https://base-sepolia.easscan.org/schema/view/0x2dba9942d1a8641e31f045580478f3f4af72ad54848e873fd67b4ec5b3129bab
- Deliverable hash: `0xa4f5e33157d51bf7a424f58c4f46456a2f7fe52e0567e4a31f2ecf6fd8726407`
- EAS attestation UID: `0xad4248110505b27adc3b4fed651fd7be5871838983f2939b863d05c1d8478e4d`
- easscan: https://base-sepolia.easscan.org/attestation/view/0xad4248110505b27adc3b4fed651fd7be5871838983f2939b863d05c1d8478e4d
- Attest tx: https://sepolia.basescan.org/tx/0x3a8779e81a5ff2819084724c3bb7d3e7787994127a9bd2fc7447de443f73f907

### Step 4 — CLIENT Approval
- EAS attestation verified on-chain ✅
- Hash match confirmed ✅
- A2A "accepted" message sent

### Step 5 — DEV Review Request
- DEV sent review request via A2A: "Thank you for accepting the deliverable! Please provide your feedback and reputation score for this delivery. Your review will be recorded on ERC-8004 via giveFeedback()."

### Step 6 — ERC-8004 Reputation Feedback
- giveFeedback tx: https://sepolia.basescan.org/tx/0xb8b45a23164e6cfcaf9f3da24bf74b41acf27b3a2540197cbcd80faa14b68609
- getSummary BEFORE: count=0 value=0
- getSummary AFTER:  count=1  value=100
- Reputation delta: 0 → 1 ✅

### ✅ Demo Complete
| Item | Value |
|------|-------|
| CLIENT agentId | `7060` |
| DEV agentId | `7059` |
| EAS schema UID | `0x2dba9942d1a8641e31f045580478f3f4af72ad54848e873fd67b4ec5b3129bab` |
| EAS attestation UID | `0xad4248110505b27adc3b4fed651fd7be5871838983f2939b863d05c1d8478e4d` |
| giveFeedback tx | `0xb8b45a23164e6cfcaf9f3da24bf74b41acf27b3a2540197cbcd80faa14b68609` |
| Reputation count | 0 → 1 |

## Run 2026-06-18T05:03:19.280Z

- CLIENT address: `0x10136Fa41B6522E4DBd068C6F7D80373aBbCFBe6`
- DEV address: `0x7C510aBf45c10a9aB949ef69ccBba5d77312d814`

### Step 1 — Register Identities
- CLIENT agentId: `7060`
- CLIENT tx: https://sepolia.basescan.org/tx/0x5164152e67d7a4c6fbaca0391213b7495a5717bee25015710126072c1b47034d
- DEV agentId: `7059`
- DEV tx: https://sepolia.basescan.org/tx/0x14a2c153ea867ff2baf7c26bc57bd6b708ef88734c7ea628eb2460914062f22b

### Step 2 — A2A Task Delegation
- A2A task ID: `f36667d8-2e17-422d-a37b-481e13b37438`
- A2A context ID: `ea295781-f550-4352-80ae-205b0614e9ac`

### Step 3 — EAS Attestation
- EAS schema UID: `0x2dba9942d1a8641e31f045580478f3f4af72ad54848e873fd67b4ec5b3129bab`
- EAS schema: https://base-sepolia.easscan.org/schema/view/0x2dba9942d1a8641e31f045580478f3f4af72ad54848e873fd67b4ec5b3129bab
- Deliverable hash: `0xe292f99f6aa60efd6b1c8fd433bb53fa4aaf6a45731a68baa08f3d83417aed43`
- EAS attestation UID: `0xe0ebe0aa8443a38455151630687d782f09be79c2a938ae39472984853c91b9ea`
- easscan: https://base-sepolia.easscan.org/attestation/view/0xe0ebe0aa8443a38455151630687d782f09be79c2a938ae39472984853c91b9ea
- Attest tx: https://sepolia.basescan.org/tx/0x9928372db8bcc77a37888a0c930d0d68db1d5f2b98bd09d3c053f104e66d7086

### Step 4 — CLIENT Approval
- EAS attestation verified on-chain ✅
- Hash match confirmed ✅
- A2A "accepted" message sent

### Step 5 — DEV Review Request
- DEV sent review request via A2A: "Thank you for accepting the deliverable! Please provide your feedback and reputation score for this delivery. Your revie..."

### Step 6 — ERC-8004 Reputation Feedback
- giveFeedback tx: https://sepolia.basescan.org/tx/0x85535f4a5811ec678f78d17b24c230658899b958b34f68b2cecba1d0de5bd894
- getSummary BEFORE: count=1 value=100
- getSummary AFTER:  count=2  value=100
- Reputation delta: 1 → 2 ✅

### ✅ Demo Complete
| Item | Value |
|------|-------|
| CLIENT agentId | `7060` |
| DEV agentId | `7059` |
| EAS schema UID | `0x2dba9942d1a8641e31f045580478f3f4af72ad54848e873fd67b4ec5b3129bab` |
| EAS attestation UID | `0xe0ebe0aa8443a38455151630687d782f09be79c2a938ae39472984853c91b9ea` |
| giveFeedback tx | `0x85535f4a5811ec678f78d17b24c230658899b958b34f68b2cecba1d0de5bd894` |
| Reputation count | 1 → 2 |
