# Contributing to CD Agency

We welcome contributions! Here's how to add to the agency.

## Adding a New Agent

1. Copy `content-design/agent-template.md` to `content-design/your-agent-name.md`
2. Fill in the YAML frontmatter (name, description, inputs, outputs, tags)
3. Write the system prompt, core mission, critical rules, and 2-3 few-shot examples
4. Test it: `cd-agency agent info your-agent-name` to verify it loads
5. Add a before/after case study in `examples/`
6. Submit a PR

Or use the wizard: `cd-agency agent create`

### Agent requirements
- Name should be descriptive (e.g., "Newsletter Subject Line Writer")
- At least one required input
- At least one output
- 2-3 few-shot examples showing before → after
- Tags for discoverability

## Adding a Workflow

1. Create a YAML file in `workflows/`
2. Follow the schema in `workflows/workflow-schema.yaml`
3. Reference existing agents by slug
4. Test: `cd-agency workflow info your-workflow`

## Adding a Design System Preset

1. Create a YAML file in `presets/` following the format of existing presets
2. Include: name, tone descriptors, do/don't rules, sample content, character limits, terminology
3. Test: `cd-agency score voice -i "test text" --guide presets/your-preset.yaml --no-llm`

## Adding Lint Rules

1. Edit `tools/linter.py`
2. Add a new `LintRule` to the appropriate category
3. Add tests in `tests/test_linter.py`
4. Run: `python -m pytest tests/test_linter.py`

## Development Setup

```bash
git clone https://github.com/adedayoagarau/cd-agency.git
cd cd-agency
pip install -e ".[dev]"
python -m pytest tests/
```

## Code Style

- Python 3.10+, type hints, dataclasses over dicts
- `from __future__ import annotations` in all files
- Test coverage for new features
- Keep it simple — no over-engineering

## PR Guidelines

- One feature/fix per PR
- Include tests
- Update README if adding user-facing features
- Link to the relevant issue if applicable
