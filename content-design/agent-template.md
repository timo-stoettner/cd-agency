---
# Agent Template — Copy this file and fill in each section
# Run `cd-agency agent create` for a guided wizard instead

name: Your Agent Name
description: A one-line description of what this agent does.
color: "#6366F1"
version: "1.0.0"
difficulty_level: intermediate  # beginner | intermediate | advanced
tags: ["content-design"]  # Add relevant tags for filtering
inputs:
  - name: content
    type: string
    required: true
    description: "The primary input text to process"
  # Add more inputs as needed:
  # - name: context
  #   type: string
  #   required: false
  #   description: "Additional context"
outputs:
  - name: result
    type: string
    description: "The primary output"
  # Add more outputs as needed
related_agents:
  - content-designer-generalist
  # Add related agent slugs
---

### System Prompt

<!-- The agent's personality, expertise, and approach. 2-4 paragraphs. -->

You are a specialist content designer who...

**Your approach:**
- Rule 1
- Rule 2
- Rule 3

**Output format:** Describe what the agent should output.

### Core Mission

<!-- 1-2 sentences describing the agent's purpose -->

### Critical Rules

<!-- Non-negotiable rules the agent must follow -->
- Rule 1
- Rule 2
- Rule 3

### Few-Shot Examples

<!-- Provide 2-3 examples showing input → output -->

**Example 1:**

Input:
> Example input text

Output:
> Example output text

**Example 2:**

Input:
> Example input text

Output:
> Example output text
