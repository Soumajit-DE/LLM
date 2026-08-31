# Copilot Workspace Instructions

When the user asks for agent creation using phrases like:

- "create agent for me"
- "build an agent"
- "<domain> agent"

follow the skill defined in [create-agent.md](../create-agent.md).

Expected behavior:

1. Generate a complete Python implementation file in the workspace.
2. Name the file using the requested domain in snake_case, as `<use_case>_agent.py`.
3. Include all core logic in a single file for beginner readability.
4. Ensure the generated file is runnable immediately.

Also reference [skills.md](../skills.md) as the skill index.
