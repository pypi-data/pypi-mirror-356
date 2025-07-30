"""Pytest plugin to hook Mini Agent Harness into the test runner."""

import pytest

from .fixtures import agent_fixture, Replay



def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--llm-live",
        action="store_true",
        default=False,
        help="Run tests against live language model instead of replay cache.",
    )


@pytest.fixture

def replay(request: pytest.FixtureRequest):
    """Provide a shared Replay instance for a test run."""
    live = bool(request.config.getoption("--llm-live"))
    return Replay(enabled=not live)


# Re-export common fixtures for convenience so tests can simply import
# `agent_fixture` from the plugin path via pytest's auto-discovery.
@pytest.fixture

def agent(request: pytest.FixtureRequest):
    """Default agent fixture that loads ./agents/quickstart.yaml."""
    return agent_fixture("agents/quickstart.yaml")


__all__ = ["agent_fixture", "Replay"] 