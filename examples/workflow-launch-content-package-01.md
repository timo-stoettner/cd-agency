# Case Study: Launch Content Package Workflow

## Context

- **Product**: B2B SaaS analytics platform launching a new "Team Insights" feature
- **Page/Screen**: Multiple surfaces — onboarding, empty states, CTAs, and consolidated launch copy
- **Target Audience**: Product managers and team leads who manage cross-functional teams
- **Workflow Used**: `launch-content-package.yaml` (3 parallel + 1 consolidation)
- **Agents Used**: Onboarding Flow Designer + CTA Optimization Specialist + Empty State Content Designer (parallel) → Content Design Generalist (consolidation)

## Input Brief

> **Feature name:** Team Insights
> **What it does:** Aggregates team activity across projects, shows workload distribution, identifies bottlenecks, and surfaces collaboration patterns
> **Target user:** Product managers with teams of 5-20 people
> **Launch type:** In-app announcement to existing users + new user onboarding
> **Key value prop:** "See how your team actually works — not just what they ship"

## Parallel Agent Outputs

### Agent 1: Onboarding Flow Designer — Feature Introduction

> **3-screen introduction flow (shown on first visit to Team Insights):**
>
> **Screen 1 — Value hook:**
> Headline: "See how your team works together"
> Subtext: "Team Insights shows workload balance, collaboration patterns, and bottlenecks — so you can make better team decisions."
> CTA: "Show me my team's data"
> Visual: Abstract team graph animation
>
> **Screen 2 — Orientation (interactive):**
> Headline: "Here's what you're looking at"
> Three highlighted areas with tooltips:
> 1. Workload bar chart — "Who's overloaded and who has capacity"
> 2. Collaboration graph — "Who works with whom most often"
> 3. Bottleneck alerts — "Where work is getting stuck"
> CTA: "Got it, let me explore"
>
> **Screen 3 — Activation prompt:**
> Headline: "Invite your team to unlock full insights"
> Subtext: "Team Insights works best with 3+ active members. You have 1 right now."
> CTA: "Invite teammates"
> Skip: "Explore with my data only"

### Agent 2: CTA Optimization Specialist — Conversion Points

> **In-app announcement banner:**
> Headline: "New: See how your team actually works"
> CTA: "Explore Team Insights" [RECOMMENDED]
> Dismiss: "Maybe later" (tracks for re-engagement)
>
> **Upgrade prompt (for free-tier users):**
> "Team Insights is available on the Pro plan"
> CTA: "Start 14-day Pro trial — no credit card"
> Supporting: "Includes Team Insights, custom dashboards, and priority support"
>
> **Sidebar navigation entry:**
> Label: "Team Insights" with "New" badge (auto-expires after 30 days)
>
> **Re-engagement (if dismissed banner):**
> Trigger: User views any team-related page 3+ times
> Tooltip: "Curious about your team's workload balance? → Team Insights"

### Agent 3: Empty State Content Designer — Zero-Data States

> **No team members yet:**
> Illustration: Connected nodes (abstract team)
> Headline: "Team Insights needs your team"
> Subtext: "Invite at least 2 teammates to see collaboration patterns and workload balance."
> CTA: "Invite teammates"
> Secondary: "See a demo with sample data"
>
> **Team exists but insufficient data (<7 days):**
> Headline: "Collecting your team's patterns"
> Subtext: "Team Insights needs about a week of activity to show meaningful patterns. Check back on [date]."
> Progress indicator: "Day 3 of 7 — building your first insights"
> CTA: "Notify me when insights are ready"
>
> **Single metric unavailable (e.g., collaboration graph needs 3+ members):**
> Inline message: "Add 1 more teammate to unlock collaboration patterns"
> CTA: "Invite"

## Consolidation: Content Design Generalist

> **Voice & terminology audit across all three outputs:**
>
> **Standardized terms:**
> - "Team Insights" — always capitalized, always two words (not "team insights" or "TeamInsights")
> - "teammates" — not "team members" or "collaborators" (consistent with product voice)
> - "workload balance" — not "workload distribution" (simpler, more natural)
> - "collaboration patterns" — kept as-is (specific and clear)
>
> **Tone consistency check:**
> - All three outputs use direct, confident tone — ✓ consistent
> - Onboarding is slightly more educational, CTAs more action-oriented — ✓ appropriate variation
> - Empty states are encouraging without being dismissive of the wait — ✓ good
>
> **Cross-surface conflicts resolved:**
> 1. Onboarding said "5+ active members" but empty state said "2 teammates" — **standardized to "3+ active members"** (matches actual feature threshold)
> 2. CTA used "Explore" but onboarding used "Show me" — **kept both** (different contexts warrant different verbs: explore = discovery, show me = guided)
> 3. Added "New" badge expiration (30 days) to prevent stale UI
>
> **Content hierarchy (user journey order):**
> 1. Announcement banner (awareness)
> 2. Onboarding flow (first visit education)
> 3. Empty states (data collection period)
> 4. Full feature (ongoing use)
> 5. Re-engagement (if user drops off)

## Pipeline Transformation Summary

| Deliverable | Surface | Words | Agent |
|-------------|---------|-------|-------|
| 3-screen onboarding flow | In-app overlay | 89 | Onboarding Flow Designer |
| 4 CTA placements | Banner, upgrade, nav, tooltip | 67 | CTA Optimization Specialist |
| 3 empty state variations | Feature page | 74 | Empty State Content Designer |
| Terminology + tone guide | Internal reference | 52 | Content Design Generalist |
| **Total** | **10 content pieces** | **282 words** | **4 agents** |

## Why the Parallel Pipeline Matters

| Without workflow | With workflow |
|-----------------|---------------|
| One writer creates all 10 pieces sequentially | 3 specialists work simultaneously on their expertise area |
| Terminology drift across surfaces ("team members" vs "teammates") | Generalist consolidation catches and standardizes |
| CTA tone leaks into empty states (too pushy) or vice versa (too passive) | Each agent optimizes for its surface's intent |
| Feature threshold inconsistency (different numbers in different places) | Cross-surface audit catches conflicts |
| ~2 hours of sequential work | Parallel execution + consolidation |

The parallel pipeline doesn't just save time — it produces better content because each agent focuses on what it does best, and the consolidation pass ensures everything works together.
