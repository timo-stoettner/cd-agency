# Case Study: E-Commerce Product Image Alt Text

## Context

- **Product**: E-commerce marketplace (Etsy-style)
- **Page/Screen**: Product listing page — image gallery
- **Target Audience**: All users, including screen reader users and those on slow connections
- **Agent(s) Used**: Accessibility Content Auditor

## Before (Original Content)

> - Image 1 alt: "product image"
> - Image 2 alt: "IMG_4521.jpg"
> - Image 3 alt: ""  (empty)
> - Image 4 alt: "Handmade ceramic mug blue glaze pottery coffee tea kitchen home decor gift birthday anniversary housewarming artisan craft studio made wheel thrown stoneware food safe dishwasher microwave oven"
> - Image 5 alt: "Click to enlarge"

## After (Agency Output)

> **Audit findings:**
>
> | Image | Issue | Severity | WCAG Criterion |
> |-------|-------|----------|----------------|
> | 1 | Generic alt text — "product image" conveys no information | High | 1.1.1 Non-text Content |
> | 2 | Filename as alt text — meaningless to screen reader users | High | 1.1.1 Non-text Content |
> | 3 | Empty alt on informative image — image is invisible to screen readers | Critical | 1.1.1 Non-text Content |
> | 4 | Keyword-stuffed alt (43 words) — disorienting for screen readers, reads as spam | High | 1.1.1 Non-text Content |
> | 5 | Describes interaction, not content — screen reader user can't decide to "click" without knowing what the image shows | Medium | 1.1.1 Non-text Content |
>
> **Corrected alt text:**
> - Image 1: "Handmade ceramic mug with ocean-blue glaze, 12 oz"
> - Image 2: "Close-up of the mug's interior showing smooth white glaze finish"
> - Image 3: "Side view of the mug showing the attached handle shape"
> - Image 4: "The mug next to a standard coffee cup for size comparison"
> - Image 5: "Mug being held in one hand, showing the ergonomic handle grip"
>
> **Alt text guidelines applied:**
> 1. Describe what's *in* the image, not what the image *is*
> 2. Keep alt text under 125 characters (screen readers truncate beyond this)
> 3. Include product-relevant details (material, color, size) — not SEO keywords
> 4. Each image in a gallery should describe something different
> 5. Never use filenames, "image of", or interaction instructions as alt text

## What Changed & Why

| Change | Before | After | Principle |
|--------|--------|-------|-----------|
| Generic alt | "product image" | Specific description with material + color + size | Alt text replaces the image — it must do the image's job |
| Filename alt | "IMG_4521.jpg" | Describes the image content (interior detail) | Filenames are meaningless to all users |
| Empty alt | "" | Describes the image content (side view) | Empty alt = decorative image. Product images aren't decorative |
| Keyword-stuffed | 43 words of SEO terms | 10 words describing what's shown | Screen readers read alt text linearly — 43 words is exhausting |
| Interaction alt | "Click to enlarge" | Describes image content | Users need to know what's in the image before deciding to interact |

## Measurable Difference

| Metric | Before | After |
|--------|--------|-------|
| WCAG 1.1.1 violations | 5 of 5 images | 0 |
| Average alt text length | 12 chars (excluding keyword-stuffed) | 55 chars |
| Meaningful descriptions | 0 of 5 | 5 of 5 |
| Keyword-stuffed alts | 1 | 0 |
| Screen reader experience | Unusable (no product info conveyed) | Equivalent to sighted experience |
