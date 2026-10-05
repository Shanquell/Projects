"""
orchestrator.py — the agent you talk to.

The orchestrator decides what the user wants to do and connects natural
language requests to PersonaForge's Python functions.

Live Claude mode uses real Anthropic tool calling.

Offline/test models that do not provide structured tool responses continue
to use a small deterministic fallback router so the package can still be
tested without an API key.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from .agent import agent_from_spec
from .conversation import (
    Conversation,
    Turn,
    run_conversation,
    save_transcript,
)
from .llm import ClaudeLLM, LLM
from .persona import (
    DEFAULT_PERSONA_DIR,
    PersonaSpec,
    find_persona,
    generate_persona,
    list_personas,
    save_persona,
)


# =============================================================================
# Stage-manager prompt
# =============================================================================

_STAGE_MANAGER_SYSTEM = """
You are the stage manager of a persona simulation workshop.

The user can create fictional personas, list existing personas, and start
conversations between personas.

Use the available tools whenever the user clearly requests an action.

If required information is missing or ambiguous, do not guess. Ask the user
a brief clarifying question.

Examples:

User: "Create a doctor."
Action: use create_persona.

User: "Create a persona."
Action: ask the user what kind of persona they want.

User: "List my characters."
Action: use list_personas.

User: "Have Maria and James discuss the MRI."
Action: use start_conversation.

User: "Have them talk."
Action: if it is unclear who "them" refers to or what they should discuss,
ask a clarifying question.

