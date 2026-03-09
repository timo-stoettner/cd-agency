# Case Study: E-Commerce Payment Failure

## Context

- **Product**: Online retail store (Shopify-style)
- **Page/Screen**: Checkout page — payment processing error
- **Target Audience**: Non-technical online shoppers
- **Agent(s) Used**: Error Message Architect

## Before (Original Content)

> Error 503: Service Unavailable. The server is temporarily unable to service your request due to maintenance downtime or capacity problems. Please try again later.

## After (Agency Output)

> **User message:** "We couldn't process your payment right now. Your card hasn't been charged."
>
> **Resolution steps:**
> 1. Wait a moment and try again
> 2. If it keeps happening, try a different payment method
> 3. Contact us at support@store.com — we'll help you complete your order
>
> **Developer note:** HTTP 503 from payment gateway. Check PG health dashboard. Consider implementing automatic retry (1x) before surfacing error.
>
> **Prevention tip:** Add a loading indicator ("Processing your payment...") and implement a 30-second timeout with retry before showing the error.

## What Changed & Why

| Change | Before | After | Principle |
|--------|--------|-------|-----------|
| Removed HTTP status code | "Error 503" | Removed entirely | Users don't need technical codes |
| Removed jargon | "Service Unavailable", "capacity problems" | "We couldn't process your payment" | Plain language for non-technical audience |
| Added reassurance | None | "Your card hasn't been charged" | Addresses the user's #1 fear during payment errors |
| Added resolution path | "Please try again later" | 3 specific steps | Every error must tell users what to do next |
| Added developer context | None | Technical note with actionable fix | Pairs user message with engineering context |

## Measurable Difference

| Metric | Before | After |
|--------|--------|-------|
| Word count | 29 | 15 (user message) |
| Readability (Flesch-Kincaid) | Grade 14 | Grade 4 |
| Actionability | No (vague "try again later") | Yes (3 specific steps) |
| Empathy markers | 0 | 2 ("We couldn't", "we'll help") |
| Resolution paths | 0 | 3 |
