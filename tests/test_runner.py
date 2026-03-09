"""Tests for the AgentRunner (mocked, no real API calls)."""

from unittest.mock import MagicMock, patch

import pytest

from runtime.agent import Agent, AgentInput, AgentOutput
from runtime.config import Config
from runtime.runner import AgentRunner


@pytest.fixture
def mock_config() -> Config:
    return Config(api_key="test-key", model="test-model")


@pytest.fixture
def sample_agent() -> Agent:
    return Agent(
        name="Test Agent",
        description="A test agent",
        inputs=[
            AgentInput(name="content", type="string", required=True, description="Input text"),
        ],
        system_prompt="You are a test agent.",
        critical_rules="- Be concise",
        source_file="test-agent.md",
    )


class TestAgentRunner:
    def test_validates_missing_input(self, mock_config: Config, sample_agent: Agent):
        runner = AgentRunner(mock_config)
        with pytest.raises(ValueError, match="Missing required input"):
            runner.run(sample_agent, {})

    def test_validates_empty_input(self, mock_config: Config, sample_agent: Agent):
        runner = AgentRunner(mock_config)
        with pytest.raises(ValueError, match="Empty required input"):
            runner.run(sample_agent, {"content": ""})

    @patch("runtime.runner.anthropic.Anthropic")
    def test_run_success(self, mock_anthropic_cls: MagicMock, mock_config: Config, sample_agent: Agent):
        # Build mock response
        mock_text_block = MagicMock()
        mock_text_block.type = "text"
        mock_text_block.text = "Here is the improved content."

        mock_usage = MagicMock()
        mock_usage.input_tokens = 100
        mock_usage.output_tokens = 50

        mock_response = MagicMock()
        mock_response.content = [mock_text_block]
        mock_response.usage = mock_usage

        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_response
        mock_anthropic_cls.return_value = mock_client

        runner = AgentRunner(mock_config)
        result = runner.run(sample_agent, {"content": "Fix this button label"})

        assert isinstance(result, AgentOutput)
        assert result.content == "Here is the improved content."
        assert result.agent_name == "Test Agent"
        assert result.input_tokens == 100
        assert result.output_tokens == 50
        assert result.latency_ms > 0

        # Verify the API was called with correct parameters
        call_kwargs = mock_client.messages.create.call_args.kwargs
        assert call_kwargs["model"] == "test-model"
        assert "You are a test agent" in call_kwargs["system"]
        assert call_kwargs["messages"][0]["role"] == "user"

    @patch("runtime.runner.anthropic.Anthropic")
    def test_run_with_model_override(self, mock_anthropic_cls: MagicMock, mock_config: Config, sample_agent: Agent):
        mock_text_block = MagicMock()
        mock_text_block.type = "text"
        mock_text_block.text = "Result"

        mock_response = MagicMock()
        mock_response.content = [mock_text_block]
        mock_response.usage = MagicMock(input_tokens=10, output_tokens=5)

        mock_client = MagicMock()
        mock_client.messages.create.return_value = mock_response
        mock_anthropic_cls.return_value = mock_client

        runner = AgentRunner(mock_config)
        result = runner.run(sample_agent, {"content": "test"}, model="claude-opus-4-6")

        call_kwargs = mock_client.messages.create.call_args.kwargs
        assert call_kwargs["model"] == "claude-opus-4-6"

    def test_system_message_composition(self, sample_agent: Agent):
        msg = sample_agent.build_system_message()
        assert "You are a test agent." in msg
        assert "Be concise" in msg

    def test_user_message_composition(self, sample_agent: Agent):
        msg = sample_agent.build_user_message({"content": "Fix my button"})
        assert "Fix my button" in msg
