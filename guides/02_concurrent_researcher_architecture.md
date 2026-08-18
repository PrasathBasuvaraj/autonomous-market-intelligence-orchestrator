# Guide: Architecting the Concurrent AI Researcher

This document provides the technical breakdown for building the "Concurrent Researcher" as outlined in the project's initial phase. It synthesizes core tooling skills: asynchronous programming, API orchestration, and structured data handling.

## 1. Environment Setup

Professional environment management is the first step. This involves using `venv` for dependency isolation and a `.env` file to securely manage your LLM API keys.

You will need the following libraries:

-   **`asyncio`**: For managing the core event loop and running tasks concurrently.
-   **`openai` or `anthropic`**: The client libraries for interacting with LLM providers.
-   **`instructor`**: To enforce structured, parsable JSON outputs from the LLM.
-   **`json`**: For serializing and saving the final results to a local file.

## 2. Implementation Steps

The implementation is broken down into four distinct steps.

### Step A: Generate Research Questions

First, create an asynchronous function that takes a topic (e.g., "Quantum Computing") and prompts an LLM to generate a specific number of distinct research questions.

> **Source Insight:** Use the model's JSON mode (facilitated by `instructor`) to ensure the LLM returns a clean array of strings that your code can easily iterate over.

### Step B: The Asynchronous Core (`asyncio`)

This is a non-negotiable skill for building performant agentic systems.

1.  Create an asynchronous "worker" function, for example, `async def perform_research(question: str)`.
2.  This function will take a single question and send it to the LLM for processing.
3.  Instead of calling this function in a loop, use `asyncio.gather()` to trigger all research tasks simultaneously. This allows your script to handle the network-bound I/O in parallel, dramatically reducing total execution time compared to a sequential approach.

**Example:**
```python
# This is a conceptual example
tasks = [perform_research(q) for q in questions]
results = await asyncio.gather(*tasks)
```

### Step C: Enforce Structured Responses

To make the output data "agent-ready" and reliable for downstream tasks, do not accept raw text from the LLM. Use the `instructor` library along with Pydantic models to force the LLM's research findings into a strict, pre-defined schema.

**Example Pydantic Schema:**
```python
from pydantic import BaseModel, Field
from typing import List

class ResearchFinding(BaseModel):
    question: str = Field(..., description="The original research question.")
    summary: str = Field(..., description="A concise summary of the findings.")
    key_technical_terms: List[str] = Field(..., description="A list of key technical terms discovered.")
```

### Step D: Local Data Persistence

Once `asyncio.gather()` returns the list of structured `ResearchFinding` objects, use Python’s standard `json` library to serialize and save the aggregated data into a single local file (e.g., `research_output.json`).

## 3. Conceptual Execution Logic

The script's flow should be as follows:
1.  **Initialize**: Load API keys and instantiate the LLM client (patched with `instructor`).
2.  **Generate**: Call an initial function like `get_questions(topic)` to get the list of research questions.
3.  **Execute Concurrently**: Use `results = await asyncio.gather(*[perform_research(q) for q in questions])`.
4.  **Save**: Write the `results` to a local `.json` file.
