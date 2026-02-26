---
name: ph-videos-scorer-cinematography
description: Specialist scorer for video script CINEMATOGRAPHY dimension. Scores 0-15 based on shot types (wide/medium/close-up), camera movements (push/pull/follow), and visual composition clarity. Invoke via task tool with subagent_type ph-videos-scorer-cinematography.
---

# Cinematography Scorer

## Overview

Scores the **cinematography** dimension of video storyboard scripts (max 15). Evaluates shot types (wide/medium/close-up), camera movements (push/pull/follow/orbit), and composition clarity.

**Invocation**: Via `task` tool, `subagent_type: ph-videos-scorer-cinematography`. Called by ph-videos-script-generation in Phase 2 (serial).

## Workflow

### Step 1: Call via task tool

Use `task` tool with:

- `description`: Short task description, e.g. "Cinematography scoring"
- `prompt`: See Input format below
- `subagent_type`: `ph-videos-scorer-cinematography`

### Step 2: Parse output

Sub-Agent returns format per Output format. Parse `[Score]` and `[Suggestions]` for aggregation and iteration.

## Input Format (task prompt content)

Prompt should include:

1. **User requirements**: Video theme, style, etc.
2. **Script to score**: Full storyboard (one scene per line)
3. **Optional**: Target platform (volcano/wanxiang/comfyui)

Example:

```
User requirements: Product intro short video, cinematic style.

Script to score:
Protagonist: Young woman, dark hair, white shirt.
Visual style: Bright natural light, cinematic quality.
Wide shot, product centered on table, camera slowly pushes in.
Medium shot, hand picks up product, close-up on product details.
...
```

## Output Format

Sub-Agent MUST output strictly in this format for parsing:

```
[Dimension] Cinematography
[Score] X/15
[Suggestions]
(1-3 actionable, specific suggestions)
```

## Scoring Criteria

| Score | Criteria |
|-------|----------|
| 13-15 | Shot types and movements clear, composition layered |
| 10-12 | Shot types or movements mostly clear, occasional vagueness |
| 7-9 | Shot types or movements unclear, hard to guide production |
| 0-6 | Lacks cinematography language, unusable for video generation |
