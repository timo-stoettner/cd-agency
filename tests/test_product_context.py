"""Tests for the ProductContext feature."""

from __future__ import annotations

import pytest

from runtime.config import ProductContext, Config


class TestProductContext:
    def test_default_not_configured(self):
        ctx = ProductContext()
        assert not ctx.is_configured()

    def test_is_configured_with_product_name(self):
        ctx = ProductContext(product_name="Acme App")
        assert ctx.is_configured()

    def test_is_configured_with_domain(self):
        ctx = ProductContext(domain="fintech")
        assert ctx.is_configured()

    def test_is_configured_with_description(self):
        ctx = ProductContext(description="A billing tool")
        assert ctx.is_configured()

    def test_build_context_block_empty(self):
        ctx = ProductContext()
        assert ctx.build_context_block() == ""

    def test_build_context_block_full(self):
        ctx = ProductContext(
            product_name="Acme App",
            description="A billing tool for freelancers",
            domain="fintech",
            audience="freelancers and small businesses",
            tone="professional but friendly",
            platform="web app",
            guidelines=["no jargon", "use active voice"],
        )
        block = ctx.build_context_block()
        assert "## Product Context" in block
        assert "Acme App" in block
        assert "billing tool for freelancers" in block
        assert "fintech" in block
        assert "freelancers and small businesses" in block
        assert "professional but friendly" in block
        assert "web app" in block
        assert "no jargon" in block
        assert "use active voice" in block
        assert "tailor all suggestions" in block

    def test_build_context_block_partial(self):
        ctx = ProductContext(product_name="MyApp", domain="healthcare")
        block = ctx.build_context_block()
        assert "MyApp" in block
        assert "healthcare" in block
        assert "Audience" not in block  # not set

    def test_from_dict(self):
        data = {
            "product_name": "TestApp",
            "domain": "e-commerce",
            "audience": "shoppers",
            "guidelines": ["be concise"],
        }
        ctx = ProductContext.from_dict(data)
        assert ctx.product_name == "TestApp"
        assert ctx.domain == "e-commerce"
        assert ctx.audience == "shoppers"
        assert ctx.guidelines == ["be concise"]
        assert ctx.tone == ""  # not in data

    def test_from_dict_empty(self):
        ctx = ProductContext.from_dict({})
        assert not ctx.is_configured()

    def test_to_dict(self):
        ctx = ProductContext(
            product_name="Acme",
            domain="SaaS",
            guidelines=["no jargon"],
        )
        d = ctx.to_dict()
        assert d["product_name"] == "Acme"
        assert d["domain"] == "SaaS"
        assert d["guidelines"] == ["no jargon"]
        # Empty fields should not be in dict
        assert "tone" not in d
        assert "audience" not in d

    def test_to_dict_empty(self):
        ctx = ProductContext()
        assert ctx.to_dict() == {}

    def test_roundtrip(self):
        original = ProductContext(
            product_name="RoundTrip",
            description="A test",
            domain="testing",
            audience="testers",
            tone="casual",
            platform="CLI",
            guidelines=["rule 1", "rule 2"],
        )
        restored = ProductContext.from_dict(original.to_dict())
        assert restored.product_name == original.product_name
        assert restored.description == original.description
        assert restored.domain == original.domain
        assert restored.audience == original.audience
        assert restored.tone == original.tone
        assert restored.platform == original.platform
        assert restored.guidelines == original.guidelines


class TestConfigWithProductContext:
    def test_config_default_product_context(self):
        config = Config()
        assert not config.product_context.is_configured()

    def test_config_with_product_context(self):
        ctx = ProductContext(product_name="Test", domain="testing")
        config = Config(product_context=ctx)
        assert config.product_context.is_configured()
        assert config.product_context.product_name == "Test"

    def test_config_from_env_loads_product_context(self, tmp_path, monkeypatch):
        """Test that Config.from_env() reads product_context from YAML."""
        config_file = tmp_path / ".cd-agency.yaml"
        config_file.write_text(
            "product_context:\n"
            "  product_name: YAML App\n"
            "  domain: healthcare\n"
            "  audience: doctors\n"
        )
        # Point to the temp dir for config file discovery
        monkeypatch.chdir(tmp_path)
        # Create a dummy agents dir so validation doesn't complain
        (tmp_path / "content-design").mkdir()

        config = Config.from_env()
        assert config.product_context.product_name == "YAML App"
        assert config.product_context.domain == "healthcare"
        assert config.product_context.audience == "doctors"

    def test_config_from_env_no_product_context(self, tmp_path, monkeypatch):
        """Config without product_context section still works."""
        config_file = tmp_path / ".cd-agency.yaml"
        config_file.write_text("model: test-model\n")
        monkeypatch.chdir(tmp_path)
        (tmp_path / "content-design").mkdir()

        config = Config.from_env()
        assert not config.product_context.is_configured()
