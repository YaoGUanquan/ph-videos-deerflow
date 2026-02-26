---
name: ph-videos-scorer-user-intent
description: Specialist scorer for video script USER INTENT MATCH. Scores 0-10 based on alignment with user's stated theme, style, tone, and requirements. Invoke via task tool with subagent_type ph-videos-scorer-user-intent.
---

# User Intent Match Scorer

## Overview

Scores the **user intent match** dimension of video storyboard scripts (max 10). Evaluates whether script aligns with user's stated theme, style, mood, duration, etc.

**Invocation**: Via `task` tool, `subagent_type: ph-videos-scorer-user-intent`. Called by ph-videos-script-generation in Phase 2 (full 7-dim mode).

## Workflow

### Step 1: Call via task tool

Use `task` tool with:

- `description`: Short task description, e.g. "User intent match scoring"
- `prompt`: See Input format below
- `subagent_type`: `ph-videos-scorer-user-intent`

### Step 2: Parse output

Sub-Agent returns format per Output format. Parse `[Score]` and `[Suggestions]` for aggregation and iteration.

## Input Format (task prompt content)

Prompt should include:

1. **User requirements**: Video theme, style, mood, duration, etc.
2. **Script to score**: Full storyboard (one scene per line)

Example:

```
User requirements: Product intro video, portrait, 2D animation style, light and lively, ~30 seconds.

Script to score:
Protagonist: Product manager, dark suit.
Visual style: Business minimal, bright lighting.
...
```

## Output Format

Sub-Agent MUST output strictly in this format for parsing:

```
[Dimension] User Intent Match
[Score] X/10
[Suggestions]
(1-3 actionable, specific suggestions)
```

## Scoring Criteria

| Score | Criteria |
|-------|----------|
| 9-10 | Fully aligned with user intent, theme/style/mood/duration all match |
| 7-8 | Mostly aligned, occasional deviation |
| 4-6 | Deviates from user intent, needs adjustment |
| 0-3 | Off from user intent, needs rewrite |
