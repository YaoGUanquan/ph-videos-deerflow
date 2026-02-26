---
name: ph-videos-scorer-style-atmosphere
description: Specialist scorer for video script STYLE AND ATMOSPHERE. Scores 0-10 based on visual style, mood, lighting, and aesthetic consistency across scenes. Invoke via task tool with subagent_type ph-videos-scorer-style-atmosphere.
---

# Style & Atmosphere Scorer

## Overview

Scores the **style and atmosphere** dimension of video storyboard scripts (max 10). Evaluates whether visual style, lighting, mood, and aesthetic tone are consistent across scenes.

**Invocation**: Via `task` tool, `subagent_type: ph-videos-scorer-style-atmosphere`. Called by ph-videos-script-generation in Phase 2 (full 7-dim mode).

## Workflow

### Step 1: Call via task tool

Use `task` tool with:

- `description`: Short task description, e.g. "Style and atmosphere scoring"
- `prompt`: See Input format below
- `subagent_type`: `ph-videos-scorer-style-atmosphere`

### Step 2: Parse output

Sub-Agent returns format per Output format. Parse `[Score]` and `[Suggestions]` for aggregation and iteration.

## Input Format (task prompt content)

Prompt should include:

1. **User requirements**: Video theme, style, etc.
2. **Script to score**: Full storyboard (one scene per line)

Example:

```
User requirements: Cinematic product promo, dark tone, warm light.

Script to score:
Protagonist: Young woman, dark long hair.
Visual style: Bright natural light, cinematic quality.
Wide shot, product centered on table, camera slowly pushes in.
...
```

## Output Format

Sub-Agent MUST output strictly in this format for parsing:

```
[Dimension] Style & Atmosphere
[Score] X/10
[Suggestions]
(1-3 actionable, specific suggestions)
```

## Scoring Criteria

| Score | Criteria |
|-------|----------|
| 9-10 | Unified style and atmosphere, lighting/mood/aesthetic coherent |
| 7-8 | Mostly unified, occasional style jumps |
| 4-6 | Inconsistent style or atmosphere |
| 0-3 | Chaotic style, fragmented atmosphere |
