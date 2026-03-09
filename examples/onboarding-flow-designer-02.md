# Case Study: Mobile Banking App First Login

## Context

- **Product**: Digital banking app (Chime-style)
- **Page/Screen**: First login experience after account approval
- **Target Audience**: New banking customers who just completed KYC verification
- **Agent(s) Used**: Onboarding Flow Designer

## Before (Original Content)

> **Screen 1:** "Welcome to QuickBank! Your account is active."
> **Screen 2:** "Set up your PIN for secure access."
> **Screen 3:** "Enable biometric login (Face ID / Fingerprint)."
> **Screen 4:** "Set up direct deposit to start receiving your paycheck."
> **Screen 5:** "Enable push notifications to stay updated on your account activity."
> **Screen 6:** "Explore our features: Savings Goals, Round-ups, Early Pay."
> **Screen 7:** "You're ready! Tap below to go to your account."

## After (Agency Output)

> **Screen 1 — Security setup (required):**
> Headline: "Secure your account"
> Subtext: "Two quick steps before you can use QuickBank"
> Step A: Create 6-digit PIN → Step B: Enable Face ID / Fingerprint
> Both on one screen with inline progression
> CTA: "Continue"
>
> **Screen 2 — Account ready + primary action:**
> Headline: "You're in. Your account is ready."
> Shows: Account number (last 4 digits) + routing number with copy buttons
> Primary CTA: "Set up direct deposit" — with context: "Get paid up to 2 days early"
> Secondary: "I'll do this later"
>
> **Screen 3 — Home screen with contextual nudges:**
> User lands directly on their account home screen
> Empty state card: "Your balance: $0.00 — Set up direct deposit to get started"
> Tooltip on first visit: Points to the "Move Money" tab — "Tap here to add funds"
> Notification permission requested contextually (first transaction triggers the ask, not onboarding)

> **Key design decisions:**
> - Merged PIN + biometrics into one screen — both are security setup, splitting them creates unnecessary friction
> - Removed feature tour entirely — features are discovered through use, not slides
> - Moved notifications out of onboarding — ask when there's a reason ("Want to know when your deposit arrives?")
> - Direct deposit prominently featured — it's the #1 activation metric for banking apps
> - Showed account numbers immediately — users need these to set up direct deposit

## What Changed & Why

| Change | Before | After | Principle |
|--------|--------|-------|-----------|
| Screen count | 7 screens | 2 screens + home | Every screen is a drop-off point — minimize them |
| PIN + biometrics | 2 separate screens | Combined into 1 | Same category (security); no reason to split |
| Feature tour | Dedicated slide | Removed (contextual discovery) | Users don't remember feature tours |
| Notifications | Asked during onboarding | Contextual (at first transaction) | Permission requests need context to convert |
| Direct deposit | One of many setup items | Primary post-security CTA | It's the activation metric — prioritize it |
| Account details | Hidden in settings | Shown immediately | Users need account/routing numbers for direct deposit |
| "Explore features" | Feature carousel | In-app tooltips on first visit | Just-in-time education > front-loaded tours |

## Measurable Difference

| Metric | Before | After |
|--------|--------|-------|
| Onboarding screens | 7 | 2 + contextual home |
| Steps to reach account | 7 taps | 2 taps |
| Required actions | 5 (PIN, biometric, deposit, notifications, feature tour) | 1 (security setup) |
| Time to home screen | ~3 minutes | ~45 seconds |
| Feature tour retention | ~5% recall after 24h (industry avg) | N/A — contextual discovery |
| Notification opt-in timing | No context (onboarding) | High context (first transaction) |
| Direct deposit prominence | 1 of 5 equal options | Primary CTA with value prop |
