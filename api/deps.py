"""FastAPI dependencies — registry, runner, and auth."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Annotated

from fastapi import Depends, Header, HTTPException, status

from runtime.config import Config
from runtime.registry import AgentRegistry
from runtime.runner import AgentRunner

# ── Paths ─────────────────────────────────────────────────────────────────────

CONTENT_DESIGN_DIR = Path(__file__).parent.parent / "content-design"
PRESETS_DIR = Path(__file__).parent.parent / "presets"

# ── Singletons ────────────────────────────────────────────────────────────────

_registry: AgentRegistry | None = None
_runner: AgentRunner | None = None


def get_registry() -> AgentRegistry:
    """Return a cached AgentRegistry loaded from the content-design/ directory."""
    global _registry
    if _registry is None:
        _registry = AgentRegistry.from_directory(CONTENT_DESIGN_DIR)
    return _registry


def get_runner() -> AgentRunner:
    """Return a cached AgentRunner with configuration from the environment."""
    global _runner
    if _runner is None:
        config = Config.from_env()
        _runner = AgentRunner(config)
    return _runner


# ── Auth ──────────────────────────────────────────────────────────────────────


async def verify_api_key(
    x_api_key: Annotated[str | None, Header()] = None,
) -> str | None:
    """Optionally require an API key via the X-API-Key header.

    Enabled when the ``CD_AGENCY_REQUIRE_AUTH`` environment variable is set to
    a truthy value (``1``, ``true``, ``yes``).  When auth is required, the
    header value must match the ``CD_AGENCY_API_KEY`` environment variable.
    """
    require_auth = os.environ.get("CD_AGENCY_REQUIRE_AUTH", "").lower() in (
        "1",
        "true",
        "yes",
    )

    if not require_auth:
        return x_api_key

    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing X-API-Key header",
        )

    expected_key = os.environ.get("CD_AGENCY_API_KEY", "")
    if not expected_key or x_api_key != expected_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key",
        )

    return x_api_key
