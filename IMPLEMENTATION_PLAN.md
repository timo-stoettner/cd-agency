# Content Design Agency - Implementation Plan

> From blueprint to building: A phased roadmap to take this agency from 70 to 10,000.

---

## Phase 1: Foundation & Structure (Quick Wins)
**Goal**: Fix what exists before building what's missing. Clean up overlaps, add structure, and make the current agents more usable.
**Estimated effort**: 1-2 days
**Impact**: Makes the repo immediately more professional and navigable.

### 1.1 Create Decision Tree (`WHEN_TO_USE.md`)
> **~30 min** | Resolves agent overlap confusion

- [ ] Map every common content design task to the correct agent
- [ ] Create a flowchart-style decision tree:
  - "Writing error messages?" → Error Message Architect
  - "Reviewing existing microcopy?" → Microcopy Review Agent
  - "Need a full content audit?" → Start with Generalist → route to specialists
- [ ] Add a "Quick Reference Matrix" table: Task × Agent with checkmarks
- [ ] Define when to use Generalist vs. Specialist (the #1 confusion point)
- [ ] Add cross-references: "If this agent's output needs tone checking, hand off to Tone Evaluation Agent"

### 1.2 Add Structured Frontmatter to All 15 Agent Files
> **~45 min** | Makes agents machine-parseable and integration-ready

For each of the 15 agent `.md` files, add to the YAML frontmatter:
- [ ] `inputs`: list of expected input fields with types (string, file, url)
- [ ] `outputs`: list of deliverable fields with types and formats
- [ ] `related_agents`: list of agents that commonly precede or follow this one
- [ ] `difficulty_level`: beginner | intermediate | advanced
- [ ] `tags`: searchable keywords (e.g., `["microcopy", "buttons", "forms"]`)
- [ ] `version`: semantic version starting at `1.0.0`

**Files to update** (all 15):
1. `content-designer-generalist.md`
2. `conversational-ai-designer.md`
3. `accessibility-content-auditor.md`
4. `microcopy-review-agent.md`
5. `tone-evaluation-agent.md`
6. `onboarding-flow-designer.md`
7. `technical-documentation-writer.md`
8. `cta-optimization-specialist.md`
9. `error-message-architect.md`
10. `mobile-ux-writer.md`
11. `localization-content-strategist.md`
12. `notification-content-designer.md`
13. `privacy-legal-content-simplifier.md`
14. `empty-state-placeholder-specialist.md`
15. `search-experience-writer.md`

### 1.3 Rewrite Personality Sections into Effective System Prompts
> **~60 min** | Turns fluffy bios into engineering that actually changes LLM behavior

For each agent, replace the "Identity & Personality" section with:
- [ ] A concise system prompt instruction (2-3 sentences max)
- [ ] 2-3 few-shot examples showing ideal input → output pairs
- [ ] Output format specification (markdown, JSON, table, etc.)
- [ ] Temperature/style guidance (e.g., "be direct, no filler, bullet points preferred")
- [ ] Explicit constraints (max word counts, forbidden patterns)

### 1.4 Create Project Scaffolding
> **~20 min** | Sets up the directory structure for everything that follows

- [ ] Create directory structure:
  ```
  cd-agency/
  ├── content-design/          # (existing) agent definitions
  ├── examples/                # before/after case studies
  ├── workflows/               # multi-agent pipeline definitions
  ├── runtime/                 # execution engine (Phase 2)
  ├── tools/                   # evaluation & scoring (Phase 5)
  ├── docs/                    # documentation
  │   └── WHEN_TO_USE.md
  ├── IMPLEMENTATION_PLAN.md   # this file
  ├── ROADMAP.md               # public-facing roadmap
  └── README.md                # (existing) updated
  ```
- [ ] Create `ROADMAP.md` - public-facing version of this plan (high-level, no implementation details)
- [ ] Update `README.md` to reference new structure and roadmap

---

### Phase 1 Summary Checkpoint
**What was accomplished:**
- Agent overlap resolved with decision tree and cross-references
- All 15 agents have structured, machine-parseable frontmatter (inputs/outputs/relations)
- Personality fluff replaced with real system prompt engineering + few-shot examples
- Directory structure scaffolded for all future phases
- Public roadmap signals ambition to contributors

**What this enables:**
- Phase 2 can parse agent files programmatically (structured frontmatter)
- Phase 3 can build workflows using `related_agents` fields
- Phase 4 can use few-shot examples as starting points for case studies

---

## Phase 2: Runtime & Execution Layer
**Goal**: Make agents executable. Turn markdown specs into working AI agents that accept input and produce output.
**Estimated effort**: 3-5 days
**Impact**: Transforms the project from a prompt library into a functional tool.

### 2.1 Set Up Python Project
> **~30 min** | Bootstrap the codebase

- [ ] Create `pyproject.toml` with project metadata, dependencies:
  - `anthropic` (Claude API SDK)
  - `pyyaml` (parse agent frontmatter)
  - `rich` (terminal output formatting)
  - `click` (CLI framework)
  - `pydantic` (input/output validation)
- [ ] Create `runtime/__init__.py`
- [ ] Create `runtime/agent.py` - core Agent class
- [ ] Create `runtime/loader.py` - loads `.md` files into Agent objects
- [ ] Create `runtime/config.py` - API keys, model selection, defaults
- [ ] Add `.env.example` with required environment variables
- [ ] Add `runtime/` to `.gitignore` for any local config

### 2.2 Build the Agent Loader
> **~45 min** | Parses markdown agent files into executable objects

- [ ] Parse YAML frontmatter from each `.md` file
- [ ] Extract sections (Identity, Core Mission, Critical Rules, Deliverables, Workflow, Metrics)
- [ ] Build system prompt from parsed sections:
  - Core Mission → opening instruction
  - Critical Rules → numbered constraints
  - Few-shot examples → appended as demonstrations
  - Output format → closing instruction
- [ ] Validate inputs/outputs against Pydantic schemas derived from frontmatter
- [ ] Return a ready-to-execute `Agent` object with `.run(input)` method

### 2.3 Build the Agent Runner
> **~60 min** | The core execution engine

- [ ] Create `Agent.run(input: dict) -> AgentOutput` method
- [ ] Compose the full prompt: system prompt + user input + output format instructions
- [ ] Call Claude API (or configurable LLM backend)
- [ ] Parse response into structured `AgentOutput` (matches defined output schema)
- [ ] Handle errors: API failures, malformed responses, timeout
- [ ] Add retry logic with exponential backoff
- [ ] Add logging: input, output, token usage, latency
- [ ] Support streaming output for long-form content generation

### 2.4 Build Input/Output Validation
> **~30 min** | Ensures agents receive correct data and return structured results

- [ ] Generate Pydantic models from agent frontmatter `inputs`/`outputs`
- [ ] Validate user input before sending to LLM
- [ ] Validate LLM output against expected schema
- [ ] Provide clear error messages when validation fails
- [ ] Support optional fields with sensible defaults

### 2.5 Add Agent Registry
> **~20 min** | Central lookup for all available agents

- [ ] Auto-discover all `.md` files in `content-design/` directory
- [ ] Build registry mapping agent names to loaded Agent objects
- [ ] Support aliases (e.g., "error" → "error-message-architect")
- [ ] List available agents with descriptions
- [ ] Support filtering by tags, difficulty, or related agents

### 2.6 Write Unit Tests for Runtime
> **~45 min** | Ensure reliability

- [ ] Test agent loader: correctly parses all 15 agent files
- [ ] Test input validation: rejects bad input, accepts good input
- [ ] Test output parsing: handles structured and unstructured LLM responses
- [ ] Test registry: finds agents by name, alias, tag
- [ ] Test error handling: API timeout, malformed response, missing fields
- [ ] Mock LLM calls for fast, deterministic testing

---

### Phase 2 Summary Checkpoint
**What was accomplished:**
- Python project bootstrapped with dependencies and structure
- Agent loader parses all 15 `.md` files into executable Agent objects
- Agent runner calls Claude API with composed prompts and returns structured output
- Input/output validation ensures data integrity
- Agent registry provides central lookup with aliases and filtering
- Unit tests cover core functionality

**What this enables:**
- Phase 3 can chain agents together (each agent has `.run()`)
- Phase 6 can wrap the runtime in a CLI
- Any developer can now `pip install` and programmatically use agents

---

## Phase 3: Multi-Agent Workflows & Orchestration
**Goal**: Enable agents to work together in pipelines. Content design is collaborative -- agents should be too.
**Estimated effort**: 2-3 days
**Impact**: Unlocks the real value of having multiple specialized agents.

### 3.1 Define Workflow Schema
> **~30 min** | Standard format for multi-agent pipelines

- [ ] Create `workflows/schema.yaml` defining workflow structure:
  ```yaml
  name: string
  description: string
  steps:
    - agent: agent-name
      input_map: {agent_field: source}  # maps workflow input or previous step output
      output_key: string                # name this step's output for later reference
      parallel: bool                    # can run alongside other parallel steps
      condition: string                 # optional: only run if condition met
  ```
- [ ] Support sequential steps (output of A feeds into B)
- [ ] Support parallel steps (A and B run simultaneously, C merges results)
- [ ] Support conditional steps (only run agent if previous output meets criteria)

### 3.2 Build Workflow Engine
> **~90 min** | Executes multi-agent pipelines

- [ ] Create `runtime/workflow.py`
- [ ] Parse workflow YAML files into executable pipeline objects
- [ ] Implement sequential execution: pass output of step N as input to step N+1
- [ ] Implement parallel execution: run independent steps concurrently (asyncio)
- [ ] Implement conditional execution: evaluate conditions against step outputs
- [ ] Handle intermediate state: store each step's output for later reference
- [ ] Add workflow-level error handling: retry failed steps, skip optional steps
- [ ] Log full workflow execution trace (every step's input/output)

### 3.3 Create Core Workflows
> **~60 min** | The 5 most valuable multi-agent pipelines

**Workflow 1: Full Content Audit**
- [ ] Define: Generalist scans → Tone Evaluator checks voice → Accessibility Auditor flags issues → Microcopy Reviewer polishes
- [ ] Each step receives original content + all previous step outputs
- [ ] Final output: consolidated audit report with prioritized recommendations

**Workflow 2: Error Message Pipeline**
- [ ] Define: Error Architect drafts → Tone Agent validates tone → Accessibility Auditor checks → Mobile UX Writer creates mobile variant
- [ ] Input: error code, context, severity, target platform
- [ ] Output: desktop message, mobile message, developer notes, resolution steps

**Workflow 3: Launch Content Package**
- [ ] Define: Onboarding Designer + CTA Specialist + Empty State Specialist run in parallel → Generalist consolidates and harmonizes
- [ ] Input: product description, target audience, key features
- [ ] Output: complete content package (onboarding flow, CTAs, empty states, all consistent in voice)

**Workflow 4: Localization Prep**
- [ ] Define: Localization Strategist audits → Generalist simplifies flagged content → Accessibility Auditor validates
- [ ] Input: content bundle, target locales
- [ ] Output: localization-ready content + glossary + i18n issue report

**Workflow 5: Notification Suite**
- [ ] Define: Notification Designer drafts → Mobile UX Writer optimizes for mobile → Tone Agent ensures consistency → CTA Specialist sharpens actions
- [ ] Input: notification triggers, channels, user segments
- [ ] Output: push, in-app, and email variants for each notification

### 3.4 Write Integration Tests for Workflows
> **~30 min** | Verify pipelines work end-to-end

- [ ] Test sequential workflow: output flows correctly between steps
- [ ] Test parallel workflow: steps run concurrently, results merge correctly
- [ ] Test conditional workflow: steps skipped/included based on conditions
- [ ] Test error recovery: workflow handles a failed step gracefully
- [ ] End-to-end test with mocked LLM: run full "Content Audit" workflow

---

### Phase 3 Summary Checkpoint
**What was accomplished:**
- Workflow schema defined supporting sequential, parallel, and conditional steps
- Workflow engine executes multi-agent pipelines with state management
- 5 core workflows built: Content Audit, Error Pipeline, Launch Package, Localization Prep, Notification Suite
- Integration tests verify pipeline correctness

**What this enables:**
- Phase 6 CLI can expose workflows as single commands
- Phase 7 integrations can trigger workflows from external tools
- Users get real, compound value from the agent collection

---

## Phase 4: Proof & Portfolio (Before/After Examples)
**Goal**: Build undeniable proof that the agency produces better content. No examples = no trust.
**Estimated effort**: 2-3 days
**Impact**: Critical for adoption. This is what people share and link to.

### 4.1 Select 10 Real Products for Case Studies
> **~30 min** | Choose diverse, recognizable products

- [ ] Pick 10 open-source or well-known products with publicly visible UI content:
  1. A developer tool (e.g., VS Code, GitHub)
  2. An e-commerce platform (e.g., Shopify storefront)
  3. A SaaS dashboard (e.g., Notion, Linear)
  4. A mobile app (e.g., a popular open-source app)
  5. A documentation site (e.g., MDN, Stripe docs)
  6. A form-heavy product (e.g., tax software, registration flows)
  7. A social platform (e.g., Mastodon)
  8. A productivity tool (e.g., Todoist, Cal.com)
  9. A fintech product (e.g., open banking UI)
  10. A healthcare or government service

### 4.2 Create Before/After Case Study Template
> **~20 min** | Standardize how examples are presented

- [ ] Create `examples/TEMPLATE.md` with structure:
  ```markdown
  # Case Study: [Product Name]
  ## Context
  Product, page/screen, target audience
  ## Before (Original Content)
  Screenshot or text of current content
  ## Agent(s) Used
  Which agents, in what order
  ## After (Agency Output)
  The improved content
  ## What Changed & Why
  Specific improvements with rationale
  ## Measurable Difference
  Readability score, word count, clarity metrics
  ```

### 4.3 Generate 3 Case Studies Per Key Agent (Top 5 Agents)
> **~3-4 hours** | The core proof portfolio

For each of the top 5 agents, produce 3 case studies:
- [ ] **Error Message Architect** (3 case studies)
  - Real error messages from selected products → improved versions
  - Include: original, rewrite, readability scores, resolution path added
- [ ] **Microcopy Review Agent** (3 case studies)
  - Real button labels, tooltips, form fields → refined versions
  - Include: original, A/B variant suggestions, character count optimization
- [ ] **CTA Optimization Specialist** (3 case studies)
  - Real CTAs from landing pages → optimized with rationale
  - Include: original, 3 variations, psychological principle behind each
- [ ] **Onboarding Flow Designer** (3 case studies)
  - Real onboarding screens → redesigned flow content
  - Include: original steps, redesigned steps, progressive disclosure applied
- [ ] **Accessibility Content Auditor** (3 case studies)
  - Real content with accessibility issues → remediated versions
  - Include: WCAG violations found, plain language rewrites, alt text suggestions

### 4.4 Create 2 Full Workflow Case Studies
> **~2 hours** | Show the power of multi-agent pipelines

- [ ] **Case Study: "Full Content Audit"** on a real product page
  - Show each agent's contribution in sequence
  - Consolidated before/after with all improvements layered
- [ ] **Case Study: "Launch Content Package"** for a hypothetical product
  - Show parallel agent outputs merging into cohesive content
  - Demonstrate voice consistency across onboarding + CTAs + empty states

### 4.5 Add Examples to README
> **~15 min** | Surface the proof

- [ ] Add "See It In Action" section to README.md
- [ ] Link to top 3 most compelling case studies
- [ ] Add before/after comparison snippet directly in README (most impactful one)

---

### Phase 4 Summary Checkpoint
**What was accomplished:**
- 10 real products selected as case study targets
- Standardized case study template created
- 15 individual agent case studies produced (3 each for top 5 agents)
- 2 full workflow case studies showing multi-agent collaboration
- README updated with proof section

**What this enables:**
- Developers and content designers can evaluate quality before committing
- Case studies serve as training data / few-shot examples for the agents themselves
- Shareable content for social media, blog posts, conference talks

---

## Phase 5: Evaluation & Scoring Tooling
**Goal**: Replace aspirational metrics with automated, measurable scoring.
**Estimated effort**: 2-3 days
**Impact**: Makes quality objective and trackable.

### 5.1 Build Readability Scorer
> **~45 min** | Automated text quality measurement

- [ ] Create `tools/scoring.py`
- [ ] Implement Flesch-Kincaid readability score
- [ ] Implement Flesch Reading Ease score
- [ ] Implement word count and character count
- [ ] Implement sentence length analysis (avg, max, min)
- [ ] Implement syllable count and complexity index
- [ ] Return structured score object with all metrics

### 5.2 Build Content Lint Rules
> **~60 min** | Automated content quality checks

- [ ] Create `tools/linter.py`
- [ ] Rule: CTA has action verb (check against verb dictionary)
- [ ] Rule: Error message is actionable (contains resolution language)
- [ ] Rule: No passive voice in microcopy
- [ ] Rule: Character count within mobile limits (< 40 chars for buttons, < 120 for push notifications)
- [ ] Rule: No jargon (check against configurable jargon list)
- [ ] Rule: Inclusive language check (flag exclusionary terms)
- [ ] Rule: Consistent terminology (flag when same concept uses different words)
- [ ] Each rule returns: pass/fail, severity, suggestion for fix

### 5.3 Build Brand Voice Consistency Checker
> **~45 min** | Measures adherence to a style guide

- [ ] Create `tools/voice_checker.py`
- [ ] Accept a brand voice guide as input (tone descriptors, do/don't lists, sample content)
- [ ] Use LLM to score content against voice guide (1-10 scale)
- [ ] Flag specific phrases that deviate from brand voice
- [ ] Suggest replacements aligned with brand
- [ ] Support custom voice profiles (saved as YAML configs)

### 5.4 Build Accessibility Text Checker
> **~30 min** | WCAG text-level compliance

- [ ] Create `tools/a11y_checker.py`
- [ ] Check reading level (target: grade 8 or lower for general audiences)
- [ ] Flag complex sentence structures
- [ ] Check for alt text presence (when image references detected)
- [ ] Flag ALL CAPS usage (screen reader issues)
- [ ] Flag emoji overuse (screen reader announces each one)
- [ ] Check link text clarity (no "click here" patterns)

### 5.5 Create Scoring Dashboard Output
> **~30 min** | Visualize scores in terminal and exportable formats

- [ ] Create `tools/report.py`
- [ ] Terminal output: rich-formatted scorecard with color-coded pass/fail
- [ ] JSON export: all scores in structured format
- [ ] Markdown export: human-readable report for sharing
- [ ] Comparison mode: score before vs. after agent processing

### 5.6 Write Tests for Scoring Tools
> **~30 min**

- [ ] Test readability scorer with known-score texts
- [ ] Test lint rules with intentionally good and bad content
- [ ] Test voice checker with matching and mismatching content
- [ ] Test a11y checker against WCAG-compliant and non-compliant text
- [ ] Test report generation outputs correct formats

---

### Phase 5 Summary Checkpoint
**What was accomplished:**
- Readability scorer provides automated Flesch-Kincaid and complexity metrics
- Content linter enforces 7+ rules covering CTAs, errors, mobile limits, jargon, inclusivity
- Brand voice checker scores content against custom style guides
- Accessibility checker validates WCAG text-level compliance
- Scoring dashboard outputs to terminal, JSON, and Markdown
- All tools tested

**What this enables:**
- Phase 6 CLI can run scoring alongside agent execution ("run agent + score output")
- Phase 7 CI/CD integration can use linter as a GitHub Action
- Agents can self-evaluate: run scoring on their own output and iterate

---

## Phase 6: CLI & Interface
**Goal**: Give users a dead-simple way to run agents, workflows, and scoring from the terminal.
**Estimated effort**: 2-3 days
**Impact**: Makes the agency accessible to anyone with a terminal.

### 6.1 Build Core CLI Structure
> **~45 min** | The command framework

- [ ] Create `cli.py` as entry point using Click
- [ ] Command groups: `agent`, `workflow`, `score`, `list`
- [ ] Global options: `--model`, `--verbose`, `--output-format (json|markdown|text)`
- [ ] Config file support: `.cd-agency.yaml` for defaults (model, API key, brand voice)
- [ ] Help text for every command and option

### 6.2 Implement `agent` Commands
> **~45 min** | Run individual agents

- [ ] `cd-agency agent list` - show all available agents with descriptions
- [ ] `cd-agency agent info <name>` - show full details (inputs, outputs, related agents)
- [ ] `cd-agency agent run <name> --input "text"` - run agent with inline input
- [ ] `cd-agency agent run <name> --file input.txt` - run agent with file input
- [ ] `cd-agency agent run <name> --interactive` - guided input prompts
- [ ] Support piping: `echo "text" | cd-agency agent run error-message-architect`
- [ ] Output formatting: raw text, JSON, markdown

### 6.3 Implement `workflow` Commands
> **~30 min** | Run multi-agent pipelines

- [ ] `cd-agency workflow list` - show available workflows
- [ ] `cd-agency workflow info <name>` - show workflow steps and data flow
- [ ] `cd-agency workflow run <name> --input "text"` - execute full pipeline
- [ ] `cd-agency workflow run <name> --step-by-step` - pause between steps for review
- [ ] Show progress: which step is running, intermediate outputs

### 6.4 Implement `score` Commands
> **~30 min** | Run evaluation tools standalone

- [ ] `cd-agency score readability --input "text"` - readability metrics
- [ ] `cd-agency score lint --input "text"` - content lint check
- [ ] `cd-agency score voice --input "text" --guide brand.yaml` - voice consistency
- [ ] `cd-agency score a11y --input "text"` - accessibility check
- [ ] `cd-agency score all --input "text"` - run all scorers, combined report
- [ ] `cd-agency score compare --before "text1" --after "text2"` - before/after comparison

### 6.5 Add Interactive Mode
> **~45 min** | Guided experience for new users

- [ ] `cd-agency interactive` - launches guided session
- [ ] Asks: "What are you trying to do?" → suggests agent/workflow
- [ ] Walks through required inputs with prompts and examples
- [ ] Shows output with optional scoring
- [ ] Offers to hand off to related agents ("Want to check tone? [y/n]")

### 6.6 Write CLI Tests
> **~30 min**

- [ ] Test all list/info commands return correct data
- [ ] Test agent run with inline input produces output
- [ ] Test workflow run executes all steps
- [ ] Test score commands return valid metrics
- [ ] Test piping and file input modes
- [ ] Test error handling: missing agent, bad input, API failure

---

### Phase 6 Summary Checkpoint
**What was accomplished:**
- Full CLI with `agent`, `workflow`, `score`, and `list` command groups
- Individual agent execution with multiple input modes (inline, file, pipe, interactive)
- Workflow execution with progress display and step-by-step mode
- Scoring tools accessible as standalone commands
- Interactive mode guides new users through the agency
- CLI tests cover all commands

**What this enables:**
- Any developer can use the agency from their terminal
- Phase 7 integrations can shell out to the CLI
- Package can be published to PyPI for `pip install cd-agency`

---

## Phase 7: Ecosystem & Integrations
**Goal**: Meet content designers where they already work -- Figma, GitHub, CI/CD, design systems.
**Estimated effort**: 5-7 days (this is the big one)
**Impact**: This is what turns a tool into an indispensable part of workflows.

### 7.1 GitHub Action for Content Linting
> **~3-4 hours** | Catch content issues in PRs automatically

- [ ] Create `.github/actions/content-lint/action.yml`
- [ ] Accept config: which lint rules to enable, file patterns to scan, severity thresholds
- [ ] Scan changed files in PR for UI strings (detect patterns: `.json` locale files, `.tsx`/`.jsx` with text, `.md` files)
- [ ] Run content linter on extracted strings
- [ ] Post PR comment with findings: issues found, suggestions, scores
- [ ] Support blocking: fail the check if critical issues found
- [ ] Create `examples/github-action-usage.yml` showing how to add to a repo
- [ ] Test with a sample PR

### 7.2 Figma Plugin (Design Spec)
> **~2-3 hours for spec, implementation is separate** | The killer feature

- [ ] Create `docs/figma-plugin-spec.md` with:
  - User flow: select text layer → right-click → "Run CD Agency" → pick agent → see suggestions
  - Architecture: Figma plugin UI → API call to cd-agency backend → return results to plugin
  - Required Figma API permissions
  - Mockup of plugin UI (3 screens: agent picker, input confirmation, results)
- [ ] Define API contract the plugin would call
- [ ] Create `figma-plugin/` directory with README and spec
- [ ] Outline build steps for Figma plugin development (TypeScript, Figma Plugin API)

### 7.3 Design System Presets
> **~2-3 hours** | Pre-loaded brand configurations for popular design systems

- [ ] Create `presets/` directory
- [ ] Create `presets/material-design.yaml`:
  - Voice guide: Material Design writing guidelines
  - Terminology glossary
  - Character limits per component type
  - Tone descriptors
- [ ] Create `presets/shopify-polaris.yaml`:
  - Polaris content guidelines
  - Component-specific copy rules
  - Voice and tone parameters
- [ ] Create `presets/atlassian-design.yaml`:
  - Atlassian writing guidelines
  - Product-specific terminology
- [ ] Create `presets/apple-hig.yaml`:
  - Apple Human Interface Guidelines for text
- [ ] CLI integration: `cd-agency agent run <name> --preset material-design`
- [ ] Document how to create custom presets

### 7.4 VS Code Extension (Design Spec)
> **~2 hours for spec** | In-editor content assistance

- [ ] Create `docs/vscode-extension-spec.md`:
  - Inline suggestions for UI strings in code
  - Command palette: "CD Agency: Run Agent on Selection"
  - Sidebar panel showing content scores for open file
  - Integration with VS Code's built-in linting (squiggly lines for content issues)
- [ ] Define extension architecture and API surface
- [ ] Outline build plan

### 7.5 Export Formats
> **~1-2 hours** | Integrate with content management workflows

- [ ] JSON export (for CMS import)
- [ ] CSV export (for spreadsheet review)
- [ ] XLIFF export (for translation tools)
- [ ] Markdown export (for documentation)
- [ ] Figma-compatible JSON (for design handoff)
- [ ] Add `--export <format>` flag to CLI

---

### Phase 7 Summary Checkpoint
**What was accomplished:**
- GitHub Action scans PRs for content quality issues
- Figma plugin fully specced and ready for development
- 4 design system presets (Material, Polaris, Atlassian, Apple HIG) pre-loaded
- VS Code extension specced
- 5 export formats for CMS, translation, and design tool integration

**What this enables:**
- Content quality enforcement becomes automatic in CI/CD
- Designers can access agents without leaving Figma
- Teams using popular design systems get instant value
- Agency output flows into existing content workflows

---

## Phase 8: Scale & Community
**Goal**: Build the flywheel -- community contributions, analytics, shared memory, and distribution.
**Estimated effort**: 3-5 days
**Impact**: This is what sustains growth beyond launch.

### 8.1 Custom Agent Builder
> **~3-4 hours** | Let users create their own agents

- [ ] Create `cd-agency agent create` CLI command
- [ ] Interactive wizard:
  1. Agent name and description
  2. Core mission (1-2 sentences)
  3. Critical rules (guided prompts)
  4. Input/output definitions
  5. Few-shot examples (provide 2-3)
  6. Related agents
- [ ] Generate `.md` file in correct format
- [ ] Validate generated agent (test with sample input)
- [ ] Support importing agents from other users (URL or file)

### 8.2 Multi-Agent Memory & Context
> **~3-4 hours** | Agents remember project context across sessions

- [ ] Create `runtime/memory.py`
- [ ] Project-level memory store (SQLite or JSON):
  - Brand voice decisions made
  - Terminology glossary (learned over time)
  - Content patterns preferred by this team
  - Previous agent outputs and scores
- [ ] Agent can read from memory: "Last time we decided to use 'workspace' not 'project'"
- [ ] Agent can write to memory: after user confirms a choice, store it
- [ ] Memory scoped per project (different projects = different memory)
- [ ] CLI commands: `cd-agency memory show`, `cd-agency memory clear`, `cd-agency memory export`

### 8.3 Analytics & Usage Tracking
> **~2-3 hours** | Understand how the agency is used

- [ ] Create `tools/analytics.py`
- [ ] Track (locally, opt-in):
  - Which agents are used most
  - Average scores before/after agent processing
  - Common workflows
  - Most frequent content types
- [ ] Dashboard command: `cd-agency stats`
- [ ] Export analytics as JSON/CSV for team reporting
- [ ] Privacy-first: all data local unless explicitly shared

### 8.4 Contribution Framework
> **~1-2 hours** | Make it easy for others to contribute

- [ ] Create `CONTRIBUTING.md`:
  - How to add a new agent (template + validation)
  - How to add a workflow
  - How to add a design system preset
  - How to add lint rules
  - Code style guide
  - PR template
- [ ] Create GitHub issue templates:
  - New agent request
  - Bug report
  - Feature request
  - Design system preset request
- [ ] Create `agent-template.md` - blank agent file with comments explaining each section
- [ ] Add agent validation CI: PR that adds an agent file gets auto-validated for correct structure

### 8.5 Distribution & Packaging
> **~1-2 hours** | Get it into people's hands

- [ ] Package for PyPI: `pip install cd-agency`
- [ ] Create `Dockerfile` for containerized usage
- [ ] Create Homebrew formula (for macOS users)
- [ ] Set up GitHub Releases with changelog
- [ ] Add badges to README: PyPI version, downloads, stars, license
- [ ] Create a simple landing page (GitHub Pages) with:
  - Value proposition
  - Quick start guide
  - Agent showcase
  - Link to case studies

### 8.6 Launch Checklist
> **~1 hour** | Everything needed for a successful public launch

- [ ] All 15 agents tested and producing quality output
- [ ] 5 workflows tested end-to-end
- [ ] 15+ case studies published in `/examples`
- [ ] CLI documented with `--help` on every command
- [ ] README rewritten for the post-runtime version (not just agent descriptions)
- [ ] ROADMAP.md updated with completed items and future vision
- [ ] Tweet thread / blog post drafted
- [ ] Product Hunt launch page prepared
- [ ] Hacker News "Show HN" post drafted
- [ ] Post in content design communities (UX Writing Hub, Content Design London Slack)
- [ ] Post in developer communities (Reddit r/programming, r/webdev, Dev.to)

---

### Phase 8 Summary Checkpoint
**What was accomplished:**
- Users can create custom agents via interactive wizard
- Agents maintain project memory across sessions (terminology, preferences, patterns)
- Local analytics track usage and quality improvements
- Contribution framework enables community growth
- Package distributed via PyPI, Docker, Homebrew
- Launch materials prepared for multiple channels

**What this enables:**
- Self-sustaining community of contributors
- Each team's agency gets smarter over time (memory)
- Quality data drives continuous improvement
- Distribution ensures accessibility across platforms

---

## Execution Priority Order

| Priority | Phase | Why First |
|----------|-------|-----------|
| 1 | Phase 1: Foundation | 1 day, immediate quality improvement, unblocks everything |
| 2 | Phase 2: Runtime | Core capability - nothing else works without it |
| 3 | Phase 4: Examples | Proof before features - examples drive adoption |
| 4 | Phase 3: Workflows | Multiplies agent value, demonstrates unique advantage |
| 5 | Phase 5: Scoring | Makes quality measurable, enables CI/CD integration |
| 6 | Phase 6: CLI | User interface for everything built so far |
| 7 | Phase 7: Integrations | Meet users where they work |
| 8 | Phase 8: Scale | Build the community and sustain growth |

---

## Total Estimated Effort

| Phase | Effort | Cumulative |
|-------|--------|------------|
| Phase 1: Foundation | 1-2 days | 1-2 days |
| Phase 2: Runtime | 3-5 days | 4-7 days |
| Phase 3: Workflows | 2-3 days | 6-10 days |
| Phase 4: Examples | 2-3 days | 8-13 days |
| Phase 5: Scoring | 2-3 days | 10-16 days |
| Phase 6: CLI | 2-3 days | 12-19 days |
| Phase 7: Integrations | 5-7 days | 17-26 days |
| Phase 8: Scale | 3-5 days | 20-31 days |

**Total: ~4-6 weeks of focused work to go from markdown files to a fully functional, distributed content design agency.**

---

*This plan is a living document. Update it as phases complete and priorities shift.*
