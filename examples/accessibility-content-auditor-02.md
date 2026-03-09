# Case Study: Dashboard Data Visualization

## Context

- **Product**: Analytics dashboard (Datadog-style)
- **Page/Screen**: Main dashboard — charts and status indicators
- **Target Audience**: DevOps engineers monitoring system health, including those with color vision deficiency
- **Agent(s) Used**: Accessibility Content Auditor

## Before (Original Content)

> - Status indicators: Red circle = down, Yellow circle = degraded, Green circle = healthy
> - Chart legend: Red line = errors, Green line = success, Orange line = warnings
> - Alert banner: Red background with white text: "Critical: 3 services down"
> - Tooltip on hover: "CPU: 87% — High" (only appears on mouse hover)
> - Table header sorting: Small triangle icon changes direction (no text label)

## After (Agency Output)

> **Audit findings:**
>
> | Element | Issue | Severity | WCAG Criterion |
> |---------|-------|----------|----------------|
> | Status indicators | Color-only encoding — red/yellow/green indistinguishable for ~8% of male users | Critical | 1.4.1 Use of Color |
> | Chart legend | Same color-only issue — error/success/warning lines rely on red vs green | Critical | 1.4.1 Use of Color |
> | Alert banner | Red bg + white text may not meet 4.5:1 contrast ratio | High | 1.4.3 Contrast (Minimum) |
> | Tooltips | Hover-only content inaccessible to keyboard and touch users | High | 1.4.13 Content on Hover or Focus |
> | Sort indicators | Icon-only — no text alternative, no aria-label | Medium | 1.3.1 Info and Relationships |
>
> **Corrected content:**
>
> **Status indicators:**
> - ● Down (with "Down" text label + `aria-label="Service status: down"`)
> - ▲ Degraded (with "Degraded" text label + `aria-label="Service status: degraded"`)
> - ✓ Healthy (with "Healthy" text label + `aria-label="Service status: healthy"`)
> - Each uses a distinct shape + text, not just color
>
> **Chart legend:**
> - Errors: red dashed line (──  ──) + label "Errors"
> - Success: green solid line (────) + label "Success"
> - Warnings: orange dotted line (· · · ·) + label "Warnings"
> - Line patterns distinguish data series without color
>
> **Alert banner:**
> - Background: #B91C1C (darker red) with white text — 5.2:1 contrast ratio
> - Added icon: ⚠ before text
> - Added `role="alert"` for screen reader announcement
> - Text: "⚠ Critical: 3 services are down — View affected services"
>
> **Data values:**
> - Visible on focus (keyboard) and hover (mouse)
> - Touch: tap to reveal, tap elsewhere to dismiss
> - Always-visible for critical thresholds (>80% CPU always shows inline)
>
> **Sort indicators:**
> - "Name ↑ (sorted ascending)" — visible text + `aria-sort="ascending"`
> - Click target is the full header cell, not just the icon

## What Changed & Why

| Change | Before | After | Principle |
|--------|--------|-------|-----------|
| Status encoding | Color only (red/yellow/green) | Color + shape + text label | Never use color as the sole indicator |
| Chart lines | Color-differentiated only | Color + line pattern (solid/dashed/dotted) | Patterns are distinguishable without color |
| Alert contrast | Red bg (#EF4444) + white text (3.1:1) | Darker red (#B91C1C) + white (5.2:1) | WCAG AA requires 4.5:1 for normal text |
| Tooltips | Hover-only | Hover + focus + tap | All interaction methods must access the same content |
| Sort headers | Icon-only triangle | Text label + aria-sort attribute | State must be programmatically determinable |

## Measurable Difference

| Metric | Before | After |
|--------|--------|-------|
| WCAG violations | 5 | 0 |
| Color-only indicators | 3 (status, chart, alert) | 0 (all have redundant encoding) |
| Contrast ratio (alert) | 3.1:1 (fail AA) | 5.2:1 (pass AA) |
| Keyboard-accessible content | Partial (tooltips hidden) | Full |
| Screen reader support | Minimal (no roles/labels) | Full (aria-label, aria-sort, role=alert) |
| Color-blind accessible | No | Yes (shapes + patterns + text) |
