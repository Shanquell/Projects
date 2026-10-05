from __future__ import annotations

import os
import sys
from pathlib import Path

import gradio as gr


# ============================================================
# Make src/personaforge importable
# ============================================================

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))


# ============================================================
# PersonaForge imports
# ============================================================

from personaforge.llm import ClaudeLLM
from personaforge.orchestrator import Orchestrator


# ============================================================
# Persistent data directory
# ============================================================

PERSONA_DIR = ROOT / "temp"
PERSONA_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================
# Create the LLM
# ============================================================

def create_llm():
    """
    Create the Claude LLM used by PersonaForge.
    """

    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY is not configured. "
            "Add it to the Hugging Face Space secrets."
        )

    return ClaudeLLM()


# ============================================================
# Create PersonaForge
# ============================================================

llm = create_llm()

orchestrator = Orchestrator(
    llm=llm,
    persona_dir=PERSONA_DIR,
)


# ============================================================
# Gradio response function
# ============================================================

def respond(message, history):
    """
    Send a natural-language command to PersonaForge.
    """

    if not message or not message.strip():
        return "Please enter a command or message."

    generated_turns = []

    def on_start(topic):
        generated_turns.append(
            f"**Conversation: {topic}**"
        )

    def on_turn(turn):
        generated_turns.append(
            f"**{turn.speaker}:** {turn.text}"
        )

    try:
        result = orchestrator.handle(
            message,
            on_turn=on_turn,
            on_start=on_start,
        )

        output = []

        # Display generated conversation turns.
        if generated_turns:
            output.extend(generated_turns)

        # Display the orchestrator's final response.
        if result.reply:
            output.append(result.reply)

        # Display useful events such as saved files.
        if result.events:
            output.append(
                "\n".join(
                    f"*{event}*"
                    for event in result.events
                )
            )

        if not output:
            return "Done."

        return "\n\n".join(output)

    except Exception as exc:
        return f"Error: {exc}"


# ============================================================
# Gradio interface
# ============================================================

demo = gr.ChatInterface(
    fn=respond,
    title="PersonaForge",
    description=(
        "Create fictional personas and generate "
        "multi-agent conversations using PersonaForge."
    ),
    examples=[
        "Create a persona doctor named Edward Chen",
        "Create a persona patient named David Chen",
        "List personas",
        (
            "Have Edward Chen and David Chen talk "
            "about MRI results"
        ),
    ],
)


# ============================================================
# Launch
# ============================================================

if __name__ == "__main__":
    demo.launch()