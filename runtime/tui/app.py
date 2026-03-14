"""CD Agency Studio — main TUI application."""

from __future__ import annotations

from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import Footer, Header, Static, TabbedContent, TabPane
from textual.worker import Worker

from runtime.agent import Agent, AgentOutput
from runtime.tui.widgets.agent_browser import AgentBrowser, AgentSelected
from runtime.tui.widgets.agent_output import AgentOutputPanel, OutputAccepted
from runtime.tui.widgets.chat_panel import (
    AcceptRequested,
    ChatMessageSent,
    ChatPanel,
    ScoreRequested,
)
from runtime.tui.widgets.command_palette import StudioCommandProvider
from runtime.tui.widgets.content_editor import ContentChanged, ContentEditor
from runtime.tui.widgets.memory_panel import MemoryPanel
from runtime.tui.widgets.scoring_panel import ScoringPanel
from runtime.tui.widgets.status_bar import StatusBar


class HelpScreen(ModalScreen):
    """Modal help overlay showing all keyboard shortcuts."""

    DEFAULT_CSS = """
    HelpScreen {
        align: center middle;
    }
    HelpScreen #help-dialog {
        width: 60;
        max-height: 80%;
        background: $surface;
        border: thick $primary;
        padding: 2 4;
    }
    HelpScreen .help-title {
        text-align: center;
        text-style: bold;
        padding: 0 0 1 0;
    }
    HelpScreen .help-section {
        padding: 1 0 0 0;
        text-style: bold;
        color: $accent;
    }
    HelpScreen .help-row {
        padding: 0 0 0 2;
    }
    HelpScreen .help-footer {
        text-align: center;
        color: $text-muted;
        padding: 1 0 0 0;
    }
    """

    BINDINGS = [
        Binding("escape", "dismiss", "Close", show=True),
        Binding("f1", "dismiss", "Close", show=False),
    ]

    def compose(self) -> ComposeResult:
        with Vertical(id="help-dialog"):
            yield Static("CD Agency Studio — Keyboard Shortcuts", classes="help-title")
            yield Static("Navigation", classes="help-section")
            yield Static("  Ctrl+P     Command palette", classes="help-row")
            yield Static("  Ctrl+O     Toggle Chat / Form mode", classes="help-row")
            yield Static("  Ctrl+B     Toggle agent sidebar", classes="help-row")
            yield Static("  Ctrl+Y     Toggle memory panel", classes="help-row")
            yield Static("  Escape     Dismiss panels / close dialogs", classes="help-row")
            yield Static("Actions", classes="help-section")
            yield Static("  Ctrl+R     Run agent on current content", classes="help-row")
            yield Static("  Ctrl+S     Score current content", classes="help-row")
            yield Static("  Ctrl+L     Clear chat history", classes="help-row")
            yield Static("  Enter      Send message (in chat mode)", classes="help-row")
            yield Static("General", classes="help-section")
            yield Static("  F1         Show / close this help", classes="help-row")
            yield Static("  Ctrl+Q     Quit", classes="help-row")
            yield Static("Press Escape or F1 to close", classes="help-footer")


