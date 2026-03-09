# CD Agency: 15 AI Agents That Write Your App's UX Copy So You Don't Have To

*A CLI toolkit for content designers, product teams, and developers who are tired of writing "Something went wrong" for the 47th time.*

---

Writing good UX copy is deceptively hard. Error messages that actually help. Onboarding flows that don't lose people at step 2. Button labels that convert. Notifications that aren't annoying.

Most teams wing it. A developer writes "Invalid input" at 2am, ships it, and nobody touches it again.

**CD Agency** is a Python CLI that gives you 15 specialized AI agents for content design, plus scoring tools, multi-agent workflows, and design system presets — all from the command line.

Here's everything you need to know: what it does, what it can't do, and how to set it up.

---

## What Is CD Agency?

CD Agency is an open-source Python package that bundles:

- **15 AI agents** — each specialized for a specific content design task (error messages, CTAs, onboarding, mobile copy, accessibility audits, etc.)
- **4 scoring tools** — readability, content linting, accessibility checking, and brand voice consistency
- **5 multi-agent workflows** — pipelines that chain agents together for complex tasks like content audits or launch packages
- **4 design system presets** — pre-configured voice profiles for Material Design, Shopify Polaris, Atlassian, and Apple HIG

It runs on the command line. No web UI, no drag-and-drop. Just `cd-agency agent run error -i "your error message"` and you get back a rewritten, human-centered version.

---

## Setting It Up

### Requirements

- Python 3.10+
- An Anthropic API key (for running agents)

### Installation

```bash
pip install cd-agency
```

### Configuration

Set your API key:

```bash
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
```

Optionally, create a `.cd-agency.yaml` in your project root for persistent settings:

```yaml
model: claude-sonnet-4-20250514
default_preset: material-design
brand_voice_guide: presets/material-design.yaml
```

### Tell It About Your Product (New)

This is the part that makes everything 10x more useful. Run:

```bash
cd-agency context init
```

It'll ask you a few questions:

```
Product name: Payroll Pro
What does your product do? Payroll management for small businesses
Domain: fintech
Target audience: small business owners with no accounting background
Tone: professional but friendly, never condescending
Platform: web app
Content guidelines: no jargon, use active voice, assume users are busy
```

This gets saved to `.cd-agency.yaml` and is automatically injected into every agent's prompt. Now when you ask for an error message, the agent knows it's writing for non-technical small business owners in a fintech app — not generic placeholder text.

You can also set individual fields:

```bash
cd-agency context set audience "HR managers at mid-size companies"
cd-agency context show
```

---

## The 15 Agents

Every agent is a specialist. Here's the full roster:

### Writing & Creation

| Agent | What It Does |
|-------|-------------|
| **Content Designer Generalist** | Your all-rounder. Good starting point for any UX writing task. |
| **Error Message Architect** | Writes error messages that explain what happened, why, and how to fix it. |
| **Onboarding Flow Designer** | Designs complete onboarding sequences that drive users to their activation moment. |
| **Notification Content Designer** | Writes notifications across push, email, in-app, and SMS — channel-appropriate. |
| **CTA Optimization Specialist** | Generates 5 CTA variations with conversion psychology principles for each. |
| **Empty State & Placeholder Specialist** | Turns blank screens into guidance opportunities. |
| **Search Experience Writer** | Writes search placeholders, no-results pages, filter labels, and autocomplete hints. |
| **Conversational AI Designer** | Scripts chatbot dialogues, voice UI flows, and IVR trees with branching logic. |

### Review & Optimization

| Agent | What It Does |
|-------|-------------|
| **Microcopy Review Agent** | Takes your existing microcopy and returns 3-5 ranked improvements. |
| **Tone Evaluation Agent** | Scores your content on 5 tone dimensions against your brand voice guide. |
| **Accessibility Content Auditor** | WCAG 2.1 compliance checks — reading level, link text, ALL CAPS, emoji overuse. |
| **Mobile UX Writer** | Rewrites content for mobile constraints — character limits, touch targets, truncation strategies. |

### Specialized Domains

| Agent | What It Does |
|-------|-------------|
| **Technical Documentation Writer** | API docs, SDK guides, developer tutorials with code examples. |
| **Localization Content Strategist** | i18n audits, cultural adaptation flags, translation-ready content prep. |
| **Privacy & Legal Content Simplifier** | Turns dense legal text into plain language without losing legal accuracy. |

### Running an Agent

```bash
# Quick inline input
cd-agency agent run error -i "Error 500: Internal Server Error"

# With specific fields
cd-agency agent run onboarding \
  -F product_description="A time tracking app for freelancers" \
  -F activation_moment="User logs their first hour" \
  -F target_user="freelancers new to time tracking"

# From a file
cd-agency agent run microcopy -f my-button-labels.txt

# Pipe from stdin
echo "Click here to submit" | cd-agency agent run microcopy

# JSON output for automation
cd-agency agent run cta -i "Sign Up" --json-output
```

---

## Scoring Tools (No API Key Needed)

Here's the thing — you don't need an API key for scoring. These run 100% locally:

### Readability

```bash
cd-agency score readability -i "Utilizing our proprietary methodology, we facilitate the optimization of your workflow paradigms."
```

Output: Flesch-Kincaid grade level, reading ease score, word count, reading time. That sentence? Grade 18. Your users left 10 grades ago.

### Content Linting

```bash
cd-agency score lint -i "Please click the button below" --type button
```

Catches: jargon ("leverage", "synergy"), non-inclusive language ("whitelist" → "allowlist"), passive voice, missing action verbs in CTAs, character limit violations.

### Accessibility

```bash
cd-agency score a11y -i "Click here for more info!!!"
```

