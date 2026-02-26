---
name: ph-videos-scorer-description
description: Specialist scorer for video script DESCRIPTION QUALITY. Scores 0-15 based on visualizability, concreteness, and absence of abstract/vague terms. Invoke via task tool with subagent_type ph-videos-scorer-description.
---

# Description Quality Scorer

## Overview

Scores the **description quality** dimension of video storyboard scripts (max 15). Evaluates whether descriptions are concrete, visualizable, and free of vague/abstract terms; whether each segment is directly usable for AI video generation.

**Invocation**: Via `task` tool, `subagent_type: ph-videos-scorer-description`. Called by ph-videos-script-generation in Phase 2 (serial).

## Workflow

### Step 1: Call via task tool

Use `task` tool with:

- `description`: Short task description, e.g. "Description quality scoring"
- `prompt`: See Input format below
- `subagent_type`: `ph-videos-scorer-description`

### Step 2: Parse output

Sub-Agent returns format per Output format. Parse `[Score]` and `[Suggestions]` for aggregation and iteration.

## Input Format (task prompt content)

Prompt should include:

1. **User requirements**: Video theme, style, etc.
2. **Script to score**: Full storyboard (one scene per line)

Example:

```
User requirements: Convert novel excerpt to video storyboard.

Script to score:
Protagonist: Teen boy, black short hair, school uniform.
Visual style: Japanese animation style.
Morning, sunlight through curtains, boy sits up from bed.
...
```

## Output Format

Sub-Agent MUST output strictly in this format for parsing:

```
[Dimension] Description Quality
[Score] X/15
[Suggestions]
(1-3 actionable, specific suggestions)
```

## Scoring Criteria

| Score | Criteria |
|-------|----------|
| 13-15 | Concrete, visualizable, no vague/abstract terms, each segment directly usable |
| 10-12 | Mostly concrete, occasional generic phrasing |
| 7-9 | Many abstract/vague descriptions, need more detail |
| 0-6 | Vague descriptions, cannot guide video generation |
