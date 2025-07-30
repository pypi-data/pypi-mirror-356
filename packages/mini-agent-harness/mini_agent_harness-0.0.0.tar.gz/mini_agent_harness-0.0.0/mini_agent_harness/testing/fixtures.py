"""Pytest fixtures and utilities for Mini Agent Harness."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from ..core import Agent, AgentResult


class Replay:
    """Very simple replay/cache stub.

    In a future version this will record and replay LLM calls to avoid flaky
    tests. For now it is a no-op wrapper that just forwards through.
    """

    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self._cache: dict[str, AgentResult] = {}

    def record(self, prompt: str, result: AgentResult) -> None:
        if self.enabled:
            self._cache[prompt] = result

    def fetch(self, prompt: str) -> AgentResult | None:
        return self._cache.get(prompt)


def _load_agent_yaml(yaml_path: str | Path) -> dict[str, Any]:
    path = Path(yaml_path)
    if not path.exists():
        raise FileNotFoundError(f"Agent manifest not found: {yaml_path}")
    return yaml.safe_load(path.read_text())


def agent_fixture(yaml_path: str | Path):
    """Load an agent manifest and return a ready-to-run Agent instance.

    Usage in tests::

        from mini_agent_harness.testing import agent_fixture
        
        booking_agent = agent_fixture("agents/booking.yaml")
        result = booking_agent.run("Some prompt")
    """

    manifest = _load_agent_yaml(yaml_path)
    return Agent(manifest) 