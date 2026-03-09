# Case Study: Social Platform Permission Denied

## Context

- **Product**: Social media platform (Mastodon-style)
- **Page/Screen**: Post creation — attempting to post in a moderated group
- **Target Audience**: General consumers, community members
- **Agent(s) Used**: Error Message Architect

## Before (Original Content)

> 403 Forbidden. You do not have the required permissions to perform this action. Contact your administrator.

## After (Agency Output)

> **User message:** "You can't post in this group yet. New members can post after being approved by a moderator."
>
> **Resolution steps:**
> 1. Check your group membership status in Settings → Groups
> 2. If you recently joined, a moderator will review your request — usually within 24 hours
> 3. In the meantime, you can post in public groups or on your own profile
>
> **Developer note:** HTTP 403 — user role `pending_member` attempted `create_post` in group with `moderated` policy. Check `group_memberships` table for approval_status.
>
> **Prevention tip:** Disable the "Post" button for pending members and show an inline note: "Your membership is pending approval. You'll be able to post once approved."

## What Changed & Why

| Change | Before | After | Principle |
|--------|--------|-------|-----------|
| Removed HTTP code | "403 Forbidden" | Removed | Technical codes are meaningless to users |
| Explained *why* | "do not have the required permissions" | "New members can post after being approved" | Tell users the reason, not just the status |
| Replaced "administrator" | "Contact your administrator" | "a moderator will review" | Use terms the user actually knows |
| Added alternative actions | None | "post in public groups or on your own profile" | Don't block users — redirect them |
| Prevention | None | Disable button + inline note | Prevent the frustrating attempt entirely |

## Measurable Difference

| Metric | Before | After |
|--------|--------|-------|
| Word count | 16 | 18 (user message) |
| Readability (Flesch-Kincaid) | Grade 12 | Grade 6 |
| Jargon terms | 3 ("403", "permissions", "administrator") | 0 |
| Actionability | No (who is "administrator"?) | Yes (3 steps + alternatives) |
| Empathy markers | 0 | 1 ("yet" implies it's temporary) |
