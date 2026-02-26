# Script Generation Prompt Templates

Select formulas by video_provider, style variants by script_style, and adjust visual descriptions by video_style.

---

## 0. Video Style (video_style)

When generating scripts, specify video style to guide visual description and cinematography:

| video_style | Description | Key Points |
|-------------|-------------|------------|
| 2D | Flat illustration/comic style | Lines, color blocks, flat composition |
| 3D | 3D realistic | Depth, lighting, depth of field |
| 2D animation | Animation style | Cartoon, exaggerated motion, smooth transitions |
| photorealistic 3D | Film-grade realistic | Realistic lighting, physical texture |
| cartoon | Simplified cartoon | Simple shapes, high contrast colors |

---

## 1. Platform Formulas (video_provider)

### Volcano/Doubao Seedance / ComfyUI

**Formula**: Subject + Action/Motion + Shot/View + Style/Atmosphere

- Subject: Main visual object, including appearance
- Action: Run, turn, traverse, flow; emphasize amplitude and rhythm
- Shot: Shot type (wide/medium/close-up) + Camera movement (push, pull, follow, orbit)
- Style: Lighting (natural, cinematic, golden hour), quality (4K, realistic), style (cinematic, cyberpunk)

**When involving characters**: Start with "Protagonist: XXX", "Visual style: XXX"; repeat appearance anchors when protagonist appears.

### Aliyun Wanxiang Text-to-Video (t2v)

**Formula**: Subject + Scene + Motion + Aesthetic Control + Stylization

- Subject: Appearance details
- Scene: Environment features
- Motion: Amplitude, speed, effect
- Aesthetic control: Light source, lighting, shot type, camera movement
- Stylization: Cyberpunk, line illustration, etc.

**When involving characters**: Same as above, protagonist setting + visual style + appearance anchors.

### Aliyun Wanxiang Image-to-Video (i2v)

**Formula**: Motion + Camera (first frame already defines subject and scene)

- Motion: Describe dynamic process based on image elements
- Camera: Push in, pan left, static shot, etc.

### Aliyun Wanxiang Reference-to-Video (r2v)

**Formula**: Protagonist + Action + Dialogue + Scene

- Use character1, character2 to reference protagonists from reference video
- Action, dialogue, scene flow naturally

---

## 2. Script Style Variants (script_style)

For multi-draft generation, assign different styles to subtasks for diversity.

### video_generation - Video Script Optimization

General style, improves scene description precision and visual guidance. Structure: scene + shot + subject action + lighting atmosphere.

### cinematic_shot - Cinematic Storyboard

Film-grade cinematography, emphasizes lighting, camera movement, atmosphere. Each segment specifies shot type and movement, lighting matches mood.

### product_intro - Product Introduction

For product showcase, marketing copy. Each segment: scene (usage context) + shot (medium/close-up) + product action + lighting (bright, professional). Highlight selling points.

### knowledge_popular - Knowledge Popularization

For educational, science content. Express abstract concepts with concrete visuals (e.g. water flow for electric current). Shots: wide for scene, medium for subject, close-up for detail.

### narrative - Narrative Commentary

For storytelling, documentary. Each segment: scene + shot + character/subject action + emotional atmosphere. Engaging.

### novel_story - Novel to Video

For novel, story adaptation. **Character consistency is critical**: Start with "Protagonist: XXX" (detailed clothing color, hair, age), then "Visual style: XXX". Repeat appearance anchors when protagonist appears.

### short_form_video - Short-Form Script

For TikTok/YouTube Shorts. Strong hook in first 3 seconds (close-up, surprising action), fast pace, 30–60 chars per segment, quick cuts.

### character_consistent - Character-Consistent Script

Multi-character video. Write detailed costume specs per character (main color, top, bottom, accessories, hair), use specific colors like "navy blue", "burgundy". Repeat character definition at segment start.

---

## 3. Style Assignment for Multi-Draft Generation

When generating 3–5 drafts, assign styles per subtask:

| Draft | Suggested Style | Notes |
|-------|-----------------|-------|
| 1 | video_generation | General balance |
| 2 | cinematic_shot | Cinematic enhancement |
| 3 | narrative / novel_story | Narrative/story feel (if content fits) |
| 4 | short_form_video | Fast pace (if targeting short-form) |
| 5 | product_intro / knowledge_popular | By content type |
