# Case Study: SaaS Project Management Onboarding

## Context

- **Product**: Project management SaaS (Monday.com-style)
- **Page/Screen**: Post-signup onboarding flow — first 5 screens
- **Target Audience**: Team leads setting up their first workspace
- **Agent(s) Used**: Onboarding Flow Designer

## Before (Original Content)

> **Screen 1:** "Welcome to ProjectFlow! Let's get you set up."
> **Screen 2:** "Enter your company name and upload your logo."
> **Screen 3:** "Invite your team members by entering their email addresses below."
> **Screen 4:** "Choose a template to get started or create a blank project."
> **Screen 5:** "You're all set! Click 'Go to Dashboard' to begin."

## After (Agency Output)

> **Screen 1 — Value reminder:**
> Headline: "Let's get your team shipping faster"
> Subtext: "3 quick steps — takes about 2 minutes"
> CTA: "Set up my workspace"
>
> **Screen 2 — Workspace identity (Step 1 of 3):**
> Headline: "Name your workspace"
> Field: Workspace name (pre-filled with email domain, e.g., "Acme")
> Skip option: "I'll customize later" (ghost link)
> Progress: ████░░░░░░ 1/3
>
> **Screen 3 — First project (Step 2 of 3):**
> Headline: "Start with a real project"
> 3 template cards: "Sprint planning", "Product launch", "Bug tracking"
> Each shows: preview thumbnail + "Used by 2,000+ teams"
> Alt: "Start blank" (secondary link)
> Progress: ██████░░░░ 2/3
>
> **Screen 4 — Team invite (Step 3 of 3):**
> Headline: "Add your first collaborator"
> Subtext: "Projects are better with your team. Invite just one person to start."
> Field: Single email field (not a bulk form)
> CTA: "Send invite"
> Skip: "I'll invite later — show me around"
> Progress: █████████░ 3/3
>
> **Screen 5 — Activation moment:**
> Headline: "Your first project is ready"
> Shows: Their named project with the chosen template populated
> CTA: "Open my project"
> Subtext: "Tip: Create your first task to see ProjectFlow in action"

> **Key design decisions:**
> - Moved team invite to Step 3 (after they've invested in setup) — inviting first creates obligation without context
> - Removed logo upload entirely — low-value friction that delays time-to-value
> - Pre-filled workspace name from email domain — reduces typing, feels personalized
> - Changed from 5 screens to 4 screens + activation — fewer steps, stronger finish
> - "Add your first collaborator" (singular) instead of bulk invite — less intimidating

## What Changed & Why

| Change | Before | After | Principle |
|--------|--------|-------|-----------|
| Welcome screen | Generic greeting | Value reminder + time estimate | Users need motivation and expectation-setting |
| Logo upload | Required in step 2 | Removed | Low-value customization delays activation |
| Team invite placement | Step 3 (early) | Step 4 (after project created) | Invite after investment, not before |
| Invite format | Bulk email form | Single email field | Reduce the ask; one person is enough to start |
| Template selection | "Choose a template" | 3 visual cards with social proof | Show, don't tell; validate with usage data |
| Final screen | "You're all set!" | Shows their actual project populated | End on activation, not congratulation |
| Progress indicator | None | Visual progress bar + step count | Reduces abandonment by showing how close they are |

## Measurable Difference

| Metric | Before | After |
|--------|--------|-------|
| Screen count | 5 | 4 + activation |
| Time estimate shown | No | Yes ("2 minutes") |
| Progress indicator | None | Visual bar + step numbers |
| Pre-filled fields | 0 | 1 (workspace name) |
| Social proof elements | 0 | 3 (template usage stats) |
| Skip options | 0 | 2 (customize later, invite later) |
| Activation moment | Generic dashboard | Their actual project with data |
