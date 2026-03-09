"""Tests for the Agent model."""

import pytest

from runtime.agent import Agent, AgentInput, OutputField


@pytest.fixture
def sample_agent() -> Agent:
    return Agent(
        name="Test Agent",
        description="A test agent",
        tags=["test", "sample"],
        inputs=[
            AgentInput(name="content", type="string", required=True, description="The content"),
            AgentInput(name="tone", type="string", required=False, description="Desired tone"),
        ],
        outputs=[
            OutputField(name="result", type="string", description="The result"),
        ],
        related_agents=["other-agent"],
        system_prompt="You are a test agent. Be helpful.",
        few_shot_examples="**Example 1:** Input: hello → Output: world",
        critical_rules="- Be concise\n- Be clear",
        source_file="content-design/test-agent.md",
    )


class TestAgent:
    def test_slug_from_source_file(self, sample_agent: Agent):
        assert sample_agent.slug == "test-agent"

    def test_slug_without_source_file(self):
        agent = Agent(name="My Cool Agent", description="test")
        assert agent.slug == "my-cool-agent"

    def test_validate_input_passes_with_required(self, sample_agent: Agent):
        errors = sample_agent.validate_input({"content": "hello"})
        assert errors == []

    def test_validate_input_fails_missing_required(self, sample_agent: Agent):
        errors = sample_agent.validate_input({})
        assert len(errors) == 1
        assert "content" in errors[0]

    def test_validate_input_fails_empty_required(self, sample_agent: Agent):
        errors = sample_agent.validate_input({"content": ""})
        assert len(errors) == 1

    def test_validate_input_optional_not_required(self, sample_agent: Agent):
        errors = sample_agent.validate_input({"content": "hello"})
        assert errors == []  # "tone" is optional, shouldn't error

    def test_build_system_message(self, sample_agent: Agent):
        msg = sample_agent.build_system_message()
        assert "You are a test agent" in msg
        assert "Example 1" in msg
        assert "Be concise" in msg

    def test_build_user_message(self, sample_agent: Agent):
        msg = sample_agent.build_user_message({"content": "Fix this button", "tone": "friendly"})
        assert "Fix this button" in msg
        assert "friendly" in msg

    def test_build_user_message_skips_empty(self, sample_agent: Agent):
        msg = sample_agent.build_user_message({"content": "hello", "tone": ""})
        assert "Tone" not in msg

    def test_get_required_inputs(self, sample_agent: Agent):
        required = sample_agent.get_required_inputs()
        assert len(required) == 1
        assert required[0].name == "content"

    def test_get_optional_inputs(self, sample_agent: Agent):
        optional = sample_agent.get_optional_inputs()
        assert len(optional) == 1
        assert optional[0].name == "tone"

    def test_repr(self, sample_agent: Agent):
        r = repr(sample_agent)
        assert "Test Agent" in r
        assert "test-agent" in r
