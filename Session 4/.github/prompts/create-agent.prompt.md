---
mode: ask
tools: ['codebase', 'editFiles', 'runCommands']
description: Generate a complete Python agent from a beginner prompt
---

Use the workspace skill in `create-agent.md`.

Task:

- Convert the user request into one runnable Python file with full implementation.
- Name the file from the requested domain in snake_case as `<use_case>_agent.py`.
- If the domain is unclear, generate `generic_agent.py`.
- Include beginner-friendly structure, simple comments, and a main demo block.
- Do not leave core logic as placeholders.

User request:

{{input}}
