"""Sidebar menu — clickable action items for common studio operations."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Button, Label, Rule, Static


class MenuAction(Message):
    """Posted when a sidebar menu item is clicked."""

    def __init__(self, action: str) -> None:
        super().__init__()
        self.action = action


class SidebarMenu(Widget):
    """Quick-access menu with labeled action buttons for the sidebar."""

    DEFAULT_CSS = """
    SidebarMenu {
        height: auto;
        padding: 0 0 1 0;
    }
    SidebarMenu .menu-section {
        color: $accent;
        text-style: bold;
        padding: 1 0 0 0;
    }
    SidebarMenu .menu-btn {
        width: 100%;
        min-width: 16;
        height: 1;
        margin: 0;
        text-style: bold;
    }
    SidebarMenu .menu-hint {
        color: $text-muted;
        text-align: right;
        padding: 0;
        height: 1;
    }
    SidebarMenu .menu-row {
        height: 1;
        layout: horizontal;
    }
    SidebarMenu .menu-row .menu-btn {
        width: 1fr;
    }
    SidebarMenu .menu-row .menu-hint {
        width: auto;
        min-width: 6;
    }
    SidebarMenu #preset-label {
        color: $text;
        padding: 0 0 0 1;
        height: 1;
    }
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self._current_mode: str = "Chat"
        self._current_preset: str = "default"

    def compose(self) -> ComposeResult:
        yield Static("MODE", classes="menu-section")
        with Horizontal_Row("menu-row"):
            yield Button("Chat/Form", id="menu-toggle-mode", classes="menu-btn", variant="default")
            yield Static("^O", classes="menu-hint")

        yield Static("ACTIONS", classes="menu-section")
        with Horizontal_Row("menu-row"):
            yield Button("Run Agent", id="menu-run-agent", classes="menu-btn", variant="success")
            yield Static("^R", classes="menu-hint")
        with Horizontal_Row("menu-row"):
            yield Button("Score", id="menu-score", classes="menu-btn", variant="primary")
            yield Static("^S", classes="menu-hint")
        with Horizontal_Row("menu-row"):
            yield Button("Clear Chat", id="menu-clear", classes="menu-btn", variant="default")
            yield Static("^L", classes="menu-hint")
        with Horizontal_Row("menu-row"):
            yield Button("Commands", id="menu-palette", classes="menu-btn", variant="default")
            yield Static("^P", classes="menu-hint")

        yield Static("PRESET", classes="menu-section")
        yield Button("Material Design", id="menu-preset-material", classes="menu-btn", variant="default")
        yield Button("Apple HIG", id="menu-preset-apple", classes="menu-btn", variant="default")
        yield Button("Polaris", id="menu-preset-polaris", classes="menu-btn", variant="default")
        yield Button("Atlassian", id="menu-preset-atlassian", classes="menu-btn", variant="default")

        yield Static("VIEW", classes="menu-section")
        with Horizontal_Row("menu-row"):
            yield Button("Memory", id="menu-memory", classes="menu-btn", variant="default")
            yield Static("^Y", classes="menu-hint")
        with Horizontal_Row("menu-row"):
            yield Button("Help", id="menu-help", classes="menu-btn", variant="default")
            yield Static("F1", classes="menu-hint")

        yield Rule()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        action_map = {
            "menu-toggle-mode": "toggle_mode",
            "menu-run-agent": "run_agent",
            "menu-score": "score_content",
            "menu-clear": "clear_chat",
            "menu-palette": "command_palette",
            "menu-memory": "toggle_memory",
            "menu-help": "help_screen",
            "menu-preset-material": "preset:Material Design",
            "menu-preset-apple": "preset:Apple HIG",
            "menu-preset-polaris": "preset:Polaris",
            "menu-preset-atlassian": "preset:Atlassian",
        }
        action = action_map.get(event.button.id)
        if action:
            self.post_message(MenuAction(action))

    def set_mode(self, mode: str) -> None:
        """Update mode display on the toggle button."""
        self._current_mode = mode
        try:
            btn = self.query_one("#menu-toggle-mode", Button)
            btn.label = f"Mode: {mode}"
        except Exception:
            pass

    def set_preset(self, preset: str) -> None:
        """Highlight the active preset button."""
        self._current_preset = preset
        preset_ids = {
            "Material Design": "menu-preset-material",
            "Apple HIG": "menu-preset-apple",
            "Polaris": "menu-preset-polaris",
            "Atlassian": "menu-preset-atlassian",
        }
        for name, btn_id in preset_ids.items():
            try:
                btn = self.query_one(f"#{btn_id}", Button)
                btn.variant = "primary" if name == preset else "default"
            except Exception:
                pass


class Horizontal_Row(Widget):
    """Simple horizontal container for menu rows."""

    DEFAULT_CSS = """
    Horizontal_Row {
        height: 1;
        layout: horizontal;
    }
    """

    def __init__(self, classes: str = "", **kwargs) -> None:
        super().__init__(classes=classes, **kwargs)
