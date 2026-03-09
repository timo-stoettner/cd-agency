# Case Study: Healthcare Patient Portal Forms

## Context

- **Product**: Healthcare patient portal (MyChart-style)
- **Page/Screen**: Appointment booking form + confirmation
- **Target Audience**: Patients of all ages and abilities, including elderly users and those using assistive technology
- **Agent(s) Used**: Accessibility Content Auditor

## Before (Original Content)

> - Form title: "SCHEDULE YOUR APPOINTMENT"
> - Required field indicator: Fields marked with * (no legend explaining what * means)
> - Date picker: Custom JavaScript calendar widget (not keyboard navigable)
> - Error message: Fields turn red border with no text explanation
> - Confirmation: "Your appointment has been successfully scheduled! ✓" (green text on white background)
> - Timeout warning: None — form silently expires after 15 minutes and data is lost

## After (Agency Output)

> **Audit findings:**
>
> | Element | Issue | Severity | WCAG Criterion |
> |---------|-------|----------|----------------|
> | ALL CAPS title | Harder to read; screen readers may spell out letter-by-letter | Medium | 1.3.1 Info and Relationships |
> | Asterisk convention | No legend explains what * means; assumes visual convention knowledge | High | 3.3.2 Labels or Instructions |
> | Date picker | Keyboard trap — Tab key doesn't move focus out of widget | Critical | 2.1.2 No Keyboard Trap |
> | Error indication | Color-only (red border) — no text, no aria-invalid | Critical | 3.3.1 Error Identification |
> | Confirmation text | Green (#22C55E) on white = 2.1:1 contrast ratio | High | 1.4.3 Contrast (Minimum) |
> | Session timeout | No warning before data loss | Critical | 2.2.1 Timing Adjustable |
>
> **Corrected content:**
>
> **Form title:**
> "Schedule your appointment" (sentence case)
> Subtext: "Required fields are marked with (required)" — using the word, not just *
>
> **Required fields:**
> - Label: "Appointment date (required)" — explicit text, not just asterisk
> - `aria-required="true"` on each required input
>
> **Date picker:**
> - Use native `<input type="date">` as base (keyboard accessible by default)
> - Enhanced widget: Arrow keys navigate days, Escape closes, Tab moves to next field
> - Format hint below field: "Example: 03/15/2026"
>
> **Error messages:**
> - Red border retained + error icon + text message below the field
> - "Please select an appointment date" (specific to the field)
> - `aria-invalid="true"` + `aria-describedby` pointing to error message
> - Error summary at top of form: "2 items need your attention" with links to each field
>
> **Confirmation:**
> - Text color: #15803D (dark green) on white = 4.8:1 contrast ratio
> - "Your appointment is confirmed" — added `role="status"` for screen reader announcement
> - Details shown: Date, time, provider, location — not just a success message
> - "Add to calendar" link + "What to bring" checklist
>
> **Session timeout:**
> - Warning at 12 minutes: "Your session will expire in 3 minutes. Need more time?"
> - CTA: "Extend session" (resets to 15 minutes)
> - Data saved to sessionStorage as user types — recoverable on refresh
> - `role="alert"` on timeout warning for screen reader announcement

## What Changed & Why

| Change | Before | After | Principle |
|--------|--------|-------|-----------|
| ALL CAPS title | "SCHEDULE YOUR APPOINTMENT" | "Schedule your appointment" | Sentence case is 13% faster to read; some screen readers spell ALL CAPS |
| Required indicator | * with no legend | "(required)" text on each field | Explicit > symbolic; don't assume convention knowledge |
| Date picker | Custom widget, keyboard trap | Native input enhanced with keyboard support | Never trap keyboard focus |
| Error feedback | Red border only | Border + icon + text + aria-invalid + summary | Errors must be identified in text, not just visually |
| Confirmation color | Green #22C55E (2.1:1 contrast) | Dark green #15803D (4.8:1 contrast) | Text must meet 4.5:1 minimum contrast |
| Session timeout | Silent expiration | Warning + extend option + data persistence | Users must be warned and given control over time limits |

## Measurable Difference

| Metric | Before | After |
|--------|--------|-------|
| WCAG violations | 6 | 0 |
| Critical violations | 3 (keyboard trap, error ID, timeout) | 0 |
| Keyboard navigable | No (date picker trap) | Yes (full keyboard support) |
| Error message text | 0 (color-only) | Specific message per field + summary |
| Contrast ratio (confirmation) | 2.1:1 (fail AA) | 4.8:1 (pass AA) |
| Session timeout handling | None (data lost) | Warning + extend + data persistence |
| ARIA attributes used | 0 | 5 (required, invalid, describedby, role, alert) |
