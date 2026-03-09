"""Configuration management for the CD Agency runtime."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Config:
    """Runtime configuration with environment variable overrides."""

    api_key: str = ""
    model: str = "claude-sonnet-4-20250514"
    agents_dir: Path = field(default_factory=lambda: Path("content-design"))
    max_tokens: int = 4096
    temperature: float = 0.7
    timeout: float = 60.0
    max_retries: int = 3

    @classmethod
    def from_env(cls) -> Config:
        """Load configuration from environment variables."""
        agents_dir_str = os.environ.get("CD_AGENCY_AGENTS_DIR", "content-design")
        return cls(
            api_key=os.environ.get("ANTHROPIC_API_KEY", ""),
            model=os.environ.get("CD_AGENCY_MODEL", "claude-sonnet-4-20250514"),
            agents_dir=Path(agents_dir_str),
            max_tokens=int(os.environ.get("CD_AGENCY_MAX_TOKENS", "4096")),
            temperature=float(os.environ.get("CD_AGENCY_TEMPERATURE", "0.7")),
        )

    def validate(self) -> list[str]:
        """Return a list of configuration errors, empty if valid."""
        errors = []
        if not self.api_key:
            errors.append("ANTHROPIC_API_KEY is not set")
        if not self.agents_dir.exists():
            errors.append(f"Agents directory not found: {self.agents_dir}")
        return errors
