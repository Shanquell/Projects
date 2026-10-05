"""
llm.py — the thin layer between a persona and a model.

Everything in this package that needs to "think" goes through the `LLM`
protocol below. There are two implementations:

    ClaudeLLM    real Claude calls. Needs ANTHROPIC_API_KEY.
    ScriptedLLM  returns canned strings. No key, no network, no cost.

That split is deliberate and it is the reason this project is testable. The
unit tests in `tests/` inject a ScriptedLLM, so they run in milliseconds for
free, and `main.py --offline` uses one too so you can see the whole app work
before you have configured anything.

ClaudeLLM also provides complete_with_tools(). This is used by the
orchestrator when real Claude tool calling is required. Unlike complete(),
complete_with_tools() returns the full Anthropic response so the orchestrator
can inspect tool_use blocks, tool IDs, tool inputs, and stop_reason.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Protocol


# Claude Opus 5 is the most capable model. While you are iterating you may want
# "claude-haiku-4-5" — a persona conversation makes one call per turn, and those
# add up. Say which model produced your submitted transcripts.
DEFAULT_MODEL = "claude-opus-5"


class LLM(Protocol):
    """
    Anything that can turn a system prompt plus a transcript into a reply.

    Normal persona/agent calls use complete(), which returns text.

    The orchestrator can use complete_with_tools(), which returns the full
    structured model response so real tool calls can be executed by Python.
    """

    def complete(
        self,
        system: str,
        messages: List[Dict[str, Any]],
        max_tokens: int = 2048,
    ) -> str:
        ...

    def complete_with_tools(
        self,
        system: str,
        messages: List[Dict[str, Any]],
        tools: List[Dict[str, Any]],
        max_tokens: int = 2048,
    ) -> Any:
        ...


# =============================================================================
# ⚠️  NEEDS YOUR OWN API KEY
# =============================================================================
# REQUIRES A KEY. ClaudeLLM is every real model call in this package. Without
# ANTHROPIC_API_KEY it raises with instructions rather than failing quietly.
#
# Put your key in `.env`:
#
#     ANTHROPIC_API_KEY=your-real-key
#
# Calls are billed to you. A persona conversation costs one model call per
# turn, plus calls for persona creation and orchestration.
#
# You do not need a key for normal offline testing:
#
#     uv run pytest
#     uv run python main.py --offline
#
# =============================================================================


@dataclass
class ClaudeLLM:
    """
    Real Claude implementation.

    complete()
        Used for normal text generation such as persona creation and
        persona conversation turns.

    complete_with_tools()
        Used by the orchestrator. It returns the complete Anthropic
        response rather than flattening the response into text. This allows
        the orchestrator to inspect and execute real tool_use blocks.

    The client is created lazily so importing this module never requires
    an API key.
    """

    model: str = DEFAULT_MODEL
    _client: Any = field(default=None, repr=False)

    def _get_client(self) -> Any:
        """
        Create and return the Anthropic client.

        The client is created only when it is first needed.
        """

        if self._client is None:
            import anthropic

            if not os.getenv("ANTHROPIC_API_KEY"):
                raise RuntimeError(
                    "ANTHROPIC_API_KEY is not set. "
                    "Copy .env.example to .env and add your key, "
                    "or run in offline mode: "
                    "uv run python main.py --offline"
                )

            self._client = anthropic.Anthropic()

        return self._client

    def complete(
        self,
        system: str,
        messages: List[Dict[str, Any]],
        max_tokens: int = 2048,
    ) -> str:
        """
        Send a normal text-generation request.

        This method intentionally returns only text because persona.py,
        agent.py, and conversation.py expect a string response.
        """

        response = self._get_client().messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system,
            messages=messages,
        )

        # Claude may decline a request. In that case return a simple
        # string instead of causing the rest of PersonaForge to crash.
        if response.stop_reason == "refusal":
            return "[declined to respond]"

        return "".join(
            block.text
            for block in response.content
            if block.type == "text"
        ).strip()

    def complete_with_tools(
        self,
        system: str,
        messages: List[Dict[str, Any]],
        tools: List[Dict[str, Any]],
        max_tokens: int = 2048,
    ) -> Any:
        """
        Send a request with Claude tool calling enabled.

        IMPORTANT:
        Do not convert this response to a string.

        The orchestrator needs the complete response so it can inspect:

            response.stop_reason

        and blocks such as:

            block.type
            block.name
            block.input
            block.id

        When block.type == "tool_use", the orchestrator executes the
        corresponding Python function and returns a tool_result to Claude.
        """

        response = self._get_client().messages.create(
            model=self.model,
            max_tokens=max_tokens,
            system=system,
            messages=messages,
            tools=tools,
        )

        return response


@dataclass
class ScriptedLLM:
    """
    A fake model that replays a fixed list of replies, then loops.

    Used by unit tests. It records every call it receives in `.calls`,
    which makes it easy for tests to verify what was sent to the model.

    ScriptedLLM does not contact Anthropic and therefore has no API cost.
    """

    replies: List[str] = field(
        default_factory=lambda: ["(scripted reply)"]
    )

    calls: List[Dict[str, Any]] = field(
        default_factory=list
    )

    def complete(
        self,
        system: str,
        messages: List[Dict[str, Any]],
        max_tokens: int = 2048,
    ) -> str:
        """
        Return the next scripted text response.
        """

        self.calls.append(
            {
                "system": system,
                "messages": list(messages),
                "max_tokens": max_tokens,
            }
        )

        return self.replies[
            (len(self.calls) - 1) % len(self.replies)
        ]

    def complete_with_tools(
        self,
        system: str,
        messages: List[Dict[str, Any]],
        tools: List[Dict[str, Any]],
        max_tokens: int = 2048,
    ) -> Any:
        """
        Record a tool-enabled request without making a network call.

        The existing ScriptedLLM is primarily designed for text-generation
        tests. It does not attempt to imitate Anthropic's complete tool-use
        response format.

        More advanced orchestrator tests can inject their own fake LLM
        containing predetermined tool_use responses.
        """

        self.calls.append(
            {
                "system": system,
                "messages": list(messages),
                "tools": tools,
                "max_tokens": max_tokens,
            }
        )

        return None


# =============================================================================
# Offline demo data
# =============================================================================


_DEMO_DIALOGUE = [
    "I understand. Could you tell me more about when the symptoms started?",
    "That has been going on for about three weeks now, mostly in the mornings.",
    "Have you noticed anything that makes it better or worse?",
    "Coffee seems to make it worse, and lying down helps a little.",
    "Thank you, that is useful. I would like to run a couple of tests.",
    "Whatever you think is best, doctor. I just want to feel normal again.",
]


_DEMO_PERSONA = """---
name: {name}
role: {role}
summary: a demo persona generated in offline mode
---

