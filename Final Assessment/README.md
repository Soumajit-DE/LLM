# Event-Planning Multi-Agent System - Final Assessment

Five notebooks build up one event-planning multi-agent system, each adding a layer on top of the
last:

| Notebook | Adds |
|---|---|
| [Task.ipynb](Task.ipynb) | Four single-purpose agents (`VenueAgent`, `CateringLogisticsAgent`, `AVVendorCoordinationAgent`, `AgendaAssemblyAgent`) with Pydantic input/output schemas (exported to [schemas/](schemas/)) and isolated unit tests |
| [Task2.ipynb](Task2.ipynb) | A `MemoryStore` for bounded multi-turn/multi-session conversational context |
| [Task3.ipynb](Task3.ipynb) | An `EventPlanningOrchestrator` that routes the four agents through a DAG with conditional routing and a parallel branch, plus a trace logger |
| [Task4.ipynb](Task4.ipynb) | An `Evaluator` (LLM-as-judge) that scores every agent output against a 4-criterion rubric, with retry/escalation logic |
| [Task5.ipynb](Task5.ipynb) | Guardrails: an input classifier, rule-based output hallucination checks, and a cost-cap guard, wired into a `GuardedEventPipeline` |

Supporting submission artifacts:
- [agent_flow_diagram.md](agent_flow_diagram.md) - the full agent/guardrail flow (ASCII + Mermaid).
- [evaluation_report.md](evaluation_report.md) - the five-test-case evaluation report from `Task4.ipynb`.
- [trace_log_sample_request.md](trace_log_sample_request.md) - an end-to-end trace log for one complete sample event request from `Task3.ipynb`.

## Setup instructions

1. **Prerequisites**: Python 3.11+ and the Jupyter extension for VS Code (or any Jupyter
   front-end).
2. **Create and activate a virtual environment**, then install dependencies from the repo root:
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r ..\requirements.txt
   ```
3. **Run the notebooks offline (default, no credentials needed)**: every notebook injects a
   scripted/fake `LLMClient` (`FakeLLMClient`, `ScriptedLLMClient`, or `KeyedFakeLLMClient`) into
   each agent, so all cells run deterministically with no network access or API keys. Just open
   a notebook in VS Code, select a Python 3.11+ kernel, and "Run All".
4. **Run against the real Azure OpenAI backend (optional)**: set the `DOPPLER_AIGUILD_TOKEN`
   environment variable (consumed by the repo-root `init_creds.py` via the Doppler SDK), then in
   the notebook construct each agent/guard with `AzureOpenAIClient()` instead of the scripted fake
   client - every class implements the same `LLMClient.generate(...)` protocol, so this is a
   drop-in swap with no other code changes.
5. **Recommended run order**: `Task.ipynb` -> `Task2.ipynb` -> `Task3.ipynb` -> `Task4.ipynb` ->
   `Task5.ipynb`. Each notebook is fully self-contained (it redefines the shared agent/schema
   classes it needs) and can also be run independently.

## Design rationale (150 words)

The system decomposes event planning into four single-purpose agents (venue, catering, AV,
agenda), each with its own system prompt and Pydantic-validated input/output schema,
communicating only through structured JSON. A duck-typed `LLMClient` protocol decouples agents
from any specific backend, letting every notebook run deterministically against scripted fake
clients with no network access, while `AzureOpenAIClient` is a drop-in swap for production.
Task2 bounds multi-turn/multi-session context via summarization so returning users aren't asked
to restate known preferences. Task3's orchestrator composes the agents into a DAG with
conditional routing and a parallel branch for latency. Task4 adds an LLM-as-judge `Evaluator`
scoring every output against a 4-criterion rubric, retrying once before escalating to human
review. Task5 wraps the pipeline in guardrails: an input classifier blocking off-topic/harmful
requests, rule-based checks catching hallucinated venues and impossible timelines, and a
cost-cap guard that aborts before overspending - a layered, testable, defense-in-depth design.
