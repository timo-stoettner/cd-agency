"""Pydantic models for API request/response schemas."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


# ── Agent Models ──────────────────────────────────────────────────────────────


class AgentInputSchema(BaseModel):
    """Schema for an agent's expected input field."""

    name: str
    type: str
    required: bool
    description: str = ""


class AgentOutputSchema(BaseModel):
    """Schema for an agent's expected output field."""

    name: str
    type: str
    description: str = ""


class AgentSummary(BaseModel):
    """Lightweight agent representation for list endpoints."""

    slug: str
    name: str
    description: str
    tags: list[str] = []


class AgentDetail(BaseModel):
    """Full agent representation including inputs and outputs."""

    slug: str
    name: str
    description: str
    tags: list[str] = []
    inputs: list[AgentInputSchema] = []
    outputs: list[AgentOutputSchema] = []
    related_agents: list[str] = []
    version: str = "1.0.0"
    difficulty_level: str = "intermediate"


class AgentRunRequest(BaseModel):
    """Request body for running an agent."""

    input: dict[str, Any] = Field(..., description="Input fields for the agent")
    preset: str | None = Field(None, description="Optional design system preset name")


class AgentRunResponse(BaseModel):
    """Response from running an agent."""

    content: str
    agent_name: str
    model: str = ""
    input_tokens: int = 0
    output_tokens: int = 0
    latency_ms: float = 0.0


# ── Scoring Models ────────────────────────────────────────────────────────────


class ScoreRequest(BaseModel):
    """Request body for scoring endpoints."""

    text: str = Field(..., min_length=1, description="Text content to score")


class ReadabilityResponse(BaseModel):
    """Readability scoring result."""

    word_count: int
    character_count: int
    sentence_count: int
    syllable_count: int
    avg_sentence_length: float
    max_sentence_length: int
    min_sentence_length: int
    avg_word_length: float
    flesch_reading_ease: float
    flesch_kincaid_grade: float
    complexity_index: float
    reading_time_seconds: float
    grade_label: str
    ease_label: str


class LintIssue(BaseModel):
    """A single lint rule result."""

    rule: str
    passed: bool
    severity: str
    message: str
    suggestion: str = ""
    matches: list[str] = []


class LintResponse(BaseModel):
    """Linter result containing all rule checks."""

    issues: list[LintIssue]
    passed_count: int
    failed_count: int
    total_rules: int


class A11yIssueResponse(BaseModel):
    """A single accessibility issue."""

    rule: str
    severity: str
    message: str
    wcag_criterion: str
    suggestion: str = ""
    matches: list[str] = []


class A11yResponse(BaseModel):
    """Accessibility checker result."""

    passed: bool
    label: str
    issue_count: int
    reading_grade: float
    target_grade: float
    issues: list[A11yIssueResponse]


class CombinedScoreResponse(BaseModel):
    """Combined result from all scoring tools."""

    readability: ReadabilityResponse
    lint: LintResponse
    a11y: A11yResponse


# ── Preset Models ─────────────────────────────────────────────────────────────


class PresetSummary(BaseModel):
    """Lightweight preset representation for list endpoints."""

    name: str
    filename: str


class PresetDetail(BaseModel):
    """Full preset data."""

    name: str
    filename: str
    tone_descriptors: list[str] = []
    do: list[str] = Field(default_factory=list, alias="do_rules")
    dont: list[str] = Field(default_factory=list, alias="dont_rules")
    sample_content: list[str] = []
    character_limits: dict[str, int] = {}
    terminology: dict[str, str] = {}

    model_config = {"populate_by_name": True}