# {name}

## Background
This persona was produced by the offline stub, not by a model. Run without
`--offline` to get a real character written by Claude.

## Personality
- Placeholder
- Placeholder

## How they speak
- In whatever the scripted stub happens to return
"""


@dataclass
class DemoLLM:
    """
    Offline stub used by --offline.

    A single ScriptedLLM cannot serve both jobs because persona creation
    expects Markdown while conversations expect dialogue.

    DemoLLM therefore looks at the system prompt and returns content in
    the shape expected by the caller.

    It does not make network requests and does not require an API key.
    """

    calls: List[Dict[str, Any]] = field(
        default_factory=list
    )

    def complete(
        self,
        system: str,
        messages: List[Dict[str, Any]],
        max_tokens: int = 2048,
    ) -> str:
        """
        Return an offline persona, stage-manager response, or dialogue line.
        """

        self.calls.append(
            {
                "system": system,
                "messages": list(messages),
                "max_tokens": max_tokens,
            }
        )

        request = messages[-1]["content"] if messages else ""

        # -------------------------------------------------------------
        # Persona generation
        # -------------------------------------------------------------
        # The persona-author prompt is the only one that asks for this
        # particular frontmatter structure.
        # -------------------------------------------------------------

        if "role: <one lowercase word" in system:
            description = request.replace(
                "Write a persona for:",
                "",
            ).strip()

            words = [
                word
                for word in description.split()
                if word.isalpha()
            ]

            role = (
                words[0].lower()
                if words
                else "person"
            )

            name = (
                description[:40].title()
                or "Demo Persona"
            )

            return _DEMO_PERSONA.format(
                name=name,
                role=role,
            )

        # -------------------------------------------------------------
        # Stage manager
        # -------------------------------------------------------------

        if "stage manager" in system.lower():
            return (
                "Offline mode — I'm a stub. "
                "Try: create a persona doctor"
            )

        # -------------------------------------------------------------
        # Persona dialogue
        # -------------------------------------------------------------

        return _DEMO_DIALOGUE[
            (len(self.calls) - 1) % len(_DEMO_DIALOGUE)
        ]

    def complete_with_tools(
        self,
        system: str,
        messages: List[Dict[str, Any]],
        tools: List[Dict[str, Any]],
        max_tokens: int = 2048,
    ) -> Any:
        """
        Record a tool-enabled request in offline mode.

        DemoLLM does not imitate Anthropic's structured tool-use API.

        The orchestrator should continue using its offline/test routing
        behavior when DemoLLM is active.
        """

        self.calls.append(
            {
                "system": system,
                "messages": list(messages),
                "tools": tools,
                "max_tokens": max_tokens,
            }
        )

        return None


def default_llm(
    offline: bool = False,
    model: Optional[str] = None,
) -> LLM:
    """
    Select the appropriate LLM implementation.

    offline=True:
        Return DemoLLM. No network or API key is required.

    offline=False:
        Return ClaudeLLM using the requested model or DEFAULT_MODEL.
    """

    if offline:
        return DemoLLM()

    return ClaudeLLM(
        model=model or DEFAULT_MODEL
    )