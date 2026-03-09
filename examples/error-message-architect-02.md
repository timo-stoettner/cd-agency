# Case Study: SaaS File Upload Failure

## Context

- **Product**: Project management SaaS (Notion-style)
- **Page/Screen**: Document editor — file attachment upload
- **Target Audience**: Knowledge workers, mixed technical levels
- **Agent(s) Used**: Error Message Architect

## Before (Original Content)

> Upload failed. File too large. Maximum file size exceeded. (ERR_FILE_SIZE_LIMIT)

## After (Agency Output)

> **User message:** "This file is too large to upload. The maximum size is 25 MB."
>
> **Resolution steps:**
> 1. Compress the file or reduce its resolution
> 2. Split it into smaller files if possible
> 3. For larger files, paste a link from Google Drive, Dropbox, or OneDrive instead
>
> **Developer note:** Client-side validation: file.size > 25MB (26,214,400 bytes). No API call made. Log file type and size for capacity planning.
>
> **Prevention tip:** Show the file size limit near the upload button before the user attempts to upload. Consider adding a progress bar that validates size before upload begins.

## What Changed & Why

| Change | Before | After | Principle |
|--------|--------|-------|-----------|
| Added the actual limit | "Maximum file size exceeded" | "maximum size is 25 MB" | Be specific — don't make users guess the limit |
| Removed error code | "(ERR_FILE_SIZE_LIMIT)" | Removed | Internal codes confuse non-technical users |
| Removed redundancy | "Upload failed. File too large. Maximum file size exceeded." (3 ways to say the same thing) | Single clear sentence | Say it once, say it well |
| Added workarounds | None | 3 alternatives including cloud link | Give users a path forward, not just a wall |
| Prevention guidance | None | Show limit before upload | Best error message is the one you never show |

## Measurable Difference

| Metric | Before | After |
|--------|--------|-------|
| Word count | 12 | 14 (user message) |
| Redundant statements | 3 | 0 |
| Readability (Flesch-Kincaid) | Grade 8 | Grade 5 |
| Actionability | No | Yes (3 steps + prevention) |
| Specific details | 0 (no size limit shown) | 1 (25 MB stated) |
