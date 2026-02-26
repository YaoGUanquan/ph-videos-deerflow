---
name: ph-videos-music-script
description: Generate BGM/music script from video script and video config. For CosyVoice/Suno or user-uploaded BGM. Use after ph-videos-script-generation produces final script.
---

# ph-videos Music Script Skill

## Overview

Generates BGM descriptions suitable for AI music generation (CosyVoice, Suno, etc.) or user upload from video storyboard scripts and config. **Call after ph-videos-script-generation** produces final script, before or after ph-videos-video-generation.

## Core Capabilities

- Synthesize video content, duration, segments, and mood into BGM description
- Incorporate user music keywords (style, instruments, mood)
- Output under 50 chars, usable by AI music API or manual selection

## Workflow

### Step 1: Prerequisites

- Have **ph-videos-script-generation** final video storyboard script
- Optional: video config (total duration, segment count, resolution, effects)
- Optional: user music keywords (style, instruments, mood)

### Step 2: Analyze Script & Config

- Extract video theme, emotional arc, rhythm changes
- Infer BGM rhythm and structure from segment count and duration
- Naturally incorporate user keywords if provided

### Step 3: Generate BGM Description

Output a music script under 50 chars including:

- **Style**: gentle / uplifting / healing / epic / electronic / classical, etc.
- **Mood**: Matches video scenario
- **Rhythm**: fast / medium / slow, aligned with segment rhythm
- **Instruments**: piano / strings / electronic / guitar, etc.

### Step 4: Output

- Output BGM description to user
- User can use CosyVoice/Suno to generate audio or select music manually

## ph-videos Flow Integration

```
ph-videos-script-generation (script)
        ↓
ph-videos-music-script (this skill, BGM description)  ← optional
        ↓
ph-videos-music-generation (BGM audio)  ← optional, needs SUNO_API_KEY etc.
        ↓
ph-videos-video-generation (video, --bgm-file mix)
```

## Output Specification

1. Under 50 chars, direct music style description
2. Must include: style, mood, rhythm, instruments
3. Match video content, duration rhythm, scenario mood
4. If user keywords provided, incorporate naturally, do not copy verbatim

## Keywords

- BGM, background music, score, music script, CosyVoice, Suno
