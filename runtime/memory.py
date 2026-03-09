"""Project-level memory store for cross-session agent context.

Agents can read from memory ("Last time we decided to use 'workspace' not 'project'")
and write to memory after user confirms a choice. Memory is scoped per project directory.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any


MEMORY_DIR = ".cd-agency"
MEMORY_FILE = "memory.json"


@dataclass
class MemoryEntry:
    """A single memory entry."""

    key: str
    value: str
    category: str  # terminology, voice, pattern, decision
    source_agent: str = ""
    timestamp: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.timestamp:
            self.timestamp = time.time()


@dataclass
class ProjectMemory:
    """Project-scoped memory store backed by a JSON file."""

    entries: dict[str, MemoryEntry] = field(default_factory=dict)
    project_dir: Path = field(default_factory=lambda: Path("."))

    @property
    def memory_path(self) -> Path:
        return self.project_dir / MEMORY_DIR / MEMORY_FILE

    @classmethod
    def load(cls, project_dir: Path | None = None) -> ProjectMemory:
        """Load memory from the project directory."""
        project_dir = project_dir or Path(".")
        memory = cls(project_dir=project_dir)
        if memory.memory_path.exists():
            data = json.loads(memory.memory_path.read_text(encoding="utf-8"))
            for key, entry_data in data.get("entries", {}).items():
                memory.entries[key] = MemoryEntry(**entry_data)
        return memory

    def save(self) -> None:
        """Persist memory to disk."""
        self.memory_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "version": "1.0",
            "entries": {k: asdict(v) for k, v in self.entries.items()},
        }
        self.memory_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def remember(
        self,
        key: str,
        value: str,
        category: str = "decision",
        source_agent: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Store a memory entry."""
        self.entries[key] = MemoryEntry(
            key=key,
            value=value,
            category=category,
            source_agent=source_agent,
            metadata=metadata or {},
        )
        self.save()

    def recall(self, key: str) -> MemoryEntry | None:
        """Retrieve a specific memory by key."""
        return self.entries.get(key)

    def recall_by_category(self, category: str) -> list[MemoryEntry]:
        """Get all memories in a category."""
        return [e for e in self.entries.values() if e.category == category]

    def search(self, query: str) -> list[MemoryEntry]:
        """Search memories by key or value substring."""
        query_lower = query.lower()
        return [
            e for e in self.entries.values()
            if query_lower in e.key.lower() or query_lower in e.value.lower()
        ]

    def forget(self, key: str) -> bool:
        """Remove a memory entry."""
        if key in self.entries:
            del self.entries[key]
            self.save()
            return True
        return False

    def clear(self) -> int:
        """Clear all memory. Returns count of entries removed."""
        count = len(self.entries)
        self.entries.clear()
        self.save()
        return count

    def get_context_for_agent(self, agent_name: str = "") -> str:
        """Build a context string from memory for use in agent prompts."""
        if not self.entries:
            return ""

        parts = ["## Project Memory\n"]

        # Terminology decisions
        terms = self.recall_by_category("terminology")
        if terms:
            parts.append("### Terminology Decisions")
            for t in terms:
                parts.append(f"- **{t.key}**: {t.value}")

        # Voice decisions
        voice = self.recall_by_category("voice")
        if voice:
            parts.append("\n### Voice & Tone Decisions")
            for v in voice:
                parts.append(f"- {v.key}: {v.value}")

        # Patterns
        patterns = self.recall_by_category("pattern")
        if patterns:
            parts.append("\n### Content Patterns")
            for p in patterns:
                parts.append(f"- {p.key}: {p.value}")

        # General decisions
        decisions = self.recall_by_category("decision")
        if decisions:
            parts.append("\n### Past Decisions")
            for d in decisions:
                parts.append(f"- {d.key}: {d.value}")

        return "\n".join(parts)

    def to_dict(self) -> dict:
        """Export memory as a dictionary."""
        return {
            "project": str(self.project_dir),
            "entry_count": len(self.entries),
            "categories": list(set(e.category for e in self.entries.values())),
            "entries": {k: asdict(v) for k, v in self.entries.items()},
        }

    def __len__(self) -> int:
        return len(self.entries)
