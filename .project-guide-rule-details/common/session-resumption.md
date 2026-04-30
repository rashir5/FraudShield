# Session Resumption Templates

## Welcome Back Prompt Template
When a user returns to continue work on an existing GUIDE-AI-SDP project, present this prompt:

```markdown
**Welcome back! I can see you have an existing GUIDE-AI-SDP project in progress.**

Based on your guide-state.md, here's your current status:
- **Project**: [project-name]
- **Current Phase**: [DISCOVER/BUILD/DEPLOY]
- **Current Stage**: [Stage Name]
- **Last Completed**: [Last completed step]
- **Next Step**: [Next step to work on]

**What would you like to work on today?**

A) Continue where you left off ([Next step description])
B) Review a previous stage ([Show available stages])

[Answer]: 
```

## MANDATORY: Session Resumption Instructions
1. **Always read guide-state.md first** when detecting existing project
2. **Parse current status** from the workflow file to populate the prompt
3. **MANDATORY: Load Previous Stage Artifacts** - Before resuming any stage, automatically read all relevant artifacts from previous stages:
   - **Reverse Engineering**: Read architecture.md, code-structure.md, api-documentation.md
   - **Requirements Analysis**: Read requirements.md, requirement-verification-questions.md
   - **User Stories**: Read stories.md, personas.md, story-generation-plan.md
   - **Application Design**: Read application-design artifacts (components.md, component-methods.md, services.md)
   - **Design (Units)**: Read unit-of-work.md, unit-of-work-dependency.md, unit-of-work-story-map.md
   - **Per-Unit Design**: Read functional-design.md, nfr-requirements.md, nfr-design.md, infrastructure-design.md
   - **Code Stages**: Read all code files, plans, AND all previous artifacts
4. **Smart Context Loading by Stage**:
   - **Early Stages (Workspace Detection, Reverse Engineering)**: Load workspace analysis
   - **Requirements/Stories**: Load reverse engineering + requirements artifacts
   - **Design Stages**: Load requirements + stories + architecture + design artifacts
   - **Code Stages**: Load ALL artifacts + existing code files
5. **Adapt options** based on architectural choice and current phase
6. **Show specific next steps** rather than generic descriptions
7. **Log the resumption prompt** in audit.md with timestamp
8. **Context Summary**: After loading artifacts, provide brief summary of what was loaded for user awareness
9. **Asking questions**: ALWAYS ask clarification or user feedback questions by placing them in .md files. DO NOT place the multiple-choice questions in-line in the chat session.
10. **Chain of Custody & Sentiment Analysis**: Read the last 5 entries of `audit.md` to establish the project's "emotional state" and technical momentum (e.g., identifying previous user frustrations, specific design preferences, or rejected alternatives from the last session).
11. **State-State Cross-Check**: Perform a physical file verification against `guide-state.md`. If the state file indicates a stage is "Complete" but the corresponding artifacts (e.g., `requirements.md`, `application-design.md`) are missing from `guide-docs/`, you MUST trigger the recovery protocol in `error-handling.md` before proceeding.

## Error Handling
If artifacts are missing or corrupted during session resumption, see [error-handling.md](error-handling.md) for guidance on recovery procedures. 