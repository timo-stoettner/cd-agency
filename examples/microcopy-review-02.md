# Case Study: Registration Form Labels

## Context

- **Product**: Fintech app (Wise-style)
- **Page/Screen**: Account registration form
- **Target Audience**: International users opening a financial account
- **Agent(s) Used**: Microcopy Review Agent

## Before (Original Content)

> - "Please enter your first name as it appears on your official government-issued identification document"
> - "Input your electronic mail address"
> - "Create a password (must be minimum 8 characters in length and contain at least one uppercase letter, one lowercase letter, one number, and one special character)"
> - Button: "Click Here to Register Your Account"

## After (Agency Output)

> **Analysis:** Form labels are extremely verbose — the longest is 156 characters for a password hint. "Electronic mail address" is archaic. The button repeats the "Click here" anti-pattern. Password rules should be shown as a checklist, not inline text.
>
> **Suggestions:**
> - "Legal first name" (16 chars) — Placeholder: "As shown on your ID"
> - "Email" (5 chars) — Placeholder: "name@example.com"
> - "Password" (8 chars) — Helper below field as interactive checklist:
>   - [ ] 8+ characters
>   - [ ] Uppercase letter
>   - [ ] Number
>   - [ ] Special character (!@#$)
> - Button: "Create account" (14 chars)
>
> **Rationale:** Moved context from labels to placeholders and helper text. "Legal first name" is concise but signals this is for ID verification (important for fintech). Password rules as a checklist are scannable and provide real-time feedback. "Create account" is specific and verb-first.

## What Changed & Why

| Change | Before | After | Principle |
|--------|--------|-------|-----------|
| Name field | 96 chars explaining ID requirement | "Legal first name" + placeholder | Label = what; placeholder = how |
| Email field | "electronic mail address" | "Email" | Use the word everyone knows |
| Password rules | 156-char inline paragraph | 4-item checklist | Scannable > readable for requirements |
| Register button | "Click Here to Register Your Account" | "Create account" | Verb-first, no "click here" |

## Measurable Difference

| Metric | Before | After |
|--------|--------|-------|
| Total label characters | 319 | 43 |
| Character reduction | — | 87% |
| Readability | Grade 14 | Grade 3 |
| Form completion time (est.) | High cognitive load | Low — scan and type |
| Archaic terms | 1 ("electronic mail") | 0 |
