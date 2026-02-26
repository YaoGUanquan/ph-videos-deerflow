---
name: ph-videos-scorer-character
description: Specialist scorer for video script CHARACTER CONSISTENCY. Scores 0-10 when script involves characters - appearance, style, and visual anchors across scenes. Invoke via task tool with subagent_type ph-videos-scorer-character.
---

# Character Consistency Scorer

## Overview

Scores the **character consistency** dimension of video storyboard scripts (max 10). **Only when script involves characters**; if no characters, output 10/10 and note "No characters involved". Evaluates protagonist setting, visual style, and appearance anchors across segments.

**Invocation**: Via `task` tool, `subagent_type: ph-videos-scorer-character`. Used in full ph-videos-script-generation (lite uses 3 scorers).

## Workflow

### Step 1: Call via task tool

Use `task` tool with:

- `description`: Short task description, e.g. "Character consistency scoring"
- `prompt`: See Input format below
- `subagent_type`: `ph-videos-scorer-character`

### Step 2: Parse output

Sub-Agent returns format per Output format. If no characters, score is fixed at 10/10.

## Input Format (task prompt content)

Prompt should include:

1. **User requirements**: Video theme, style, etc.
2. **Script to score**: Full storyboard (one scene per line)

Example (with characters):

```
User requirements: Novel to video, protagonist is a young girl.

Script to score:
Protagonist: Young girl, brown long hair, white dress, 16 years old.
Visual style: Fresh Japanese animation.
Wide shot, girl standing under cherry tree.
Medium shot, girl turns and smiles.
...
```

## Output Format

Sub-Agent MUST output strictly in this format for parsing:

```
[Dimension] Character Consistency
[Score] X/10
[Suggestions]
(1-3 actionable suggestions; if no characters, write "No characters involved, no changes needed")
```

## Scoring Criteria

| Score | Criteria |
|-------|----------|
| 9-10 | Has "protagonist setting" and "visual style", repeats appearance anchors when protagonist appears, multi-segment video can maintain same character |
| 7-8 | Basic setting present, occasional missing anchors |
| 4-6 | Incomplete setting or many missing anchors |
| 0-3 | No character setting or contradictory character descriptions across segments |
