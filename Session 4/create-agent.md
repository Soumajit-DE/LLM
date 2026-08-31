# Skill: create-agent

## Purpose
Convert a beginner-level generic request into a complete, runnable Python agent implementation built with LangGraph.

## Primary Trigger
Use this skill when the user asks for:

- "create agent for me"
- "build an agent"
- "<domain> agent" (any domain)

## Behavior Contract
When this skill is triggered, do all of the following:

1. Infer a concrete use case from the user text.
2. Create one Python file with full implementation using LangGraph for orchestration.
3. Include all required helper classes/functions in the same file.
4. Include clear defaults so the file runs without additional editing.
5. Add a short usage example in a `if __name__ == "__main__":` block.
6. Keep the code beginner-friendly with short comments only where needed.

## Output Requirements
- File name pattern: `<use_case>_agent.py`
- Derive `<use_case>` from the request in snake_case. If unclear, use `generic_agent.py`.
- Must include:
  - Agent class
  - LangGraph graph/state workflow setup
  - State handling (simple dict or dataclass)
  - Tool layer (at least FAQ/tool lookup)
  - Response generation logic
  - Error handling and fallback response
  - Demo input loop or example run

## Domain Specialization Example
If the request is customer support chat, generate `customer_support_agent.py` with:

- Intent detection for common requests (order status, returns, refunds, escalation)
- FAQ/knowledge lookup from in-file dictionary
- LangGraph node/edge flow for routing between intent, tool lookup, and response
- Human handoff trigger for unknown or sensitive requests
- Polite and concise response style
- Basic conversation history handling

## Quality Rules
- Use LangGraph for orchestration (`langgraph` package required).
- You may use minimal supporting packages commonly paired with LangGraph when needed.
- Ensure code is runnable as-is.
- Avoid placeholders like "TODO" for core logic.
- Keep implementation under 250 lines unless user asks for enterprise scale.

## Example Invocation
"Create agent for me for customer support chat"

## Expected Action
Create a complete Python file for the requested domain directly in the workspace.
