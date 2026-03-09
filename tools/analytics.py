"""Local analytics and usage tracking for the CD Agency.

All data is stored locally. Nothing is sent externally.
Tracks: agent usage, scores, workflows, content types.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any


ANALYTICS_DIR = ".cd-agency"
ANALYTICS_FILE = "analytics.json"


@dataclass
class AgentUsage:
    """Track usage of a single agent."""

    agent_name: str
    run_count: int = 0
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    total_latency_ms: float = 0.0
    last_used: float = 0.0
    scores: list[float] = field(default_factory=list)

    @property
    def avg_latency_ms(self) -> float:
        return self.total_latency_ms / self.run_count if self.run_count else 0.0

    @property
    def avg_score(self) -> float:
        return sum(self.scores) / len(self.scores) if self.scores else 0.0


@dataclass
class Analytics:
    """Local analytics store."""

    agents: dict[str, AgentUsage] = field(default_factory=dict)
    workflow_runs: dict[str, int] = field(default_factory=dict)
    content_types: dict[str, int] = field(default_factory=dict)
    total_runs: int = 0
    first_run: float = 0.0
    project_dir: Path = field(default_factory=lambda: Path("."))

    @property
    def analytics_path(self) -> Path:
        return self.project_dir / ANALYTICS_DIR / ANALYTICS_FILE

    @classmethod
    def load(cls, project_dir: Path | None = None) -> Analytics:
        """Load analytics from disk."""
        project_dir = project_dir or Path(".")
        analytics = cls(project_dir=project_dir)
        if analytics.analytics_path.exists():
            data = json.loads(analytics.analytics_path.read_text(encoding="utf-8"))
            analytics.total_runs = data.get("total_runs", 0)
            analytics.first_run = data.get("first_run", 0.0)
            analytics.workflow_runs = data.get("workflow_runs", {})
            analytics.content_types = data.get("content_types", {})
            for name, agent_data in data.get("agents", {}).items():
                analytics.agents[name] = AgentUsage(**agent_data)
        return analytics

    def save(self) -> None:
        """Persist analytics to disk."""
        self.analytics_path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "version": "1.0",
            "total_runs": self.total_runs,
            "first_run": self.first_run,
            "workflow_runs": self.workflow_runs,
            "content_types": self.content_types,
            "agents": {k: asdict(v) for k, v in self.agents.items()},
        }
        self.analytics_path.write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def record_agent_run(
        self,
        agent_name: str,
        input_tokens: int = 0,
        output_tokens: int = 0,
        latency_ms: float = 0.0,
        score: float | None = None,
        content_type: str = "general",
    ) -> None:
        """Record an agent execution."""
        if agent_name not in self.agents:
            self.agents[agent_name] = AgentUsage(agent_name=agent_name)

        usage = self.agents[agent_name]
        usage.run_count += 1
        usage.total_input_tokens += input_tokens
        usage.total_output_tokens += output_tokens
        usage.total_latency_ms += latency_ms
        usage.last_used = time.time()
        if score is not None:
            usage.scores.append(score)

        self.total_runs += 1
        if not self.first_run:
            self.first_run = time.time()

        self.content_types[content_type] = self.content_types.get(content_type, 0) + 1
        self.save()

    def record_workflow_run(self, workflow_name: str) -> None:
        """Record a workflow execution."""
        self.workflow_runs[workflow_name] = self.workflow_runs.get(workflow_name, 0) + 1
        self.save()

    def top_agents(self, n: int = 5) -> list[AgentUsage]:
        """Get most-used agents."""
        return sorted(
            self.agents.values(),
            key=lambda a: a.run_count,
            reverse=True,
        )[:n]

    def summary(self) -> dict[str, Any]:
        """Generate a summary report."""
        return {
            "total_runs": self.total_runs,
            "unique_agents_used": len(self.agents),
            "unique_workflows_used": len(self.workflow_runs),
            "top_agents": [
                {"name": a.agent_name, "runs": a.run_count, "avg_score": round(a.avg_score, 2)}
                for a in self.top_agents()
            ],
            "content_types": self.content_types,
            "total_tokens": sum(
                a.total_input_tokens + a.total_output_tokens
                for a in self.agents.values()
            ),
        }

    def export_csv(self) -> str:
        """Export analytics as CSV."""
        import csv
        import io
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["Agent", "Runs", "Avg Latency (ms)", "Avg Score", "Total Tokens"])
        for usage in sorted(self.agents.values(), key=lambda a: a.run_count, reverse=True):
            writer.writerow([
                usage.agent_name,
                usage.run_count,
                f"{usage.avg_latency_ms:.0f}",
                f"{usage.avg_score:.2f}" if usage.scores else "N/A",
                usage.total_input_tokens + usage.total_output_tokens,
            ])
        return output.getvalue()