class StudioApp(App):
    """Interactive content design studio."""

    TITLE = "CD Agency Studio"
    CSS = """
    Screen {
        layout: grid;
        grid-size: 3;
        grid-columns: auto 1fr auto;
        grid-rows: 1fr auto;
    }
    #center-panel {
        column-span: 1;
    }
    #mode-tabs {
        height: 1fr;
    }
    """

    BINDINGS = [
        Binding("ctrl+p", "command_palette", "Commands", show=True),
        Binding("ctrl+b", "toggle_sidebar", "Sidebar", show=True),
        Binding("ctrl+y", "toggle_memory", "Memory", show=True),
        Binding("ctrl+o", "toggle_mode", "Chat/Form", show=True),
        Binding("ctrl+r", "run_agent", "Run", show=True),
        Binding("ctrl+s", "score_content", "Score", show=True),
        Binding("ctrl+l", "clear_chat", "Clear", show=True),
        Binding("escape", "dismiss_panels", "Back", show=False),
        Binding("f1", "help_screen", "Help", show=True),
        Binding("ctrl+q", "quit", "Quit", show=True),
    ]

    COMMANDS = {StudioCommandProvider}

    def __init__(
        self,
        preset: str | None = None,
        initial_content: str | None = None,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self._preset_name = preset or "default"
        self._initial_content = initial_content or ""
        self._current_agent: Agent | None = None
        self._agents: list[Agent] = []
        self._total_tokens: int = 0
        self._score_timer = None

    def compose(self) -> ComposeResult:
        yield Header()
        yield AgentBrowser(id="agent-browser")
        yield MemoryPanel(id="memory-panel")
        with Vertical(id="center-panel"):
            with TabbedContent(id="mode-tabs"):
                with TabPane("Chat", id="chat-tab"):
                    yield ChatPanel(id="chat-panel")
                with TabPane("Form", id="form-tab"):
                    yield ContentEditor(
                        initial_content=self._initial_content, id="content-editor"
                    )
                    yield AgentOutputPanel(id="agent-output")
        yield ScoringPanel(id="scoring-panel")
        yield StatusBar(id="status-bar")
        yield Footer()

    def on_mount(self) -> None:
        """Initialize app state from existing runtime modules."""
        self._load_agents()
        self._load_memory()
        status = self.query_one("#status-bar", StatusBar)
        status.set_preset(self._preset_name)
        status.set_mode("Chat")

    def _load_agents(self) -> None:
        """Load agents from the content-design directory."""
        try:
            from runtime.config import Config
            from runtime.registry import AgentRegistry

            config = Config.from_env()
            registry = AgentRegistry.from_directory(config.agents_dir)
            self._agents = registry.list_all()
            browser = self.query_one("#agent-browser", AgentBrowser)
            browser.set_agents(self._agents)
        except Exception:
            self._agents = []

    def _load_memory(self) -> None:
        """Load project memory."""
        try:
            from runtime.memory import ProjectMemory

            memory = ProjectMemory.load()
            self.query_one("#memory-panel", MemoryPanel).set_memory(memory)
            self.query_one("#status-bar", StatusBar).set_memory_count(
                len(memory.entries)
            )
        except Exception:
            pass

    # --- Agent selection ---

    def on_agent_selected(self, event: AgentSelected) -> None:
        """Handle agent selection from browser or command palette."""
        self.select_agent(event.agent)

    def select_agent(self, agent: Agent) -> None:
        """Set the active agent."""
        self._current_agent = agent
        self.query_one("#status-bar", StatusBar).set_agent(agent.name)
        # Clear chat when switching agents
        self.query_one("#chat-panel", ChatPanel).clear_chat()

    # --- Chat mode ---

    def on_chat_message_sent(self, event: ChatMessageSent) -> None:
        """Handle a chat message from the user."""
        if not self._current_agent:
            chat = self.query_one("#chat-panel", ChatPanel)
            chat.add_agent_message(
                "Please select an agent first (use the sidebar or Ctrl+P)."
            )
            return

        chat = self.query_one("#chat-panel", ChatPanel)
        chat.set_loading(True)
        self._run_conversation()

    def _run_conversation(self) -> None:
        """Run agent conversation in a background worker."""
        self.run_worker(
            self._conversation_worker,
            name="conversation",
            exclusive=True,
            thread=True,
        )

    def _conversation_worker(self) -> AgentOutput:
        """Execute multi-turn conversation (runs in thread)."""
        from runtime.config import Config
        from runtime.runner import AgentRunner

        chat = self.query_one("#chat-panel", ChatPanel)
        messages = chat.messages

        runner = AgentRunner(Config.from_env())
        return runner.run_conversation(self._current_agent, messages)

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        """Handle worker completion."""
        if event.worker.name == "conversation" and event.worker.state.name == "SUCCESS":
            result: AgentOutput = event.worker.result
            chat = self.query_one("#chat-panel", ChatPanel)
            chat.set_loading(False)
            chat.add_agent_message(result.content)
            self._total_tokens += result.input_tokens + result.output_tokens
            self.query_one("#status-bar", StatusBar).set_tokens(self._total_tokens)
        elif event.worker.name == "conversation" and event.worker.state.name == "ERROR":
            chat = self.query_one("#chat-panel", ChatPanel)
            chat.set_loading(False)
            error = str(event.worker.error) if event.worker.error else "Unknown error"
            chat.add_agent_message(f"[red]Error: {error}[/red]")
        elif event.worker.name == "form-run" and event.worker.state.name == "SUCCESS":
            result: AgentOutput = event.worker.result
            output_panel = self.query_one("#agent-output", AgentOutputPanel)
            editor = self.query_one("#content-editor", ContentEditor)
            output_panel.show_output(result.content, input_text=editor.text)
            self._total_tokens += result.input_tokens + result.output_tokens
            self.query_one("#status-bar", StatusBar).set_tokens(self._total_tokens)
        elif event.worker.name == "form-run" and event.worker.state.name == "ERROR":
            output_panel = self.query_one("#agent-output", AgentOutputPanel)
            error = str(event.worker.error) if event.worker.error else "Unknown error"
            output_panel.show_output(f"[red]Error: {error}[/red]")

    # --- Form mode ---

    def on_content_changed(self, event: ContentChanged) -> None:
        """Handle content editor changes — debounce scoring updates."""
        if self._score_timer:
            self._score_timer.stop()
        self._score_timer = self.set_timer(
            0.3, lambda: self._update_scores(event.text)
        )

    def _update_scores(self, text: str) -> None:
        """Update the scoring panel with new text."""
        self.query_one("#scoring-panel", ScoringPanel).update_scores(text)

    # --- Score from chat ---

    def on_score_requested(self, event: ScoreRequested) -> None:
        """Score content from a chat message."""
        self._update_scores(event.text)

    # --- Accept output ---

    def on_accept_requested(self, event: AcceptRequested) -> None:
        """Copy accepted chat content to the form editor."""
        editor = self.query_one("#content-editor", ContentEditor)
        editor.text = event.text

    def on_output_accepted(self, event: OutputAccepted) -> None:
        """Copy accepted form output to the editor."""
        editor = self.query_one("#content-editor", ContentEditor)
        editor.text = event.text

    # --- Key bindings ---

    def action_toggle_sidebar(self) -> None:
        """Toggle the agent browser sidebar."""
        browser = self.query_one("#agent-browser", AgentBrowser)
        browser.display = not browser.display

    def action_toggle_memory(self) -> None:
        """Toggle between agent browser and memory panel."""
        browser = self.query_one("#agent-browser", AgentBrowser)
        memory = self.query_one("#memory-panel", MemoryPanel)
        if memory.display:
            memory.display = False
            browser.display = True
        else:
            browser.display = False
            memory.display = True

    def action_toggle_mode(self) -> None:
        """Toggle between Chat and Form mode."""
        tabs = self.query_one("#mode-tabs", TabbedContent)
        status = self.query_one("#status-bar", StatusBar)
        if tabs.active == "chat-tab":
            tabs.active = "form-tab"
            status.set_mode("Form")
        else:
            tabs.active = "chat-tab"
            status.set_mode("Chat")

    def action_run_agent(self) -> None:
        """Run the current agent on form editor content."""
        if not self._current_agent:
            chat = self.query_one("#chat-panel", ChatPanel)
            chat.add_agent_message(
                "Please select an agent first (use the sidebar or Ctrl+P)."
            )
            return
        editor = self.query_one("#content-editor", ContentEditor)
        text = editor.text.strip()
        if not text:
            return
        output_panel = self.query_one("#agent-output", AgentOutputPanel)
        output_panel.show_loading()
        self.run_worker(
            self._form_run_worker,
            name="form-run",
            exclusive=True,
            thread=True,
        )

    def _form_run_worker(self) -> AgentOutput:
        """Execute agent on form content (runs in thread)."""
        from runtime.config import Config
        from runtime.runner import AgentRunner

        editor = self.query_one("#content-editor", ContentEditor)
        runner = AgentRunner(Config.from_env())
        return runner.run(self._current_agent, editor.text)

    def action_score_content(self) -> None:
        """Score the current content (form editor or last chat message)."""
        editor = self.query_one("#content-editor", ContentEditor)
        text = editor.text.strip()
        if text:
            self._update_scores(text)

    def action_clear_chat(self) -> None:
        """Clear the chat history."""
        self.query_one("#chat-panel", ChatPanel).clear_chat()

    def action_dismiss_panels(self) -> None:
        """Dismiss open panels — close memory if open, otherwise close sidebar."""
        memory = self.query_one("#memory-panel", MemoryPanel)
        if memory.display:
            memory.display = False
            self.query_one("#agent-browser", AgentBrowser).display = True
            return
        browser = self.query_one("#agent-browser", AgentBrowser)
        if not browser.display:
            browser.display = True

    def action_help_screen(self) -> None:
        """Show modal help screen."""
        self.push_screen(HelpScreen())

    # --- Command palette callbacks ---

    def switch_preset(self, preset: str) -> None:
        """Switch the active design system preset."""
        self._preset_name = preset
        self.query_one("#status-bar", StatusBar).set_preset(preset)

    def switch_mode_to(self, mode: str) -> None:
        """Switch to a specific mode."""
        tabs = self.query_one("#mode-tabs", TabbedContent)
        status = self.query_one("#status-bar", StatusBar)
        if mode == "Chat":
            tabs.active = "chat-tab"
        else:
            tabs.active = "form-tab"
        status.set_mode(mode)

    def run_action_command(self, action: str) -> None:
        """Execute a named action from the command palette."""
        if action == "Clear Chat":
            self.query_one("#chat-panel", ChatPanel).clear_chat()
        elif action == "Score Content":
            editor = self.query_one("#content-editor", ContentEditor)
            self._update_scores(editor.text)
        elif action == "Toggle Memory":
            self.action_toggle_memory()
