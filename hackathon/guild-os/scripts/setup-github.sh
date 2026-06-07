#!/usr/bin/env bash
# setup-github.sh — Create GuildOS labels and sprint milestones on GitHub
# Usage: ./scripts/setup-github.sh [--repo owner/repo]
# Requires: gh CLI authenticated

set -euo pipefail

REPO="${1:-santteegt/guild-os}"

echo "Setting up GitHub labels and milestones for: $REPO"
echo ""

# ─── Labels ───────────────────────────────────────────────────────────────────

create_label() {
  local name="$1" color="$2" desc="$3"
  gh label create "$name" --color "$color" --description "$desc" --repo "$REPO" --force
}

echo "Creating labels..."

# 7D phase labels
create_label "7d:discovery"   "0075ca" "Backlog / discovery item"
create_label "7d:definition"  "e4e669" "Requirements definition"
create_label "7d:design"      "d73a4a" "Technical design"

# Status labels
create_label "status:backlog"     "cfd3d7" ""
create_label "status:in-progress" "0075ca" ""
create_label "status:review"      "e4e669" ""
create_label "status:done"        "0e8a16" ""

# Priority labels (hackathon-specific)
create_label "priority:p0" "d73a4a" "Submission blocker"
create_label "priority:p1" "e4e669" "Demo quality"
create_label "priority:p2" "cfd3d7" "Judging evidence"
create_label "priority:p3" "fef2c0" "Presentation polish"

# Type labels
create_label "type:bug"         "d73a4a" ""
create_label "type:feature"     "a2eeef" ""
create_label "type:integration" "7057ff" "External API/SDK integration"
create_label "type:chore"       "fef2c0" ""

echo "✅ Labels created"
echo ""

# ─── Sprint Milestones (Days 8–13) ────────────────────────────────────────────

echo "Creating sprint milestones..."

# Function: create milestone if it doesn't exist
create_milestone() {
  local title="$1" due="$2" desc="$3"
  gh api "repos/$REPO/milestones" \
    --method POST \
    --field title="$title" \
    --field due_on="$due" \
    --field description="$desc" \
    2>/dev/null || echo "  (skipped — may already exist: $title)"
}

create_milestone \
  "Day 8 — Validation" \
  "2026-06-08T23:59:00Z" \
  "Confirm all live integrations pass or trigger fallbacks. P0: AgentFightClub launch live · A2A green · GLM-5.1 task locked"

create_milestone \
  "Day 9 — Wallets + Identity" \
  "2026-06-09T23:59:00Z" \
  "Agent wallets on-chain, ERC-8004 agents registered, guild funded. P0: Both wallet addresses · Guild funded with mandate"

create_milestone \
  "Day 10 — A2A + Execution" \
  "2026-06-10T23:59:00Z" \
  "Full A2A flow + GLM-5.1 task + deliverable hash on Base Sepolia. P0: task/delivered received · Hash committed · Basescan tx #1 saved"

create_milestone \
  "Day 11 — Settlement + Reputation + E2E" \
  "2026-06-11T23:59:00Z" \
  "Close the loop. P0: settle() tx · ERC-8004 delta visible · Full loop smoke test passes (x2)"

create_milestone \
  "Day 12 — Demo Prep" \
  "2026-06-12T23:59:00Z" \
  "Nothing new built. README, demo script, submission artifacts, repo clean."

create_milestone \
  "Day 13 — Submission" \
  "2026-06-13T04:00:00Z" \
  "Demo video + submission form. DEADLINE: 2026-06-13 12:00 UTC+8 (04:00 UTC). NO late submissions."

echo "✅ Milestones created"
echo ""

# ─── Next Steps ───────────────────────────────────────────────────────────────

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Setup complete for: $REPO"
echo ""
echo "Next steps:"
echo ""
echo "1. Create the GitHub Project board:"
echo "   https://github.com/$REPO/projects/new"
echo "   → Choose 'Board' type"
echo "   → Add columns: Backlog · Day 8 · Day 9 · Day 10 · Day 11 · Day 12 · Done"
echo ""
echo "2. Enable branch protection on 'main':"
echo "   https://github.com/$REPO/settings/branches"
echo "   → Require status checks: diagnostics-gate"
echo ""
echo "3. Add repository secrets (Settings → Secrets → Actions):"
echo "   ALCHEMY_API_KEY"
echo "   GLM_API_KEY"
echo ""
echo "4. Create issues for Day 8 P0 tasks:"
echo "   gh issue create --title 'AgentFightClub launch probe' --label '7d:discovery,priority:p0,type:integration' --milestone 'Day 8 — Validation' --repo $REPO"
echo "   gh issue create --title 'A2A Day 1 test suite (5 gates)' --label '7d:discovery,priority:p0,type:integration' --milestone 'Day 8 — Validation' --repo $REPO"
echo "   gh issue create --title 'GLM-5.1 demo task type selection' --label '7d:discovery,priority:p0,type:integration' --milestone 'Day 8 — Validation' --repo $REPO"
echo "   gh issue create --title 'ZeroDev smart account deploy on Base Sepolia' --label '7d:discovery,priority:p0,type:integration' --milestone 'Day 9 — Wallets + Identity' --repo $REPO"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
