---
name: ph-videos-script-generation
description: Use when user wants to generate or optimize video scripts for AI video generation (Seedance/Aliyun Wanxiang/ComfyUI). Employs multi-draft generation (2 versions), 3 specialist scorers, and 1 round of refinement. Proactively call web_search, image_search, deep-research, consulting-analysis, data-analysis, image-generation, video-generation, podcast-generation, github-deep-research, surprise-me, or skill-creator when needed for reference, assets, or inspiration.
---

# ph-videos Video Script Generation Skill (Lite)

## Overview

This skill generates or optimizes AI video storyboard scripts for Volcano Seedance, Aliyun Wanxiang, ComfyUI, and similar platforms. Uses a **lite workflow**: 2 drafts + 3 scorers + 1 iteration round for fast execution.

**Important**: When executing this skill, **proactively call** DeerFlow tools and skills as needed for reference materials and better script quality.

## DeerFlow Tools/Skills Integration (Proactive Calls)

Before Phase 0 or Phase 1, **decide** whether to call the following based on user needs; confirm with the user before executing:

| Capability | Type | When to Call | How |
|------------|------|--------------|-----|
| **web_search** | Tool | User mentions real events, movies, products, people, places—need search for reference details | Call `web_search` directly with search keywords |
| **image_search** | Tool | User needs **image-to-video (i2v)** or wants **reference/style images** | Call `image_search` with image description keywords (e.g. "Japanese street photography 1990s", "cyberpunk city night") to get reference URLs for image-generation or ph-videos-video-generation |
| **deep-research** | Skill | Complex topics needing multi-angle research (industry reports, competitor analysis, historical events) | `read_file` to load `deep-research` SKILL.md, follow its methodology with multi-round web_search + web_fetch |
| **image-generation** | Skill | User needs **i2v** or wants reference images before writing script | `read_file` to load `image-generation` SKILL.md, generate reference images, save to `/mnt/user-data/outputs/` for ph-videos-video-generation |
| **video-generation** | Skill | Optional: User wants single-segment preview (Gemini Veo) to validate | `read_file` to load `video-generation` SKILL.md (DeerFlow built-in Gemini video, different from ph-videos-video-generation) |
| **ph-videos-music-script** | Skill | Phase 5 output when user needs BGM description | `read_file` to load `ph-videos-music-script` SKILL.md, generate music description from final script |
| **ph-videos-music-generation** | Skill | User needs BGM audio (not just description) | `read_file` to load `ph-videos-music-generation` SKILL.md, call Suno/CosyVoice to generate audio for ph-videos-video-generation --bgm-file |
| **consulting-analysis** | Skill | Industry/competitor/market/brand videos needing professional research | `read_file` to load `consulting-analysis` SKILL.md, produce analysis framework or report, then write script from it |
| **data-analysis** | Skill | User uploads Excel/CSV for data-driven videos (sales trends, report interpretation) | `read_file` to load `data-analysis` SKILL.md, analyze data and extract visualization points, then write script |
| **podcast-generation** | Skill | User needs voiceover/narration script or video with commentary | `read_file` to load `podcast-generation` SKILL.md for dialogue-style voiceover, complements ph-videos-music-script |
| **github-deep-research** | Skill | Tech/open-source videos when user provides GitHub project URL | `read_file` to load `github-deep-research` SKILL.md, do repo research, then write tech intro script |
| **surprise-me** | Skill | User says "give me inspiration", "random idea", "something creative" | `read_file` to load `surprise-me` SKILL.md for creative inspiration or unexpected combinations |
| **skill-creator** | Skill | User wants to extend/customize video style or workflow | `read_file` to load `skill-creator` SKILL.md to guide creating custom video generation skill |

**Calling principles**:
- **Search when uncertain**: Use `web_search` for concrete movies, products, events before writing
- **Research complex topics first**: Industry, competitor, tech videos—load `deep-research` or `consulting-analysis` first
- **Analyze data first**: When user uploads Excel/CSV, load `data-analysis` before writing
- **Research tech first**: When user provides GitHub URL, load `github-deep-research` for repo research
- **i2v needs first frame**: For image-to-video, use `image_search` for reference or call `image-generation` for first frame
- **Need inspiration**: When user says "random", "inspiration", "creative", load `surprise-me`

## Core Workflow

### Phase 0: Gather User Requirements (Video Style & Aspect Ratio)

Before generating, **ask or confirm** (use defaults if user does not provide):

