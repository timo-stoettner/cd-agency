"""Agent registry — central lookup for all available agents."""

from __future__ import annotations

from pathlib import Path

from runtime.agent import Agent
from runtime.loader import load_agents_from_directory


# Common aliases: short name → agent slug
_DEFAULT_ALIASES: dict[str, str] = {
    "generalist": "content-designer-generalist",
    "general": "content-designer-generalist",
    "error": "error-message-architect",
    "errors": "error-message-architect",
    "microcopy": "microcopy-review-agent",
    "tone": "tone-evaluation-agent",
    "voice": "tone-evaluation-agent",
    "a11y": "accessibility-content-auditor",
    "accessibility": "accessibility-content-auditor",
    "wcag": "accessibility-content-auditor",
    "cta": "cta-optimization-specialist",
    "onboarding": "onboarding-flow-designer",
    "docs": "technical-documentation-writer",
    "tech-docs": "technical-documentation-writer",
    "mobile": "mobile-ux-writer",
    "l10n": "localization-content-strategist",
    "localization": "localization-content-strategist",
    "i18n": "localization-content-strategist",
    "notifications": "notification-content-designer",
    "notify": "notification-content-designer",
    "push": "notification-content-designer",
    "privacy": "privacy-legal-content-simplifier",
    "legal": "privacy-legal-content-simplifier",
    "empty": "empty-state-placeholder-specialist",
    "placeholder": "empty-state-placeholder-specialist",
    "search": "search-experience-writer",
    "chatbot": "conversational-ai-designer",
    "conversation": "conversational-ai-designer",
}


class AgentRegistry:
    """Central lookup for all available agents.

    Supports lookup by name, slug, alias, or tag.
    """

    def __init__(self, agents: list[Agent] | None = None) -> None:
        self._agents: dict[str, Agent] = {}
        self._aliases: dict[str, str] = dict(_DEFAULT_ALIASES)
        if agents:
            for agent in agents:
                self.register(agent)

    @classmethod
    def from_directory(cls, directory: Path) -> AgentRegistry:
        """Load all agents from a directory and build the registry."""
        agents = load_agents_from_directory(directory)
        return cls(agents)

    def register(self, agent: Agent) -> None:
        """Register an agent in the registry."""
        self._agents[agent.slug] = agent

    def get(self, name: str) -> Agent | None:
        """Look up an agent by name, slug, or alias."""
        key = name.lower().strip()

        # Direct slug match
        if key in self._agents:
            return self._agents[key]

        # Alias match
        if key in self._aliases:
            slug = self._aliases[key]
            return self._agents.get(slug)

        # Fuzzy match on agent name
        for agent in self._agents.values():
            if key == agent.name.lower():
                return agent

        return None

    def list_all(self) -> list[Agent]:
        """Return all registered agents sorted by name."""
        return sorted(self._agents.values(), key=lambda a: a.name)

    def filter_by_tag(self, tag: str) -> list[Agent]:
        """Return agents that have a specific tag."""
        tag_lower = tag.lower()
        return [a for a in self._agents.values() if tag_lower in a.tags]

    def filter_by_difficulty(self, level: str) -> list[Agent]:
        """Return agents at a specific difficulty level."""
        return [a for a in self._agents.values() if a.difficulty_level == level]

    def search(self, query: str) -> list[Agent]:
        """Search agents by name, description, or tags."""
        q = query.lower()
        results = []
        for agent in self._agents.values():
            if (q in agent.name.lower()
                    or q in agent.description.lower()
                    or any(q in tag for tag in agent.tags)):
                results.append(agent)
        return sorted(results, key=lambda a: a.name)

    def add_alias(self, alias: str, slug: str) -> None:
        """Add a custom alias for an agent slug."""
        self._aliases[alias.lower()] = slug

    @property
    def count(self) -> int:
        """Number of registered agents."""
        return len(self._agents)

    def __contains__(self, name: str) -> bool:
        return self.get(name) is not None

    def __len__(self) -> int:
        return self.count
