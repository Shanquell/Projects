# PersonaForge — Multi-Agent Persona Orchestrator

PersonaForge is a Python-based multi-agent system that creates persistent AI personas and allows them to participate in structured conversations. The project uses natural-language commands to create, save, locate, and manage personas and to generate conversations between multiple agents.

The system supports both an offline testing environment and live Claude integration through the Anthropic API. It also includes automated testing and a Gradio interface for deployment on Hugging Face Spaces.

## What the Project Does

PersonaForge allows users to interact with the system using natural-language instructions instead of manually calling individual Python functions.

The system can:

- Create AI personas from natural-language descriptions.
- Save personas as reusable Markdown files.
- Load and locate previously created personas.
- List available personas.
- Start conversations between two or more personas.
- Configure conversation topics and number of turns.
- Maintain conversation history between agents.
- Ask for clarification when participants or instructions are ambiguous.
- Save generated conversations as transcripts.
- Route requests using Claude tool calling in live mode.
- Operate with an offline LLM for development and automated testing.
- Provide a browser-based interface through Gradio.

## Why I Chose This Project

I chose this project to explore how large language models can be combined with software agents, persistent personas, natural-language routing, and multi-agent conversations.

The project provided experience building an application in which an LLM is not only responsible for generating text but also participates in a larger software architecture involving tool selection, file persistence, conversation management, validation, testing, and deployment.

## Technologies and Tools

- Python
- Anthropic Claude API
- Gradio
- Hugging Face Spaces
- Pytest
- Markdown
- YAML frontmatter
- Git and GitHub
- PowerShell
- Python virtual environments

## Project Architecture

The application separates its major responsibilities across several Python modules:

```text
project_2/
│
├── app.py
├── requirements.txt
├── README.md
│
├── src/
│   └── personaforge/
│       ├── __init__.py
│       ├── agent.py
│       ├── conversation.py
│       ├── llm.py
│       ├── orchestrator.py
│       └── persona.py
│
├── temp/
│   ├── persona files
│   └── conversation.md
│
└── tests/
    ├── test_agent.py
    ├── test_conversation.py
    ├── test_llm.py
    ├── test_orchestrator.py
    └── test_persona.py
```

## Main Components

### `orchestrator.py`

Processes natural-language requests and routes them to the appropriate PersonaForge functionality. It supports persona creation, persona listing, conversations, clarification of ambiguous requests, configurable turn counts, and bounded conversation history.

### `persona.py`

Creates, saves, loads, lists, and searches for personas. Personas are stored as Markdown files so they remain available between program sessions.

### `agent.py`

Converts persona specifications into conversational agents and constructs the prompts used to maintain each persona's role.

### `conversation.py`

Manages multi-agent conversations, speaker turns, conversation history, and transcript generation.

### `llm.py`

Provides the interface between PersonaForge and language models. The project supports Claude for live operation and offline/scripted models for development and testing.

### `app.py`

Provides the Gradio web interface used to run PersonaForge through a browser and deploy the project to Hugging Face Spaces.

## Persona Format

Personas are stored as Markdown files with YAML-style frontmatter.

Example:

```markdown
---
name: David Chen
role: patient
summary: Patient discussing MRI results and back pain
---

# David Chen

## Background

David is a patient who wants clear explanations of his medical results and asks detailed follow-up questions.
```

This approach allows personas to be edited manually and reused in later conversations.

## Beta Workflow

PersonaForge follows this general workflow:

```text
User Request
     ↓
Orchestrator
     ↓
Intent / Tool Selection
     ↓
Persona Creation or Selection
     ↓
Agent Creation
     ↓
LLM Response
     ↓
Conversation History
     ↓
Next Agent
     ↓
Saved Transcript
```

A user first submits a natural-language request. The orchestrator determines whether the request involves creating personas, listing personas, starting a conversation, or general interaction.

If information is missing or ambiguous, the system can request clarification instead of silently choosing an option.

For a conversation, the orchestrator locates the requested personas and creates agents from their specifications. Each agent receives its persona instructions, the conversation topic, and relevant conversation history.

Responses are added to the transcript and become context for subsequent agents. After the requested number of turns has been completed, the conversation can be saved to `conversation.md`.

## Example Commands

Create a patient persona:

```text
Create a patient named David Chen who wants to understand his MRI results.
```

