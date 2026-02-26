---
name: ph-videos-music-generation
description: Generate BGM audio from music script (ph-videos-music-script output). Supports Suno API or CosyVoice integration. Output audio for ph-videos-video-generation --bgm-file. Use after ph-videos-music-script produces BGM description.
---

# ph-videos BGM Generation Skill

## Overview

Generates BGM audio from ph-videos-music-script descriptions via AI music APIs (Suno, CosyVoice, etc.) for ph-videos-video-generation to mix into video.

## Core Capabilities

- Accept BGM description (style, mood, rhythm, instruments)
- Support Suno API (requires SUNO_API_KEY)
- Support CosyVoice local/API (requires config)
- Output mp3/wav for `generate.py --bgm-file`

## ph-videos Flow Integration

```
ph-videos-script-generation (script)
        ↓
ph-videos-music-script (BGM description)
        ↓
ph-videos-music-generation (this skill, BGM audio)  ← optional
        ↓
ph-videos-video-generation (video, --bgm-file mix)
```

## Workflow

### Step 1: Prerequisites

- Have **ph-videos-music-script** BGM description (under 50 chars, style/mood/rhythm/instruments)
- Optional: SUNO_API_KEY or CosyVoice config

### Step 2: Execute Generation

Call the script (**Do NOT read the python file, just call it with the parameters**):

```bash
python /mnt/skills/public/ph-videos-music-generation/scripts/generate.py \
  --description "Gentle piano, healing, medium tempo, suitable for product promo" \
  --output /mnt/user-data/outputs/bgm.mp3 \
  --duration 30
```

Parameters:

- `--description`: BGM description from ph-videos-music-script (required)
- `--output`: Output audio path (required)
- `--duration`: Target duration in seconds (default 30)
- `--description-file`: Optional, read description from file (instead of --description)

### Step 3: Environment Variables

| Variable | Description |
|----------|-------------|
| SUNO_API_KEY | Suno API Key; if set, calls Suno to generate |
| COSYVOICE_API_URL | CosyVoice API URL (optional) |
| COSYVOICE_API_KEY | CosyVoice API Key (optional) |

If no API configured, script saves description to `.txt` and prompts user to use CosyVoice/Suno manually.

### Step 4: Video Generation Integration

After generating BGM, pass `--bgm-file` to ph-videos-video-generation:

```bash
python /mnt/skills/public/ph-videos-video-generation/scripts/generate.py \
  --provider volcano \
  --script-file /mnt/user-data/workspace/script.txt \
  --output /mnt/user-data/outputs/video.mp4 \
  --bgm-file /mnt/user-data/outputs/bgm.mp3 \
  --bgm-volume 0.3
```

## Output Specification

- Format: mp3 or wav
- Save path: `/mnt/user-data/outputs/`
- Use `present_files` tool to share with user

## Keywords

- BGM generation, music generation, Suno, CosyVoice, ph-videos-music-script
