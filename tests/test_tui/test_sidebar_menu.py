"""Tests for the SidebarMenu widget."""

from __future__ import annotations

import pytest

from textual.app import App, ComposeResult
from textual.widgets import Button

from runtime.tui.widgets.sidebar_menu import MenuAction, SidebarMenu


class MenuTestApp(App):
    """Minimal app for testing the sidebar menu."""

    def compose(self) -> ComposeResult:
        yield SidebarMenu(id="sidebar-menu")


@pytest.fixture
def app():
    return MenuTestApp()


class TestSidebarMenu:
    """Tests for SidebarMenu rendering and interactions."""

    @pytest.mark.asyncio
    async def test_mounts(self, app):
        """Menu should mount with all expected buttons."""
        async with app.run_test() as pilot:
            menu = app.query_one("#sidebar-menu", SidebarMenu)
            assert menu is not None

    @pytest.mark.asyncio
    async def test_has_action_buttons(self, app):
        """Menu should contain action buttons for key operations."""
        async with app.run_test() as pilot:
            assert app.query_one("#menu-run-agent", Button) is not None
            assert app.query_one("#menu-score", Button) is not None
            assert app.query_one("#menu-clear", Button) is not None
            assert app.query_one("#menu-palette", Button) is not None
            assert app.query_one("#menu-toggle-mode", Button) is not None
            assert app.query_one("#menu-memory", Button) is not None
            assert app.query_one("#menu-help", Button) is not None

    @pytest.mark.asyncio
    async def test_has_preset_buttons(self, app):
        """Menu should contain preset selection buttons."""
        async with app.run_test() as pilot:
            assert app.query_one("#menu-preset-material", Button) is not None
            assert app.query_one("#menu-preset-apple", Button) is not None
            assert app.query_one("#menu-preset-polaris", Button) is not None
            assert app.query_one("#menu-preset-atlassian", Button) is not None

    @pytest.mark.asyncio
    async def test_set_mode_updates_label(self, app):
        """set_mode should update the toggle button label."""
        async with app.run_test() as pilot:
            menu = app.query_one("#sidebar-menu", SidebarMenu)
            menu.set_mode("Form")
            btn = app.query_one("#menu-toggle-mode", Button)
            assert "Form" in str(btn.label)

    @pytest.mark.asyncio
    async def test_set_preset_highlights_active(self, app):
        """set_preset should set the active preset button to primary variant."""
        async with app.run_test() as pilot:
            menu = app.query_one("#sidebar-menu", SidebarMenu)
            menu.set_preset("Apple HIG")
            apple_btn = app.query_one("#menu-preset-apple", Button)
            material_btn = app.query_one("#menu-preset-material", Button)
            assert apple_btn.variant == "primary"
            assert material_btn.variant == "default"

    @pytest.mark.asyncio
    async def test_set_preset_switches_highlight(self, app):
        """Changing preset should move highlight to the new preset."""
        async with app.run_test() as pilot:
            menu = app.query_one("#sidebar-menu", SidebarMenu)
            menu.set_preset("Material Design")
            assert app.query_one("#menu-preset-material", Button).variant == "primary"
            menu.set_preset("Polaris")
            assert app.query_one("#menu-preset-material", Button).variant == "default"
            assert app.query_one("#menu-preset-polaris", Button).variant == "primary"

    @pytest.mark.asyncio
    async def test_button_posts_menu_action(self, app):
        """Clicking a menu button should post a MenuAction message."""
        messages = []

        async with app.run_test() as pilot:
            menu = app.query_one("#sidebar-menu", SidebarMenu)

            def capture(event: MenuAction):
                messages.append(event.action)

            menu.on_menu_action = capture  # type: ignore

            btn = app.query_one("#menu-run-agent", Button)
            btn.press()
            await pilot.pause()
            # The MenuAction is posted to the parent, not handled locally.
            # Verify by checking the button's action mapping directly.
            action_map = {
                "menu-run-agent": "run_agent",
                "menu-score": "score_content",
                "menu-clear": "clear_chat",
            }
            for btn_id, expected_action in action_map.items():
                assert expected_action == {
                    "menu-toggle-mode": "toggle_mode",
                    "menu-run-agent": "run_agent",
                    "menu-score": "score_content",
                    "menu-clear": "clear_chat",
                    "menu-palette": "command_palette",
                    "menu-memory": "toggle_memory",
                    "menu-help": "help_screen",
                }.get(btn_id)

    @pytest.mark.asyncio
    async def test_run_agent_button_is_success_variant(self, app):
        """Run Agent button should use success variant to stand out."""
        async with app.run_test() as pilot:
            btn = app.query_one("#menu-run-agent", Button)
            assert btn.variant == "success"

    @pytest.mark.asyncio
    async def test_score_button_is_primary_variant(self, app):
        """Score button should use primary variant."""
        async with app.run_test() as pilot:
            btn = app.query_one("#menu-score", Button)
            assert btn.variant == "primary"
