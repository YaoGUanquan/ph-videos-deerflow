---
name: ph-videos-scorer-coherence
description: Specialist scorer for video script COHERENCE. Scores 0-15 based on scene transitions, narrative logic, and continuity. Invoke via task tool with subagent_type ph-videos-scorer-coherence.
---

# Coherence Scorer

## Overview

Scores the **coherence** dimension of video storyboard scripts (max 15). Evaluates scene transitions, narrative logic, and continuity in action/camera/mood across segments.

**Invocation**: Via `task` tool, `subagent_type: ph-videos-scorer-coherence`. Used in full ph-videos-script-generation (lite uses 3 scorers).

## Workflow

### Step 1: Call via task tool

Use `task` tool with:

- `description`: Short task description, e.g. "Coherence scoring"
- `prompt`: See Input format below
- `subagent_type`: `ph-videos-scorer-coherence`

### Step 2: Parse output

Sub-Agent returns format per Output format. Parse `[Score]` and `[Suggestions]` for aggregation and iteration.

## Input Format (task prompt content)

Prompt should include:

1. **User requirements**: Video theme, style, etc.
2. **Script to score**: Full storyboard (one scene per line)

Example:

```
User requirements: Product promo, 3 scenes.

Script to score:
Scene 1: Product close-up, camera pulls back to show environment.
Scene 2: User using product, medium shot.
Scene 3: Product logo and slogan, close-up.
```

## Output Format

Sub-Agent MUST output strictly in this format for parsing:

```
[Dimension] Coherence
[Score] X/15
[Suggestions]
(1-3 actionable, specific suggestions)
```

## Scoring Criteria

| Score | Criteria |
|-------|----------|
| 13-15 | Smooth scene transitions, clear narrative logic, coherent action/camera/mood |
| 10-12 | Mostly coherent, occasional jumps |
| 7-9 | Noticeable gaps or logic breaks |
| 0-6 | Jumpy scenes, narrative confusion |
