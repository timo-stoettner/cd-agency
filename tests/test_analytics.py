"""Tests for the analytics system."""

import json
import pytest
from pathlib import Path
from tools.analytics import Analytics, AgentUsage


@pytest.fixture
def analytics(tmp_path):
    return Analytics(project_dir=tmp_path)


class TestAnalyticsTracking:
    def test_record_agent_run(self, analytics):
        analytics.record_agent_run("error-agent", input_tokens=100, output_tokens=200, latency_ms=500.0)
        assert analytics.total_runs == 1
        assert "error-agent" in analytics.agents
        assert analytics.agents["error-agent"].run_count == 1

    def test_multiple_runs(self, analytics):
        analytics.record_agent_run("agent1", latency_ms=100.0)
        analytics.record_agent_run("agent1", latency_ms=200.0)
        analytics.record_agent_run("agent2", latency_ms=300.0)
        assert analytics.total_runs == 3
        assert analytics.agents["agent1"].run_count == 2

    def test_record_with_score(self, analytics):
        analytics.record_agent_run("agent1", score=8.5)
        analytics.record_agent_run("agent1", score=7.0)
        assert analytics.agents["agent1"].avg_score == 7.75

    def test_record_workflow(self, analytics):
        analytics.record_workflow_run("content-audit")
        analytics.record_workflow_run("content-audit")
        assert analytics.workflow_runs["content-audit"] == 2

    def test_content_type_tracking(self, analytics):
        analytics.record_agent_run("agent1", content_type="cta")
        analytics.record_agent_run("agent1", content_type="cta")
        analytics.record_agent_run("agent2", content_type="error")
        assert analytics.content_types["cta"] == 2
        assert analytics.content_types["error"] == 1


class TestAnalyticsPersistence:
    def test_save_and_load(self, tmp_path):
        a1 = Analytics(project_dir=tmp_path)
        a1.record_agent_run("agent1", input_tokens=50, output_tokens=100)

        a2 = Analytics.load(tmp_path)
        assert a2.total_runs == 1
        assert "agent1" in a2.agents

    def test_load_empty(self, tmp_path):
        a = Analytics.load(tmp_path)
        assert a.total_runs == 0


class TestAnalyticsReporting:
    def test_top_agents(self, analytics):
        for _ in range(5):
            analytics.record_agent_run("popular")
        for _ in range(2):
            analytics.record_agent_run("medium")
        analytics.record_agent_run("rare")

        top = analytics.top_agents(2)
        assert len(top) == 2
        assert top[0].agent_name == "popular"
        assert top[1].agent_name == "medium"

    def test_summary(self, analytics):
        analytics.record_agent_run("agent1", input_tokens=100, output_tokens=200)
        s = analytics.summary()
        assert s["total_runs"] == 1
        assert s["unique_agents_used"] == 1
        assert s["total_tokens"] == 300

    def test_export_csv(self, analytics):
        analytics.record_agent_run("agent1", input_tokens=100, output_tokens=200)
        csv = analytics.export_csv()
        assert "agent1" in csv
        assert "Agent" in csv  # header


class TestAgentUsage:
    def test_avg_latency(self):
        u = AgentUsage(agent_name="test", run_count=2, total_latency_ms=400.0)
        assert u.avg_latency_ms == 200.0

    def test_avg_latency_zero(self):
        u = AgentUsage(agent_name="test")
        assert u.avg_latency_ms == 0.0

    def test_avg_score(self):
        u = AgentUsage(agent_name="test", scores=[8.0, 9.0, 7.0])
        assert u.avg_score == 8.0
