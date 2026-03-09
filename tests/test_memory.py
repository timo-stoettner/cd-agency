"""Tests for the project memory system."""

import json
import pytest
from pathlib import Path
from runtime.memory import ProjectMemory, MemoryEntry


@pytest.fixture
def memory(tmp_path):
    return ProjectMemory(project_dir=tmp_path)


class TestMemoryOperations:
    def test_remember_and_recall(self, memory):
        memory.remember("app_name", "workspace", category="terminology")
        entry = memory.recall("app_name")
        assert entry is not None
        assert entry.value == "workspace"
        assert entry.category == "terminology"

    def test_recall_missing(self, memory):
        assert memory.recall("nonexistent") is None

    def test_recall_by_category(self, memory):
        memory.remember("term1", "val1", category="terminology")
        memory.remember("term2", "val2", category="terminology")
        memory.remember("voice1", "val3", category="voice")
        terms = memory.recall_by_category("terminology")
        assert len(terms) == 2

    def test_search(self, memory):
        memory.remember("button_label", "Use 'Start' not 'Begin'", category="terminology")
        results = memory.search("start")
        assert len(results) == 1
        assert results[0].key == "button_label"

    def test_forget(self, memory):
        memory.remember("key1", "val1")
        assert memory.forget("key1") is True
        assert memory.recall("key1") is None
        assert memory.forget("nonexistent") is False

    def test_clear(self, memory):
        memory.remember("k1", "v1")
        memory.remember("k2", "v2")
        count = memory.clear()
        assert count == 2
        assert len(memory) == 0

    def test_len(self, memory):
        assert len(memory) == 0
        memory.remember("k1", "v1")
        assert len(memory) == 1


class TestMemoryPersistence:
    def test_save_and_load(self, tmp_path):
        mem1 = ProjectMemory(project_dir=tmp_path)
        mem1.remember("key", "value", category="decision")

        mem2 = ProjectMemory.load(tmp_path)
        assert len(mem2) == 1
        assert mem2.recall("key").value == "value"

    def test_load_empty(self, tmp_path):
        mem = ProjectMemory.load(tmp_path)
        assert len(mem) == 0


class TestMemoryContext:
    def test_get_context_empty(self, memory):
        assert memory.get_context_for_agent() == ""

    def test_get_context_with_entries(self, memory):
        memory.remember("app", "workspace", category="terminology")
        memory.remember("tone", "friendly but professional", category="voice")
        ctx = memory.get_context_for_agent()
        assert "workspace" in ctx
        assert "friendly" in ctx
        assert "Terminology" in ctx

    def test_to_dict(self, memory):
        memory.remember("k1", "v1")
        d = memory.to_dict()
        assert d["entry_count"] == 1
        assert "k1" in d["entries"]
