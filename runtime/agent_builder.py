"""Custom agent builder — interactive wizard to create new agents."""

from __future__ import annotations

from pathlib import Path

import click
import yaml


AGENT_TEMPLATE = """---
name: {name}
description: {description}
color: "{color}"
version: "1.0.0"
difficulty_level: {difficulty}
tags: {tags}
inputs:
{inputs_yaml}outputs:
{outputs_yaml}related_agents:
{related_yaml}---

### System Prompt

{system_prompt}

### Core Mission

{core_mission}

### Critical Rules

{critical_rules}

### Few-Shot Examples

{examples}
"""


def build_agent_interactive(output_dir: Path) -> Path:
    """Run the interactive wizard to create a new agent."""
    click.echo("\n🛠  Custom Agent Builder\n")
    click.echo("Let's create a new content design agent.\n")

    # Step 1: Name and description
    name = click.prompt("Agent name (e.g., 'Newsletter Subject Line Writer')")
    description = click.prompt("One-line description")
    slug = name.lower().replace(" ", "-").replace("&", "and")
    slug = "".join(c for c in slug if c.isalnum() or c == "-")

    # Step 2: Core mission
    click.echo("\nDefine the agent's core mission (1-2 sentences):")
    core_mission = click.prompt("Core mission")

    # Step 3: Difficulty and color
    difficulty = click.prompt(
        "Difficulty level",
        type=click.Choice(["beginner", "intermediate", "advanced"]),
        default="intermediate",
    )
    color = click.prompt("Brand color (hex)", default="#6366F1")

    # Step 4: Tags
    tags_str = click.prompt("Tags (comma-separated)", default="content-design")
    tags = [t.strip() for t in tags_str.split(",") if t.strip()]

    # Step 5: Inputs
    click.echo("\nDefine inputs (what the agent needs from the user):")
    inputs = []
    while True:
        inp_name = click.prompt("  Input name (or 'done' to finish)", default="done")
        if inp_name.lower() == "done":
            break
        inp_desc = click.prompt(f"  Description for '{inp_name}'", default="")
        inp_required = click.confirm(f"  Is '{inp_name}' required?", default=True)
        inputs.append({
            "name": inp_name,
            "type": "string",
            "required": inp_required,
            "description": inp_desc,
        })

    if not inputs:
        inputs = [{"name": "content", "type": "string", "required": True, "description": "The content to process"}]

    # Step 6: Outputs
    click.echo("\nDefine outputs (what the agent produces):")
    outputs = []
    while True:
        out_name = click.prompt("  Output name (or 'done' to finish)", default="done")
        if out_name.lower() == "done":
            break
        out_desc = click.prompt(f"  Description for '{out_name}'", default="")
        outputs.append({"name": out_name, "type": "string", "description": out_desc})

    if not outputs:
        outputs = [{"name": "result", "type": "string", "description": "The processed content"}]

    # Step 7: Critical rules
    click.echo("\nDefine critical rules (press Enter twice to finish):")
    rules = []
    while True:
        rule = click.prompt("  Rule (or 'done')", default="done")
        if rule.lower() == "done":
            break
        rules.append(f"- {rule}")
    critical_rules = "\n".join(rules) if rules else "- Always prioritize clarity over cleverness\n- Match the user's brand voice"

    # Step 8: System prompt
    click.echo("\nWrite the system prompt (the agent's personality and approach):")
    system_prompt = click.prompt(
        "System prompt",
        default=f"You are a specialist content designer focused on {core_mission.lower()}. "
                "You write clear, user-centered content that follows best practices.",
    )

    # Step 9: Few-shot examples
    click.echo("\nProvide 2-3 few-shot examples (before → after):")
    examples_parts = []
    for i in range(1, 4):
        before = click.prompt(f"  Example {i} — Before (or 'done')", default="done")
        if before.lower() == "done":
            break
        after = click.prompt(f"  Example {i} — After")
        examples_parts.append(f"**Before:** {before}\n**After:** {after}")

    examples = "\n\n".join(examples_parts) if examples_parts else "*(Add examples here)*"

    # Step 10: Related agents
    related_str = click.prompt(
        "Related agents (comma-separated slugs, or 'none')",
        default="content-designer-generalist",
    )
    related = [r.strip() for r in related_str.split(",") if r.strip() and r.strip() != "none"]

    # Build YAML blocks
    inputs_yaml = ""
    for inp in inputs:
        inputs_yaml += f'  - name: {inp["name"]}\n'
        inputs_yaml += f'    type: {inp["type"]}\n'
        inputs_yaml += f'    required: {"true" if inp["required"] else "false"}\n'
        inputs_yaml += f'    description: "{inp["description"]}"\n'

    outputs_yaml = ""
    for out in outputs:
        outputs_yaml += f'  - name: {out["name"]}\n'
        outputs_yaml += f'    type: {out["type"]}\n'
        outputs_yaml += f'    description: "{out["description"]}"\n'

    related_yaml = ""
    for r in related:
        related_yaml += f"  - {r}\n"
    if not related_yaml:
        related_yaml = "  []\n"

    tags_formatted = json_list(tags)

    content = AGENT_TEMPLATE.format(
        name=name,
        description=description,
        color=color,
        difficulty=difficulty,
        tags=tags_formatted,
        inputs_yaml=inputs_yaml,
        outputs_yaml=outputs_yaml,
        related_yaml=related_yaml,
        system_prompt=system_prompt,
        core_mission=core_mission,
        critical_rules=critical_rules,
        examples=examples,
    )

    output_file = output_dir / f"{slug}.md"
    output_file.write_text(content, encoding="utf-8")

    click.echo(f"\n✅ Agent created: {output_file}")
    click.echo(f"   Run it: cd-agency agent run {slug} -i \"your input\"")

    return output_file


def json_list(items: list[str]) -> str:
    """Format a list as YAML inline array."""
    return "[" + ", ".join(f'"{item}"' for item in items) + "]"


def import_agent(source: str, output_dir: Path) -> Path:
    """Import an agent from a file path or URL."""
    source_path = Path(source)

    if source_path.exists():
        content = source_path.read_text(encoding="utf-8")
    else:
        raise FileNotFoundError(f"Agent file not found: {source}")

    # Extract slug from filename
    slug = source_path.stem
    output_file = output_dir / f"{slug}.md"
    output_file.write_text(content, encoding="utf-8")

    click.echo(f"✅ Agent imported: {output_file}")
    return output_file
