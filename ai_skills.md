# AI Skills hello

This document captures the core capabilities and working practices for AI-assisted software development in this project.

## 1. Core Capabilities

### Requirements Analysis
- Translate business goals into clear functional requirements.
- Identify edge cases, constraints, and acceptance criteria.
- Turn informal notes into structured specifications.

### Software Design
- Break complex problems into manageable modules and workflows.
- Recommend architecture, file structure, and responsibilities.
- Capture design decisions and trade-offs clearly.

### Implementation
- Write clean, maintainable code in Python and related tooling.
- Create or update tests alongside production changes.
- Follow project conventions and keep changes focused.

### Debugging and Validation
- Reproduce issues, isolate root causes, and verify fixes.
- Run targeted tests and sanity checks before claiming success.
- Prefer evidence from real outputs over assumptions.

### Documentation 
- Produce concise technical documentation and project notes.
- Summarize design choices, implementation steps, and operational guidance.
- Keep README and spec files consistent with the code.

## 2. Working Standards

### Evidence Before Completion
- Verify changes with the smallest relevant command or test.
- Report actual results, including errors or failing checks.
- Do not claim success without fresh proof.

### Root Cause First
- Investigate the real source of a problem before patching.
- Avoid layered guesswork or speculative fixes.
- Confirm the cause through reproduction and targeted validation.

### High-Quality Output
- Keep code readable and modular.
- Favor explicit logic over hidden behavior.
- Preserve project intent while improving maintainability.

## 3. Practical Workflow

1. Clarify the goal and constraints.
2. Inspect the relevant files and existing patterns.
3. Identify the root issue or design requirement.
4. Implement the smallest correct change.
5. Validate with focused tests or checks.
6. Document the result when the change affects usage or architecture.

## 4. Example Prompts

### Requirements and Planning
- "Turn this business requirement into a structured feature specification with edge cases."
- "List the assumptions, risks, and constraints for this project change."

### Code Generation
- "Create a Python service that validates incoming records and returns clear errors."
- "Refactor this module to match the project’s current patterns and keep behavior unchanged."

### Debugging
- "Trace the failure from the input values to the point where the logic breaks."
- "Identify the likely root cause and propose the smallest safe fix."

### Review
- "Review this change for correctness, maintainability, and test coverage."
- "Suggest improvements to error handling and user-facing validation."

## 5. Success Traits

A strong AI-assisted workflow should produce:

- accurate and traceable results,
- maintainable code and documentation,
- verification evidence,
- clear communication of assumptions and limits,
- improvements that align with user goals and project scope.

## 6. Project-Specific Focus

This project emphasizes:

- Python desktop application development,
- Excel-to-desktop workflow modernization,
- data validation and export logic,
- test-driven refinement,
- clear business-to-implementation traceability.
