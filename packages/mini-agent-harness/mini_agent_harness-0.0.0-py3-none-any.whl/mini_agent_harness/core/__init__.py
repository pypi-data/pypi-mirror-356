"""Core components of Mini Agent Harness.

For now this only exposes a stub Agent that simply echoes the input. The
real implementation will follow a proper tool-calling loop.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AgentResult:
    """Simple result wrapper mimicking an LLM agent response."""

    response_text: str

    # TODO: include metadata such as traces, tool calls, etc.


class Agent:
    """Extremely naive stub agent.

    Parameters
    ----------
    manifest : dict
        Parsed YAML manifest for the agent.
    """

    def __init__(self, manifest: dict):
        self.manifest = manifest

    def run(self, input_text: str) -> AgentResult:
        return AgentResult(response_text=f"[STUB-AGENT] {input_text}") 