Be concise and helpful.
"""

TOOLS = [
    {
        "name": "create_persona",
        "description": "Create and save a new fictional persona.",
        "input_schema": {
            "type": "object",
            "properties": {
                "description": {
                    "type": "string",
                    "description": (
                        "A detailed description of the persona to create, "
                        "including role, personality, name, or background "
                        "when provided by the user."
                    ),
                }
            },
            "required": ["description"],
        },
    },
    {
        "name": "list_personas",
        "description": "List all personas that currently exist.",
        "input_schema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "start_conversation",
        "description": "Start a conversation between existing personas.",
        "input_schema": {
            "type": "object",
            "properties": {
                "participants": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": (
                        "Names of personas who should participate. "
                        "Use an empty list if the user did not specify them."
                    ),
                },
                "topic": {
                    "type": "string",
                    "description": "The topic the personas should discuss.",
                },
                "turns": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 30,
                    "description": "Number of conversation turns.",
                },
            },
            "required": ["participants", "topic", "turns"],
        },
    },
]

# =============================================================================
# Result
# =============================================================================

@dataclass
class Result:
    """What the orchestrator did, in a form the UI can render."""

    reply: str
    events: List[str] = field(default_factory=list)
    conversation: Optional[Conversation] = None


# =============================================================================
# Orchestrator
# =============================================================================

class Orchestrator:
    """
    Routes what the user typed to the correct part of PersonaForge.

    Live Claude mode:
        Uses real Anthropic tool calling.

    Offline/test mode:
        Uses the deterministic fallback router.
    """

    MAX_HISTORY_MESSAGES = 20

    def __init__(
        self,
        llm: LLM,
        persona_dir: Path = DEFAULT_PERSONA_DIR,
    ) -> None:

        self.llm = llm
        self.persona_dir = Path(persona_dir)
        self.history: List[Dict[str, Any]] = []

    # =========================================================================
    # History
    # =========================================================================

    def _trim_history(self) -> None:
        """
        Keep the orchestrator history from growing forever.
        """

        if len(self.history) > self.MAX_HISTORY_MESSAGES:
            self.history = self.history[-self.MAX_HISTORY_MESSAGES:]

    # =========================================================================
    # Persona creation
    # =========================================================================

    def _create_persona(
        self,
        description: str,
    ) -> Result:
        """
        Author a persona, write it to disk, and report where it landed.
        """

        description = description.strip()

        if not description:
            return Result(
                reply=(
                    "What kind of persona would you like me to create?"
                )
            )

        spec = generate_persona(
            description,
            self.llm,
        )

        path = save_persona(
            spec,
            self.persona_dir,
        )

        return Result(
            reply=(
                f"Created **{spec.name}** ({spec.role}) — "
                f"{spec.summary}"
            ),
            events=[
                f"wrote {path}"
            ],
        )

    # =========================================================================
    # List personas
    # =========================================================================

    def _list_personas(self) -> Result:
        """
        Show the personas currently stored in the persona directory.
        """

        specs = list_personas(
            self.persona_dir
        )

        if not specs:
            return Result(
                reply=(
                    "No personas yet. "
                    "Try: create a persona doctor"
                )
            )

        lines = [
            f"- **{spec.name}** ({spec.role}) — {spec.summary}"
            for spec in specs
        ]

        return Result(
            reply=(
                f"{len(specs)} persona(s) in "
                f"`{self.persona_dir}`:\n"
                + "\n".join(lines)
            )
        )

    # =========================================================================
    # Conversation
    # =========================================================================

    def _converse(
        self,
        topic: str,
        who: Optional[List[str]] = None,
        turns: int = 6,
        on_turn: Optional[Callable[[Turn], None]] = None,
        on_start: Optional[Callable[[str], None]] = None,
    ) -> Result:
        """
        Wake up two or more personas and let them talk.
        """

        specs: List[PersonaSpec] = []

        topic = topic.strip()

        if not topic:
            return Result(
                reply="What should the personas discuss?"
            )

        # ---------------------------------------------------------------------
        # User/model supplied participant names
        # ---------------------------------------------------------------------

        if who:

            for name in who:

                found = find_persona(
                    name,
                    self.persona_dir,
                )

                if found is None:
                    return Result(
                        reply=(
                            "I couldn't find a persona matching "
                            f"'{name}'."
                        )
                    )

                specs.append(found)

        # ---------------------------------------------------------------------
        # No participant names supplied
        # ---------------------------------------------------------------------

        else:

            available = list_personas(
                self.persona_dir
            )

            if len(available) < 2:
                return Result(
                    reply=(
                        "I need at least two personas before they can talk. "
                        "Create another one first."
                    )
                )

            if len(available) > 2:

                names = ", ".join(
                    spec.name
                    for spec in available
                )

                return Result(
                    reply=(
                        "You have more than two personas. "
                        "Who should participate? "
                        f"Available personas: {names}"
                    )
                )

            specs = available

        # ---------------------------------------------------------------------
        # Safety check
        # ---------------------------------------------------------------------

        if len(specs) < 2:
            return Result(
                reply=(
                    "I need at least two personas before they can talk."
                )
            )

        # ---------------------------------------------------------------------
        # Validate turns
        # ---------------------------------------------------------------------

        try:
            turns = int(turns)
        except (TypeError, ValueError):
            turns = 6

        turns = max(
            1,
            min(turns, 30),
        )

        # ---------------------------------------------------------------------
        # Build agents
        # ---------------------------------------------------------------------

        agents = [
            agent_from_spec(
                spec,
                self.llm,
            )
            for spec in specs
        ]

        # ---------------------------------------------------------------------
        # Notify UI that the conversation is beginning
        # ---------------------------------------------------------------------

        if on_start is not None:
            on_start(topic)

        # ---------------------------------------------------------------------
        # Run actual persona conversation
        # ---------------------------------------------------------------------

        conversation = run_conversation(
            agents,
            topic=topic,
            turns=turns,
            on_turn=on_turn,
        )

        # ---------------------------------------------------------------------
        # Save actual transcript
        # ---------------------------------------------------------------------

        path = save_transcript(
            conversation,
            self.persona_dir,
            filename="conversation.md",
        )

        return Result(
            reply=(
                f"{len(conversation.turns)} turns between "
                f"{' and '.join(spec.name for spec in specs)}."
            ),
            events=[
                f"wrote {path}"
            ],
            conversation=conversation,
        )

    # =========================================================================
    # Ordinary stage-manager chat
    # =========================================================================

    def _chat(
        self,
        text: str,
    ) -> Result:
        """
        Send an ordinary non-tool request to the stage manager.
        """

        self.history.append(
            {
                "role": "user",
                "content": text,
            }
        )

        self._trim_history()

        reply = self.llm.complete(
            _STAGE_MANAGER_SYSTEM,
            self.history,
            max_tokens=512,
        )

        self.history.append(
            {
                "role": "assistant",
                "content": reply,
            }
        )

        self._trim_history()

        return Result(
            reply=reply
        )

    # =========================================================================
    # Tool execution
    # =========================================================================

    def _execute_tool(
        self,
        name: str,
        arguments: Dict[str, Any],
        on_turn: Optional[Callable[[Turn], None]] = None,
        on_start: Optional[Callable[[str], None]] = None,
    ) -> Result:
        """
        Execute a tool selected by Claude.

        Claude chooses the tool and supplies the arguments.
        Python remains responsible for performing the actual operation.
        """

        # ---------------------------------------------------------------------
        # Create persona
        # ---------------------------------------------------------------------

        if name == "create_persona":

            description = str(
                arguments.get(
                    "description",
                    "",
                )
            ).strip()

            if not description:
                return Result(
                    reply=(
                        "What kind of persona would you like me to create?"
                    )
                )

            return self._create_persona(
                description
            )

        # ---------------------------------------------------------------------
        # List personas
        # ---------------------------------------------------------------------

        if name == "list_personas":

            return self._list_personas()

        # ---------------------------------------------------------------------
        # Start conversation
        # ---------------------------------------------------------------------

        if name == "start_conversation":

            participants = arguments.get(
                "participants",
                [],
            )

            if not isinstance(
                participants,
                list,
            ):
                participants = []

            participants = [
                str(name).strip()
                for name in participants
                if str(name).strip()
            ]

            topic = str(
                arguments.get(
                    "topic",
                    "",
                )
            ).strip()

            if not topic:
                return Result(
                    reply=(
                        "What should the personas discuss?"
                    )
                )

            turns = arguments.get(
                "turns",
                6,
            )

            try:
                turns = int(turns)
            except (TypeError, ValueError):
                turns = 6

            turns = max(
                1,
                min(turns, 30),
            )

            return self._converse(
                topic=topic,
                who=participants or None,
                turns=turns,
                on_turn=on_turn,
                on_start=on_start,
            )

        # ---------------------------------------------------------------------
        # Unknown tool
        # ---------------------------------------------------------------------

        return Result(
            reply=f"Unknown tool: {name}"
        )

    # =========================================================================
    # Real Claude tool routing
    # =========================================================================

    def _handle_with_tools(
        self,
        text: str,
        on_turn: Optional[Callable[[Turn], None]] = None,
        on_start: Optional[Callable[[str], None]] = None,
    ) -> Result:
        """
        Handle a user request using real Claude tool calling.

        Flow:

            user
              ↓
            Claude
              ↓
            tool_use
              ↓
            Python executes tool
              ↓
            tool_result
              ↓
            Claude
              ↓
            final response

        The loop continues as long as Claude requests tools.
        """

        # ---------------------------------------------------------------------
        # Add user message
        # ---------------------------------------------------------------------

        self.history.append(
            {
                "role": "user",
                "content": text,
            }
        )

        self._trim_history()

        # ---------------------------------------------------------------------
        # First Claude request
        # ---------------------------------------------------------------------

        response = self.llm.complete_with_tools(
            system=_STAGE_MANAGER_SYSTEM,
            messages=self.history,
            tools=TOOLS,
            max_tokens=1024,
        )

        final_events: List[str] = []
        final_conversation: Optional[Conversation] = None
        tool_summaries: List[str] = []

        # Protect against an accidental infinite tool loop.
        tool_rounds = 0
        max_tool_rounds = 10

        # ---------------------------------------------------------------------
        # Tool loop
        # ---------------------------------------------------------------------

        while response.stop_reason == "tool_use":

            tool_rounds += 1

            if tool_rounds > max_tool_rounds:
                return Result(
                    reply=(
                        "The tool loop exceeded the allowed number "
                        "of steps."
                    ),
                    events=final_events,
                    conversation=final_conversation,
                )

            # Claude's assistant message must be preserved exactly,
            # including its tool_use blocks.
            self.history.append(
                {
                    "role": "assistant",
                    "content": response.content,
                }
            )

            tool_results = []

            # -----------------------------------------------------------------
            # Execute every tool requested in this response
            # -----------------------------------------------------------------

            for block in response.content:

                if getattr(
                    block,
                    "type",
                    None,
                ) != "tool_use":
                    continue

                result = self._execute_tool(
                    name=block.name,
                    arguments=block.input,
                    on_turn=on_turn,
                    on_start=on_start,
                )

                # Preserve events such as:
                #
                # wrote temp/josh.md
                # wrote temp/conversation.md
                #
                final_events.extend(
                    result.events
                )

                if result.conversation is not None:
                    final_conversation = result.conversation

                if result.reply:
                    tool_summaries.append(
                        result.reply
                    )

                # Return the real result to Claude.
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": (
                            result.reply
                            or "Tool completed successfully."
                        ),
                    }
                )

            # -----------------------------------------------------------------
            # Send tool results back as a user/tool-result message
            # -----------------------------------------------------------------

            self.history.append(
                {
                    "role": "user",
                    "content": tool_results,
                }
            )

            self._trim_history()

            # -----------------------------------------------------------------
            # Give Claude the results and allow another tool call
            # -----------------------------------------------------------------

            response = self.llm.complete_with_tools(
                system=_STAGE_MANAGER_SYSTEM,
                messages=self.history,
                tools=TOOLS,
                max_tokens=1024,
            )

        # ---------------------------------------------------------------------
        # Extract final normal text from Claude
        # ---------------------------------------------------------------------

        text_parts: List[str] = []

        for block in response.content:

            if getattr(
                block,
                "type",
                None,
            ) == "text":

                if block.text.strip():
                    text_parts.append(
                        block.text.strip()
                    )

        reply = "\n".join(
            text_parts
        ).strip()

        # ---------------------------------------------------------------------
        # Save Claude's final assistant response in history
        # ---------------------------------------------------------------------

        self.history.append(
            {
                "role": "assistant",
                "content": response.content,
            }
        )

        self._trim_history()

        # ---------------------------------------------------------------------
        # If Claude produced no final text, use the actual tool result.
        # ---------------------------------------------------------------------

        if not reply:

            if final_conversation is not None:

                reply = (
                    f"Conversation complete: "
                    f"{len(final_conversation.turns)} turns."
                )

            elif tool_summaries:

                reply = tool_summaries[-1]

            else:

                reply = "Done."

        return Result(
            reply=reply,
            events=final_events,
            conversation=final_conversation,
        )

    # =========================================================================
    # Offline/test fallback router
    # =========================================================================

    def _handle_fallback(
        self,
        text: str,
        on_turn: Optional[Callable[[Turn], None]] = None,
        on_start: Optional[Callable[[str], None]] = None,
    ) -> Result:
        """
        Deterministic fallback router.

        This keeps ScriptedLLM and DemoLLM usable without requiring them to
        reproduce Anthropic's structured tool-use response objects.

        Live Claude does NOT use this router.
        """

        lower = text.lower()

        # ---------------------------------------------------------------------
        # List personas
        # ---------------------------------------------------------------------

        if (
            "list personas" in lower
            or "list the personas" in lower
            or "show personas" in lower
            or "show me the personas" in lower
            or "list my characters" in lower
        ):
            return self._list_personas()

        # ---------------------------------------------------------------------
        # Create persona
        # ---------------------------------------------------------------------

        create_match = re.search(
            r"(?:create|make|build|add|generate)"
            r"\s+(?:me\s+)?(?:a\s+)?persona"
            r"(?:\s+(?:for|of))?\s*(.*)",
            text,
            re.IGNORECASE,
        )

        if create_match:

            description = create_match.group(
                1
            ).strip()

            if not description:
                return Result(
                    reply=(
                        "What kind of persona would you like me to create?"
                    )
                )

            return self._create_persona(
                description
            )

        # ---------------------------------------------------------------------
        # Explicit:
        #
        # start a conversation between Carol and Bob about the chart
        # ---------------------------------------------------------------------

        conversation_match = re.search(
            r"(?:start|have|begin)\s+"
            r"(?:a\s+)?conversation\s+between\s+"
            r"(.+?)\s+and\s+(.+?)\s+about\s+(.+)",
            text,
            re.IGNORECASE,
        )

        if conversation_match:

            first = conversation_match.group(
                1
            ).strip()

            second = conversation_match.group(
                2
            ).strip()

            topic = conversation_match.group(
                3
            ).strip()

            return self._converse(
                topic=topic,
                who=[
                    first,
                    second,
                ],
                on_turn=on_turn,
                on_start=on_start,
            )

        # ---------------------------------------------------------------------
        # More natural:
        #
        # have Josh and Pat talk about the MRI results
        # ---------------------------------------------------------------------

        named_talk_match = re.search(
            r"(?:have|let)\s+"
            r"(.+?)\s+and\s+(.+?)\s+"
            r"(?:talk|discuss|speak)"
            r"(?:\s+about)?\s+(.+)",
            text,
            re.IGNORECASE,
        )

        if named_talk_match:

            first = named_talk_match.group(
                1
            ).strip()

            second = named_talk_match.group(
                2
            ).strip()

            topic = named_talk_match.group(
                3
            ).strip()

            return self._converse(
                topic=topic,
                who=[
                    first,
                    second,
                ],
                on_turn=on_turn,
                on_start=on_start,
            )

        # ---------------------------------------------------------------------
        # General:
        #
        # have them talk about the weather
        # ---------------------------------------------------------------------

        talk_match = re.search(
            r"(?:have\s+them\s+talk|"
            r"let\s+them\s+talk|"
            r"have\s+them\s+discuss|"
            r"let\s+them\s+discuss)"
            r"(?:\s+about)?\s+(.+)",
            text,
            re.IGNORECASE,
        )

        if talk_match:

            topic = talk_match.group(
                1
            ).strip()

            return self._converse(
                topic=topic,
                who=None,
                on_turn=on_turn,
                on_start=on_start,
            )

        # ---------------------------------------------------------------------
        # Nothing matched
        # ---------------------------------------------------------------------

        return self._chat(
            text
        )

    # =========================================================================
    # Public entry point
    # =========================================================================

    def handle(
        self,
        text: str,
        on_turn: Optional[Callable[[Turn], None]] = None,
        on_start: Optional[Callable[[str], None]] = None,
    ) -> Result:
        """
        Work out what the user wants.

        ClaudeLLM:
            Use genuine Anthropic tool calling.

        DemoLLM / ScriptedLLM:
            Use the deterministic fallback router.
        """

        text = text.strip()

        if not text:
            return Result(
                reply="What would you like to do?"
            )

        # ---------------------------------------------------------------------
        # LIVE MODE
        # ---------------------------------------------------------------------

        if isinstance(
            self.llm,
            ClaudeLLM,
        ):
            return self._handle_with_tools(
                text=text,
                on_turn=on_turn,
                on_start=on_start,
            )

        # ---------------------------------------------------------------------
        # OFFLINE / TEST MODE
        # ---------------------------------------------------------------------

        return self._handle_fallback(
            text=text,
            on_turn=on_turn,
            on_start=on_start,
        )


# =============================================================================
# PROJECT NOTES
# =============================================================================
#
# The original starter router used regular expressions for all routing.
#
# This beta version uses genuine Claude tool calling in live mode:
#
#     user message
#          ↓
#     Claude receives TOOLS
#          ↓
#     Claude returns tool_use
#          ↓
#     _execute_tool()
#          ↓
#     Python performs the real action
#          ↓
#     tool_result returned to Claude
#          ↓
#     Claude may request another tool
#          ↓
#     final response
#
# The fallback regex router remains only for ScriptedLLM and DemoLLM so the
# project can still be run and tested without an Anthropic API key.
#
# Additional improvements:
#
# 1. Claude can ask clarifying questions instead of guessing.
#
# 2. Multiple tool calls can be executed from a single request.
#
# 3. _converse() no longer silently chooses the first two personas when more
#    than two personas exist.
#
# 4. Conversation turns are configurable from 1 to 30.
#
# 5. Orchestrator history is bounded to avoid unlimited growth.
#
# 6. Real conversations continue to be saved with save_transcript().
#
# =============================================================================