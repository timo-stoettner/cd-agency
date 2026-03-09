# Case Study: Full Content Audit Workflow

## Context

- **Product**: Healthcare SaaS (Zocdoc-style)
- **Page/Screen**: Patient-facing appointment confirmation page
- **Target Audience**: Patients who just booked an appointment
- **Workflow Used**: `content-audit.yaml` (4-step pipeline)
- **Agents Used**: Content Design Generalist → Tone & Voice Calibrator → Accessibility Content Auditor → Microcopy Review Agent

## Original Content

> **Heading:** "Appointment Confirmation"
> **Body:** "Your appointment has been successfully submitted for processing. You will receive a confirmation email at the email address associated with your account within 24-48 business hours. Please note that this appointment is pending and subject to provider availability. If you need to cancel or reschedule, please contact our support team at 1-800-555-0199 during business hours (Monday-Friday, 9am-5pm EST). Thank you for choosing HealthFirst."

## Workflow Pipeline Results

### Step 1: Content Design Generalist — Structural Analysis

> **Assessment:** The page buries critical information (is the appointment confirmed or pending?) in a wall of text. The user's #1 question — "Am I booked?" — isn't clearly answered. Contact information is the most prominent actionable element, but users shouldn't need to call to manage their appointment.
>
> **Recommended structure:**
> 1. Clear confirmation status (confirmed vs pending — pick one)
> 2. Appointment details (date, time, provider, location)
> 3. Next steps (what to do before the appointment)
> 4. Self-service management (reschedule/cancel without calling)

### Step 2: Tone & Voice Calibrator — Tone Adjustment

> **Tone audit:** Current tone is corporate-legal ("submitted for processing", "subject to provider availability", "associated with your account"). This is a moment of relief for the patient — they should feel reassured, not like they're reading a contract.
>
> **Calibrated tone:** Warm, clear, reassuring. Short sentences. Direct address ("you/your").
>
> **Rewritten:**
> "You're booked with Dr. Sarah Chen on Tuesday, March 17 at 2:30 PM.
> We sent a confirmation to jamie@email.com.
> Need to reschedule? You can change your appointment anytime from your dashboard."

### Step 3: Accessibility Content Auditor — A11y Review

> **Findings:**
> - Phone number (1-800-555-0199) should use `tel:` link for assistive technology and mobile
> - Time zone abbreviation "EST" should be spelled out on first use: "Eastern Time (ET)"
> - Confirmation status needs `role="status"` for screen reader announcement
> - Color of success state must not rely on green alone — add checkmark icon + text
>
> **Applied corrections to Step 2 output:**
> - Added ✓ icon before confirmation text
> - Changed "EST" → "Eastern Time"
> - Noted `role="status"` and `tel:` link requirements

### Step 4: Microcopy Review Agent — Final Polish

> **Final output:**
>
> **✓ You're booked**
>
> **Dr. Sarah Chen**
> Tuesday, March 17 · 2:30 PM Eastern Time
> HealthFirst Clinic — 123 Main St, Suite 200
>
> Confirmation sent to jamie@email.com
>
> **Before your visit:**
> - Arrive 15 minutes early for check-in
> - Bring your insurance card and photo ID
> - [Complete intake forms online](link) (saves ~10 min at the office)
>
> **Need to change this?**
> [Reschedule](link) · [Cancel appointment](link)
>
> Questions? [Call 1-800-555-0199](tel:18005550199) — available Mon–Fri, 9 AM – 5 PM Eastern Time

## Pipeline Transformation Summary

| Aspect | Original | After 4-Agent Pipeline |
|--------|----------|----------------------|
| Word count | 74 words (dense paragraph) | 62 words (structured sections) |
| Primary question answered | Ambiguous ("pending" vs "confirmed") | Immediately ("You're booked") |
| Appointment details shown | None | Full (provider, date, time, location) |
| Tone | Corporate-legal | Warm, direct, reassuring |
| Self-service options | 0 (must call to change) | 2 (reschedule + cancel links) |
| Accessibility issues | 3 (no tel: link, EST abbreviation, color-only status) | 0 |
| Actionable next steps | 0 | 3 (arrive early, bring docs, intake forms) |
| Readability grade | Grade 14 | Grade 5 |

## Why the Multi-Agent Pipeline Matters

Each agent caught something the others didn't:

1. **Generalist** identified the structural problem — information hierarchy was wrong
2. **Tone Calibrator** fixed the emotional mismatch — corporate language at a relief moment
3. **Accessibility Auditor** caught technical a11y issues — `tel:` links, abbreviations, ARIA roles
4. **Microcopy Reviewer** tightened the final copy — every word earns its place

A single pass would have caught maybe 2 of these 4 layers. The pipeline ensures comprehensive coverage.
