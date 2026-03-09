# Case Study: Developer CLI Tool First Run

## Context

- **Product**: CLI deployment tool (Vercel/Railway-style)
- **Page/Screen**: Terminal — first run after `npm install -g deploytool`
- **Target Audience**: Developers deploying their first project
- **Agent(s) Used**: Onboarding Flow Designer

## Before (Original Content)

> ```
> $ deploytool init
> Welcome to DeployTool v2.1.0!
> Please enter your API key:
> Please select your cloud provider (AWS/GCP/Azure):
> Please enter your project name:
> Please select your framework (Next.js/Remix/Astro/Other):
> Please enter your build command:
> Please enter your output directory:
> Configuration saved to deploytool.config.json
> Run `deploytool deploy` to deploy your project.
> ```

## After (Agency Output)

> ```
> $ deploytool init
>
> DeployTool v2.1.0
>
> ✓ Detected: Next.js project (from package.json)
> ✓ Build command: next build (auto-detected)
> ✓ Output: .next (auto-detected)
>
> ? Link your account: Press Enter to open browser login
>   (or paste API key with --token flag)
>
> ✓ Authenticated as dev@company.com
>
> ? Project name: my-app (from package.json — press Enter to confirm, or type a new name)
>
> ✓ Project "my-app" created
>
> Ready to deploy! Run:
>   $ deploytool deploy
>
> First deploy takes ~30 seconds. After that, deploys take ~5s.
> ```

> **Key design decisions:**
> - Auto-detect everything possible from the project directory — package.json, framework, build command, output directory
> - Browser-based auth instead of asking for API key — most developers don't have their key handy at first run
> - Pre-fill project name from package.json with confirm-or-override pattern — typing is friction
> - Removed cloud provider selection from init — default to the simplest option, let them change in config later
> - Added time expectation for first deploy — developers want to know the cost before committing
> - Used checkmarks (✓) for completed auto-detection — shows progress without requiring input
> - Kept the flow non-interactive where possible — auto-detected values are stated, not asked

> **Progressive disclosure config:**
> ```
> # deploytool.config.json (auto-generated, minimal)
> {
>   "project": "my-app",
>   "framework": "nextjs"
> }
>
> # User can later add advanced config as needed:
> # provider, region, environment variables, custom domains, etc.
> # deploytool configure --advanced
> ```

## What Changed & Why

| Change | Before | After | Principle |
|--------|--------|-------|-----------|
| Framework detection | Manual selection from list | Auto-detected from package.json | Don't ask what you can infer |
| Build command | Manual entry | Auto-detected | Framework conventions are well-known |
| Authentication | "Enter your API key" | Browser login with Enter key | Keys aren't memorable; browser auth is standard |
| Project name | Manual entry | Pre-filled, confirm or override | Reduce keystrokes; defaults should be smart |
| Cloud provider | Required selection | Removed from init (smart default) | Advanced config shouldn't block getting started |
| Output directory | Manual entry | Auto-detected | Framework determines this |
| Post-init guidance | "Run `deploytool deploy`" | Deploy command + time estimate | Set expectations for next step |
| Questions asked | 6 | 1 (project name confirmation) | Minimize required input |

## Measurable Difference

| Metric | Before | After |
|--------|--------|-------|
| Required inputs | 6 fields | 1 confirmation |
| Auto-detected values | 0 | 4 (framework, build, output, name) |
| Keystrokes to complete | ~80+ characters typed | 1 Enter key (if defaults accepted) |
| Time to completion | ~60 seconds | ~10 seconds |
| Questions asked | 6 sequential prompts | 1 confirmation + 1 auth action |
| Post-setup guidance | Command only | Command + time estimate |
| Config file complexity | Full config up front | Minimal now, `--advanced` later |
