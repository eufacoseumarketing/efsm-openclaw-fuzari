---
name: operations-scheduling
description: Design reusable scheduled or recurring operational tasks for agency workflows. Use when turning a repeated workflow into a self-contained scheduled task, reminder, recurring check, or automation prompt that can run later without relying on the current conversation.
---

# Operations Scheduling

Use this skill when a workflow should be repeatable on demand or on a schedule.

## Use cases
- recurring inbox checks
- routine reporting prompts
- follow-up reminders
- recurring operational reviews
- automated monitoring tasks

## Workflow
1. Identify the repeatable objective.
2. Rewrite it as a self-contained prompt with no dependence on the current chat.
3. Include required file paths, tools, outputs, and success criteria.
4. Decide whether the task is ad hoc, one-time, or recurring.
5. Use local time for schedules.

## Guardrails
- Never reference the current conversation as context for future runs.
- Make the prompt executable cold by another session.
- Keep the scheduled objective narrow and testable.
