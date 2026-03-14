"""Tests for the main StudioApp."""

from __future__ import annotations

import pytest

from runtime.tui.app import HelpScreen, StudioApp
from runtime.tui.widgets.agent_browser import AgentBrowser
from runtime.tui.widgets.chat_panel import ChatPanel
from runtime.tui.widgets.content_editor import ContentEditor
from runtime.tui.widgets.memory_panel import MemoryPanel
from runtime.tui.widgets.scoring_panel import ScoringPanel
from runtime.tui.widgets.status_bar import StatusBar


@pytest.fixture
def app():
    return StudioApp(preset="test-preset", initial_content="Hello world")


class TestStudioApp:
    """Tests for StudioApp mounting and key bindings."""

    @pytest.mark.asyncio
    async def test_app_mounts(self, app):
        """App should mount without errors and contain all panels."""
        async with app.run_test() as pilot:
            assert app.query_one("#agent-browser", AgentBrowser) is not None
            assert app.query_one("#chat-panel", ChatPanel) is not None
            assert app.query_one("#content-editor", ContentEditor) is not None
            assert app.query_one("#scoring-panel", ScoringPanel) is not None
            assert app.query_one("#status-bar", StatusBar) is not None
            assert app.query_one("#memory-panel", MemoryPanel) is not None

    @pytest.mark.asyncio
    async def test_initial_content(self, app):
        """Content editor should load initial content."""
        async with app.run_test() as pilot:
            editor = app.query_one("#content-editor", ContentEditor)
            assert editor.text == "Hello world"

    @pytest.mark.asyncio
    async def test_preset_in_status_bar(self, app):
        """Status bar should show the preset name."""
        async with app.run_test() as pilot:
            status = app.query_one("#status-bar", StatusBar)
            assert status._preset == "test-preset"

    @pytest.mark.asyncio
    async def test_toggle_mode(self, app):
        """Ctrl+O should toggle between Chat and Form mode."""
        async with app.run_test() as pilot:
            status = app.query_one("#status-bar", StatusBar)
            assert status._mode == "Chat"
            app.action_toggle_mode()
            assert status._mode == "Form"
            app.action_toggle_mode()
            assert status._mode == "Chat"

    @pytest.mark.asyncio
    async def test_toggle_memory(self, app):
        """Ctrl+Y should toggle memory panel visibility."""
        async with app.run_test() as pilot:
            browser = app.query_one("#agent-browser", AgentBrowser)
            memory = app.query_one("#memory-panel", MemoryPanel)
            assert browser.display is True
            assert memory.display is False
            app.action_toggle_memory()
            assert browser.display is False
            assert memory.display is True
            app.action_toggle_memory()
            assert browser.display is True
            assert memory.display is False

    @pytest.mark.asyncio
    async def test_toggle_sidebar(self, app):
        """Ctrl+B should toggle sidebar visibility."""
        async with app.run_test() as pilot:
            browser = app.query_one("#agent-browser", AgentBrowser)
            assert browser.display is True
            app.action_toggle_sidebar()
            assert browser.display is False

    @pytest.mark.asyncio
    async def test_switch_preset(self, app):
        """switch_preset should update status bar."""
        async with app.run_test() as pilot:
            app.switch_preset("Apple HIG")
            status = app.query_one("#status-bar", StatusBar)
            assert status._preset == "Apple HIG"

    @pytest.mark.asyncio
    async def test_switch_mode_to(self, app):
        """switch_mode_to should set specific mode."""
        async with app.run_test() as pilot:
            app.switch_mode_to("Form")
            status = app.query_one("#status-bar", StatusBar)
            assert status._mode == "Form"
            app.switch_mode_to("Chat")
            assert status._mode == "Chat"

    @pytest.mark.asyncio
    async def test_clear_chat_action(self, app):
        """Ctrl+L should clear chat history."""
        async with app.run_test() as pilot:
            chat = app.query_one("#chat-panel", ChatPanel)
            chat.add_user_message("test message")
            assert len(chat._messages) == 1
            app.action_clear_chat()
            assert len(chat._messages) == 0

    @pytest.mark.asyncio
    async def test_dismiss_panels_closes_memory(self, app):
        """Escape should close memory panel and show agent browser."""
        async with app.run_test() as pilot:
            browser = app.query_one("#agent-browser", AgentBrowser)
            memory = app.query_one("#memory-panel", MemoryPanel)
            # Open memory panel first
            app.action_toggle_memory()
            assert memory.display is True
            assert browser.display is False
            # Escape should close it
            app.action_dismiss_panels()
            assert memory.display is False
            assert browser.display is True

    @pytest.mark.asyncio
    async def test_dismiss_panels_restores_sidebar(self, app):
        """Escape should restore sidebar when it's hidden."""
        async with app.run_test() as pilot:
            browser = app.query_one("#agent-browser", AgentBrowser)
            app.action_toggle_sidebar()
            assert browser.display is False
            app.action_dismiss_panels()
            assert browser.display is True

    @pytest.mark.asyncio
    async def test_help_screen_opens(self, app):
        """F1 should open the help screen modal."""
        async with app.run_test() as pilot:
            app.action_help_screen()
            assert app.screen.__class__.__name__ == "HelpScreen"

    @pytest.mark.asyncio
    async def test_score_content_action(self, app):
        """Ctrl+S should trigger scoring on editor content."""
        async with app.run_test() as pilot:
            # Has initial content "Hello world", so scoring should work
            app.action_score_content()
            # Should not raise

    @pytest.mark.asyncio
    async def test_run_agent_without_agent_selected(self, app):
        """Ctrl+R without agent selected should show guidance message."""
        async with app.run_test() as pilot:
            app.action_run_agent()
            chat = app.query_one("#chat-panel", ChatPanel)
            assert any("select an agent" in m["content"].lower() for m in chat._messages)

    @pytest.mark.asyncio
    async def test_bindings_avoid_terminal_conflicts(self, app):
        """Bindings should not use ctrl+m (= Enter) or ctrl+t (= new tab)."""
        binding_keys = [b.key for b in app.BINDINGS]
        assert "ctrl+m" not in binding_keys, "ctrl+m conflicts with Enter in terminals"
        assert "ctrl+t" not in binding_keys, "ctrl+t conflicts with new-tab in terminals"
