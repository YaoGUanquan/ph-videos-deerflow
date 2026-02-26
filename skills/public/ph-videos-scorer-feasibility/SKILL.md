---
name: ph-videos-scorer-feasibility
description: Specialist scorer for video script FEASIBILITY. Scores 0-15 based on model compatibility (Seedance/Wanxiang/ComfyUI). User intent and style/atmosphere are scored by ph-videos-scorer-user-intent and ph-videos-scorer-style-atmosphere. Invoke via task tool with subagent_type ph-videos-scorer-feasibility.
---

# Feasibility Scorer

## Overview

Scores the **feasibility** dimension of video storyboard scripts (max 15). Evaluates whether script is suitable for Seedance/Wanxiang/ComfyUI video models. User intent and style/atmosphere are scored by ph-videos-scorer-user-intent and ph-videos-scorer-style-atmosphere.

**Invocation**: Via `task` tool, `subagent_type: ph-videos-scorer-feasibility`. Called by ph-videos-script-generation in Phase 2 (serial).

## Workflow

### Step 1: Call via task tool

Use `task` tool with:

- `description`: Short task description, e.g. "Feasibility scoring"
- `prompt`: See Input format below
- `subagent_type`: `ph-videos-scorer-feasibility`

### Step 2: Parse output

Sub-Agent returns format per Output format. Parse `[Score]` and `[Suggestions]` for aggregation and iteration.

## Input Format (task prompt content)

Prompt should include:

1. **User requirements**: Video theme, style, etc.
2. **Target platform**: volcano / wanxiang / comfyui
3. **Script to score**: Full storyboard (one scene per line)

Example:

```
User requirements: Product intro video, portrait, 2D animation style.

Target platform: wanxiang (Aliyun Wanxiang)

Script to score:
Protagonist: Product manager, dark suit.
Visual style: Business minimal, bright lighting.
...
```

## Output Format

Sub-Agent MUST output strictly in this format for parsing:

```
[Dimension] Feasibility
[Score] X/15
[Suggestions]
(1-3 actionable, specific suggestions)
```

## Scoring Criteria

| Score | Criteria |
|-------|----------|
| 13-15 | Suitable for target video model, clear format, no ambiguity |
| 10-12 | Mostly suitable, occasional model-incompatible descriptions |
| 7-9 | Some descriptions unsuitable or hard for model to understand |
| 0-6 | Hard for video model to understand or generate |