| Parameter | Description | Default |
|-----------|--------------|---------|
| **video_style** | 2D / 3D / 2D animation / photorealistic 3D / cartoon | 2D |
| **aspect_ratio** | 16:9 landscape / 9:16 portrait | 16:9 |
| **video_provider** | volcano / wanxiang / comfyui | Per user or config |

These parameters affect script style and are passed to ph-videos-video-generation.

### Phase 1: Dual Draft Generation (2 drafts)

**Must use Sub-Agent mode** to generate **2** script drafts in parallel:

1. Use `task` tool to spawn **2** subtasks (`subagent_type: general-purpose`)
2. Draft 1: `video_generation` style (balanced)
3. Draft 2: `cinematic_shot` style (cinematic)
4. Each draft must follow target platform (volcano/wanxiang/comfyui) prompt formulas

**Prompt variants** (see `references/prompt_templates.md` by video_provider):
- Volcano/ComfyUI: subject + action + shot + style; include "protagonist setting" and "visual style" when involving characters
- Aliyun Wanxiang: subject + scene + motion + aesthetic control + stylization

### Phase 2: Scorer Evaluation

**Lite mode** (3 scorers, total 45, pass line 36):

| Scorer | Dimension | Max | Focus |
|--------|-----------|-----|-------|
| ph-videos-scorer-cinematography | Cinematography | 15 | Shot types, camera movements |
| ph-videos-scorer-description | Description Quality | 15 | Visualizability, concreteness |
| ph-videos-scorer-feasibility | Feasibility | 15 | Model compatibility |

**Full 7-dim mode** (7 scorers, total 90, pass line 72):

| Scorer | Dimension | Max | Focus |
|--------|-----------|-----|-------|
| ph-videos-scorer-cinematography | Cinematography | 15 | Shot types, camera movements |
| ph-videos-scorer-description | Description Quality | 15 | Visualizability, concreteness |
| ph-videos-scorer-coherence | Coherence | 15 | Scene transitions, narrative logic |
| ph-videos-scorer-character | Character Consistency | 10 | Character appearance/style unity |
| ph-videos-scorer-feasibility | Feasibility | 15 | Seedance/Wanxiang/ComfyUI compatibility |
| ph-videos-scorer-user-intent | User Intent Match | 10 | Alignment with user theme/style/mood |
| ph-videos-scorer-style-atmosphere | Style & Atmosphere | 10 | Visual style, lighting, mood consistency |

**Action**: For each script, spawn the corresponding number of `task` subtasks with the above `subagent_type`. **Prefer serial calls** to avoid overload.

### Phase 3: Aggregate & Select

1. Sum scores per dimension for each script (lite max 45, full max 90)
2. **Pass line**: Lite 36, Full 72 (both 80%)
3. **Prefer**: If any script passes, use the highest-scoring one
4. **Else**: Use current highest, proceed to Phase 4

### Phase 4: Iteration (1 round only)

If highest score does not pass (lite < 36, full < 72):

1. Collect **suggestions** from scorers, merge into feedback
2. Optimize script based on feedback (spawn 1 subtask)
3. Re-run Phase 2 with same number of scorers
4. **Only 1 round**, no further iteration

### Phase 5: Output

- Output final script (prefer passing draft, else highest-scoring)
- **Optional**: If user needs BGM, load `ph-videos-music-script` to generate music description
- Output score summary (per-dimension scores, pass/fail)
- **Handoff**: Tell user to call `ph-videos-video-generation` to turn script into video

## Timeout & Fallback

- If a subtask times out (e.g. 120s), **skip** it and continue
- If a scorer returns parse failure, **that dimension scores 0**, excluded from total
- If both drafts fail, **use main Agent to generate 1 draft** as fallback

## Keywords & Triggers

- Video script, storyboard, script optimization, video copy
- Volcano, Doubao, Seedance, Aliyun Wanxiang, ComfyUI
- Text-to-video, image-to-video, novel-to-video

## Output Specification

1. Each segment: one complete, visualizable sentence, 30–80 chars
2. When involving characters: start with "Protagonist: XXX", "Visual style: XXX"
3. Segments separated by newlines, end with period
4. Directly usable by Seedance/Wanxiang/ComfyUI API

## Scorers & Modes

**Lite** (3): cinematography, description, feasibility

**Full 7-dim** (7): cinematography, description, coherence, character, feasibility, user-intent, style-atmosphere

Choose lite or full based on user needs. Full mode suits higher quality requirements.
