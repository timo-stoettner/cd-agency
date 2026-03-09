# Case Study: SaaS Dashboard Action Buttons

## Context

- **Product**: Analytics dashboard (Mixpanel-style)
- **Page/Screen**: Report builder — multiple action buttons
- **Target Audience**: Product managers and data analysts
- **Agent(s) Used**: Microcopy Review Agent

## Before (Original Content)

> Buttons: "Click Here to Generate Report" | "Submit Query" | "Click to Download as CSV"

## After (Agency Output)

> **Analysis:** All three buttons are verbose and use the anti-pattern "Click here/Click to" which adds no value — users know to click buttons. "Submit Query" uses technical jargon.
>
> **Suggestions:**
> 1. "Generate report" (15 chars) | "Run query" (9 chars) | "Export CSV" (10 chars) [RECOMMENDED]
> 2. "Build report" (12 chars) | "Run" (3 chars) | "Download CSV" (12 chars)
> 3. "Create report" (13 chars) | "Execute" (7 chars) | "Export" (6 chars)
>
> **Rationale:** Removed "Click here/Click to" from all buttons — the button affordance already communicates clickability. Replaced "Submit Query" with "Run query" (friendlier, same meaning). Made all buttons verb-first for consistency. Kept "CSV" since the audience (PMs and analysts) knows the term.

## What Changed & Why

| Change | Before | After | Principle |
|--------|--------|-------|-----------|
| Removed "Click here to" | "Click Here to Generate Report" | "Generate report" | Button affordance communicates clickability |
| Removed "Click to" | "Click to Download as CSV" | "Export CSV" | Same principle — redundant instruction |
| Simplified jargon | "Submit Query" | "Run query" | "Run" is more natural than "Submit" for data queries |
| Consistent case | Mixed: "Click Here to Generate" | Sentence case throughout | Visual consistency across the UI |
| Verb-first pattern | Inconsistent | All start with action verb | Scannable, action-oriented button labels |

## Measurable Difference

| Metric | Before | After |
|--------|--------|-------|
| Total characters (3 buttons) | 69 | 34 |
| Character reduction | — | 51% |
| "Click" occurrences | 2 | 0 |
| Consistent pattern | No | Yes (all verb-first) |
| Avg chars per button | 23 | 11 |