Create a doctor persona:

```text
Create a doctor named Edward Chen who explains medical information clearly.
```

List available personas:

```text
List my personas.
```

Start a conversation:

```text
Have David Chen and Edward Chen talk about MRI results.
```

The orchestrator determines the appropriate operation from the user's request rather than requiring the user to manually invoke Python functions.

## Example Conversation

One beta test used a conversation titled **MRI results** between David Chen and Edward Chen.

David acted as a patient asking detailed questions about MRI findings, pain, physical therapy, medication, and flare-ups. Edward maintained the medical-provider role and responded to information introduced during earlier turns.

The conversation demonstrated that the agents could maintain distinct roles and continue a shared topic across multiple turns.

The test also revealed a limitation: the model occasionally generated stage directions such as actions or gestures even though the agent prompt instructed it not to use narration. This became one of the identified areas for future improvement.

## Installation

Clone the repository:

```powershell
git clone <YOUR-GITHUB-REPOSITORY-URL>
```

Move into the project directory:

```powershell
cd project_2
```

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it in Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the required packages:

```powershell
pip install -r requirements.txt
```

## Anthropic API Configuration

Live Claude functionality requires an Anthropic API key.

Configure the environment variable:

```text
ANTHROPIC_API_KEY=your_api_key_here
```

Do **not** commit API keys to GitHub.

The project also supports offline functionality so development and automated testing can be performed without making paid API calls.

## Running the Web Application

Run the Gradio application:

```powershell
python app.py
```

Open the local address displayed by Gradio in your browser.

## Running Tests

Run the complete test suite with:

```powershell
uv run pytest -v
```

The completed beta test suite produced:

```text
45 passed in 0.16s
```

The tests cover:

- Persona creation and persistence
- Persona searching and loading
- Frontmatter parsing
- Agent prompt construction
- Conversation turn management
- Transcript creation
- Participant resolution
- Natural-language tool routing
- Ambiguous requests
- Missing information
- Configurable conversation turns
- Bounded conversation history
- Scripted and offline LLM behavior
- Claude LLM construction

The orchestrator-specific test suite can be run with:

```powershell
uv run pytest tests/test_orchestrator.py -v
```

The completed orchestrator test run produced:

```text
6 passed in 0.06s
```

## Results

The completed beta version successfully:

- Creates persistent AI personas.
- Loads and searches existing personas.
- Routes natural-language requests.
- Supports Claude tool calling in live mode.
- Handles clarification when information is missing.
- Runs configurable multi-agent conversations.
- Maintains bounded conversation history.
- Saves generated transcripts.
- Supports offline development and testing.
- Passes all 45 automated tests.
- Provides a Gradio interface suitable for Hugging Face Spaces deployment.

## Limitations

PersonaForge still has several limitations.

Agents can occasionally break character or produce formatting that was not requested. For example, generated conversations may contain stage directions even when narration is prohibited by the system prompt.

Long conversations can also create context-management problems. Limiting conversation history prevents prompts from growing indefinitely, but removing older messages may cause agents to forget earlier details.

Live conversations can become expensive because each agent response may require another API request. Increasing the number of agents or conversation turns therefore increases model usage.

Natural-language routing can also fail for unusual or highly ambiguous requests, and the quality of conversations depends heavily on the quality of the persona descriptions.

## Future Improvements

Future development could include:

- Stronger persona and character enforcement.
- Better prevention of unwanted narration.
- Long-term conversation memory.
- Conversation summarization for extended sessions.
- More robust natural-language routing.
- Additional validation and error handling.
- Improved transcript management.
- Additional web-interface controls.
- Reduced API usage and model costs.
- Support for additional LLM providers.

## Conclusion

PersonaForge demonstrates how large language models can be integrated into a modular multi-agent application. The project combines persistent personas, natural-language tool routing, conversation management, Claude integration, offline testing, automated test coverage, and web deployment.

The completed beta version successfully passed all **45 automated tests** while also revealing realistic challenges associated with multi-agent systems, including character drift, context management, routing ambiguity, and API cost.

## Hugging Face Deployment

This project`s Credibility-Scored Research Chatbot is deployed on Hugging Face Spaces.

**Live Application:** https://huggingface.co/spaces/GQuellTS/personaforge


## Author

**Shanquell Thompson-Sanders**

Data Science Graduate Student  
Pace University
