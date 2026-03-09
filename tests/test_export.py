"""Tests for the export module."""

import json
import pytest
from tools.export import ContentEntry, ExportFormat, export_entries


@pytest.fixture
def entries():
    return [
        ContentEntry(id="1", source="Submit", target="Start free trial", context="CTA button", agent="cta-optimizer"),
        ContentEntry(id="2", source="Error occurred", target="Something went wrong. Try again.", context="Error state", agent="error-architect"),
    ]


class TestExportFormats:
    def test_export_json(self, entries):
        result = export_entries(entries, ExportFormat.JSON)
        data = json.loads(result)
        assert data["count"] == 2
        assert len(data["entries"]) == 2
        assert data["entries"][0]["source"] == "Submit"

    def test_export_csv(self, entries):
        result = export_entries(entries, ExportFormat.CSV)
        assert "Submit" in result
        assert "Start free trial" in result
        assert "ID" in result  # header

    def test_export_markdown(self, entries):
        result = export_entries(entries, ExportFormat.MARKDOWN)
        assert "# Content Export" in result
        assert "Submit" in result
        assert "2 entries exported" in result

    def test_export_xliff(self, entries):
        result = export_entries(entries, ExportFormat.XLIFF)
        assert '<?xml version="1.0"' in result
        assert "<source>Submit</source>" in result
        assert "<target>Start free trial</target>" in result
        assert "xliff" in result

    def test_xliff_escapes_xml(self):
        entries = [ContentEntry(id="1", source='Say "hello" & <goodbye>', target="fixed")]
        result = export_entries(entries, ExportFormat.XLIFF)
        assert "&amp;" in result
        assert "&lt;" in result
        assert "&quot;" in result


class TestContentEntry:
    def test_to_dict_minimal(self):
        e = ContentEntry(id="1", source="a", target="b")
        d = e.to_dict()
        assert d == {"id": "1", "source": "a", "target": "b"}

    def test_to_dict_full(self):
        e = ContentEntry(id="1", source="a", target="b", context="ctx", agent="ag", notes="n")
        d = e.to_dict()
        assert d["context"] == "ctx"
        assert d["agent"] == "ag"
        assert d["notes"] == "n"
