# Roadmap

> From 15 markdown agents to a fully functional content design platform.

## Completed

### Phase 1: Foundation & Structure
- [x] Decision tree for agent selection (`docs/WHEN_TO_USE.md`)
- [x] Structured YAML frontmatter on all 15 agents (inputs, outputs, related agents, tags, version)
- [x] System prompts with few-shot examples replacing personality sections
- [x] Project directory scaffolding
- [x] Public roadmap

### Phase 2: Runtime & Execution Layer
- [x] Python SDK to load and run agents programmatically
- [x] Agent loader that parses `.md` files into executable objects
- [x] Input/output validation with Pydantic
- [x] Agent registry with name/alias/tag lookup
- [x] Streaming output support

### Phase 3: Multi-Agent Workflows
- [x] Workflow schema (sequential, parallel, conditional steps)
- [x] Workflow engine with state management
- [x] Core workflows: Content Audit, Error Pipeline, Launch Package, Localization Prep, Notification Suite

### Phase 4: Proof & Portfolio
- [x] Before/after case studies for top 5 agents (3 each)
- [x] Full workflow case studies showing multi-agent collaboration
- [x] Standardized case study template

### Phase 5: Evaluation & Scoring
- [x] Readability scorer (Flesch-Kincaid)
- [x] Content linter (CTA verbs, mobile limits, jargon, inclusive language)
- [x] Brand voice consistency checker
- [x] Accessibility text checker (WCAG)
- [x] Scoring dashboard (terminal, JSON, Markdown export)

### Phase 6: CLI
- [x] `cd-agency agent run <name>` — run individual agents
- [x] `cd-agency workflow run <name>` — run multi-agent pipelines
- [x] `cd-agency score <type>` — run evaluation tools
- [x] Interactive mode for guided usage

### Phase 7: Ecosystem & Integrations
- [x] GitHub Action for content linting in PRs
- [x] Design system presets (Material, Polaris, Atlassian, Apple HIG)
- [x] Export formats (JSON, CSV, XLIFF, Markdown)
- [x] Figma plugin — full TypeScript plugin with agent picker, results UI, one-click apply
- [x] VS Code extension — inline linting, agent runner, scoring commands
- [x] FastAPI REST API backend for Figma plugin and external integrations
- [x] Paper.design MCP server — Model Context Protocol integration for AI-native design tools
- [x] MCP tools: agent listing, scoring, linting, a11y checking, preset lookup

### Phase 8: Scale & Community
- [x] Custom agent builder (`cd-agency agent create`)
- [x] Project memory (terminology, preferences across sessions)
- [x] Contribution framework and templates
- [x] PyPI / Docker / Homebrew distribution
- [x] Marketing landing page and documentation site
- [x] Launch materials

## Future

### Phase 9: Advanced Integrations
- [ ] Figma plugin published to Figma Community marketplace
- [ ] VS Code extension published to VS Code Marketplace
- [ ] Slack bot integration
- [ ] Notion integration
- [ ] Browser extension for live content auditing
- [ ] Webhooks for CI/CD pipeline triggers

### Phase 10: Intelligence & Learning
- [ ] Agent self-improvement loop (score own output, iterate)
- [ ] Team analytics dashboard (web UI)
- [ ] A/B testing framework for content variants
- [ ] Custom model fine-tuning on team's content decisions
- [ ] Multi-language support (beyond English)

---

See [IMPLEMENTATION_PLAN.md](./IMPLEMENTATION_PLAN.md) for detailed, task-level breakdowns of each phase.