Flags: "click here" anti-patterns, ALL CAPS, emoji overuse, reading level above Grade 8, color-only indicators. References specific WCAG 2.1 criteria.

### Brand Voice Consistency

```bash
cd-agency score voice -i "Hey! Tap here to get started!" --guide presets/atlassian-design.yaml
```

Scores text 1-10 against a brand voice profile. Works with LLM or in rule-based offline mode (`--no-llm`).

### Score Everything at Once

```bash
cd-agency score all -i "Something went wrong. Please try again later." --json-output
```

---

## Workflows: Chain Agents Together

Single agents are good. Chaining them is better.

CD Agency ships with 5 pre-built workflows:

### 1. Content Audit

Runs 4 agents sequentially: Generalist scan → Tone check → Accessibility audit → Microcopy polish.

```bash
cd-agency workflow run content-audit -F content="Your current copy here"
```

### 2. Error Message Pipeline

Creates a complete error message: Draft → Tone validation → Accessibility check → Mobile variant.

```bash
cd-agency workflow run error-message-pipeline \
  -F error_scenario="Payment failed due to expired card"
```

### 3. Launch Content Package

Runs 3 agents **in parallel** (onboarding + CTAs + empty states), then consolidates with a generalist pass. Produces 10+ content pieces for a feature launch.

```bash
cd-agency workflow run launch-content-package \
  -F product_description="New team collaboration feature"
```

### 4. Localization Prep

i18n audit → Content simplification → Accessibility verification. Gets your content ready for translation.

### 5. Notification Suite

Multi-channel notification copy → Mobile push optimization (120 chars) → Tone consistency → CTA sharpening.

---

## Design System Presets

If your team uses a design system, CD Agency speaks its language:

- **Material Design** — Google's voice: clear, concise, "Sign in" not "Log in", sentence case, no "click"
- **Shopify Polaris** — Merchant-focused: 7th grade reading level, verb+noun buttons, no "simple"/"easy"
- **Atlassian** — Team-oriented: active voice, sentence case, <25 word sentences, "issue" not "ticket"
- **Apple HIG** — Conversational: contractions, "Tap" on iOS, Title Case buttons, "OK" only for acknowledgment

Use them with the voice scorer:

```bash
cd-agency score voice -i "Log into your account" --guide presets/material-design.yaml
# → Flags "Log into" (should be "Sign in to")
```

---

## Project Memory

Agents learn from your past decisions:

```bash
# Store terminology decisions
cd-agency memory add "workspace-vs-project" "Always use 'workspace', never 'project'" --category terminology

# Store voice decisions
cd-agency memory add "formality" "Use contractions, first-person plural" --category voice

# View all stored memory
cd-agency memory show
```

Memory entries are automatically injected into agent prompts. So if you told it once that you call them "workspaces", every agent remembers.

---

## What It Can't Do

Let's be honest about the limitations:

1. **It's a CLI tool.** No GUI, no Figma plugin (yet — there are specs for both in the repo). If your content team doesn't touch the terminal, this isn't for them today.

2. **Agent quality depends on prompts.** The 15 agents are well-tuned, but they're prompt-engineered specialists, not magic. Complex or ambiguous inputs produce variable results.

3. **Agents run sequentially by default.** Parallel execution only happens within workflows that explicitly define parallel groups. Running 5 agents back-to-back takes 5x the time.

4. **You need an API key for agents.** The scoring tools work offline, but the agents need Anthropic's API. That means API costs. A typical agent run uses 150-500 tokens.

5. **Memory is local JSON.** Fine for a single developer or small team. Not a shared database. Not synced across machines.

6. **No real-time collaboration.** It's a local tool. There's no multiplayer mode, no shared workspace, no commenting.

7. **English-first.** The agents work best in English. The localization agent helps prep for translation, but the agents themselves don't write in other languages.

---

## The Export Story

Need to hand off to translators or feed into a CMS?

```bash
# JSON
cd-agency export -i "before text" -o "after text" --format json

# CSV (for spreadsheets)
cd-agency export -i "before text" -o "after text" --format csv

# XLIFF (for translation tools)
cd-agency export -i "before text" -o "after text" --format xliff

# Markdown (for docs)
cd-agency export -i "before text" -o "after text" --format markdown
```

---

## Interactive Mode

Not sure which agent to use? Start here:

```bash
cd-agency interactive
```

It walks you through:
1. What are you working on? (pick from 10 categories)
2. Provides the right agent
3. Collects your inputs
4. Runs the agent
5. Offers to score the output
6. Suggests related agents for follow-up

---

## Quick Start Summary

```bash
# Install
pip install cd-agency
export ANTHROPIC_API_KEY="sk-ant-..."

# Tell it about your product
cd-agency context init

# See what's available
cd-agency agent list

# Run an agent
cd-agency agent run error -i "Error: Operation failed"

# Score content locally (free, no API key)
cd-agency score all -i "Click here to learn more"

# Run a full workflow
cd-agency workflow run content-audit -F content="Your UI copy"

# Store a decision
cd-agency memory add "button-style" "Use verb + noun format" --category pattern
```

---

## Who Is This For?

- **Solo developers** who know their error messages are bad but don't have a content designer on the team
- **Content designers** who want to speed up first drafts and catch inconsistencies
- **Product teams** who want to enforce content quality in CI (there's a GitHub Action)
- **Design system teams** who want to lint copy against their voice guide
- **Anyone** who's ever shipped "Something went wrong. Please try again." and felt a little guilty about it

---

The full source is on GitHub. It's 15 agents, 226+ tests, 5 workflows, and a CLI that actually makes UX copy less painful.

Give it a try: `pip install cd-agency`
