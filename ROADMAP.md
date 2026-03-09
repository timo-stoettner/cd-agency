# Roadmap

> From 15 markdown agents to a fully functional content design platform.

## Completed

### Phase 1: Foundation & Structure
- [x] Decision tree for agent selection (`docs/WHEN_TO_USE.md`)
- [x] Structured YAML frontmatter on all 15 agents (inputs, outputs, related agents, tags, version)
- [x] System prompts with few-shot examples replacing personality sections
- [x] Project directory scaffolding
- [x] Public roadmap

## Up Next

### Phase 2: Runtime & Execution Layer
- [ ] Python SDK to load and run agents programmatically
- [ ] Agent loader that parses `.md` files into executable objects
- [ ] Input/output validation with Pydantic
- [ ] Agent registry with name/alias/tag lookup
- [ ] Streaming output support

### Phase 3: Multi-Agent Workflows
- [ ] Workflow schema (sequential, parallel, conditional steps)
- [ ] Workflow engine with state management
- [ ] Core workflows: Content Audit, Error Pipeline, Launch Package, Localization Prep, Notification Suite

### Phase 4: Proof & Portfolio
- [ ] Before/after case studies for top 5 agents (3 each)
- [ ] Full workflow case studies showing multi-agent collaboration
- [ ] Standardized case study template

### Phase 5: Evaluation & Scoring
- [ ] Readability scorer (Flesch-Kincaid)
- [ ] Content linter (CTA verbs, mobile limits, jargon, inclusive language)
- [ ] Brand voice consistency checker
- [ ] Accessibility text checker (WCAG)
- [ ] Scoring dashboard (terminal, JSON, Markdown export)

### Phase 6: CLI
- [ ] `cd-agency agent run <name>` — run individual agents
- [ ] `cd-agency workflow run <name>` — run multi-agent pipelines
- [ ] `cd-agency score <type>` — run evaluation tools
- [ ] Interactive mode for guided usage

### Phase 7: Ecosystem & Integrations
- [ ] GitHub Action for content linting in PRs
- [ ] Design system presets (Material, Polaris, Atlassian, Apple HIG)
- [ ] Export formats (JSON, CSV, XLIFF, Markdown)
- [ ] Figma plugin spec
- [ ] VS Code extension spec

### Phase 8: Scale & Community
- [ ] Custom agent builder (`cd-agency agent create`)
- [ ] Project memory (terminology, preferences across sessions)
- [ ] Contribution framework and templates
- [ ] PyPI / Docker / Homebrew distribution
- [ ] Launch materials

---

See [IMPLEMENTATION_PLAN.md](./IMPLEMENTATION_PLAN.md) for detailed, task-level breakdowns of each phase.
