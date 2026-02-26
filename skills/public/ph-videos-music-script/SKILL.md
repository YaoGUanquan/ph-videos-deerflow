---
name: ph-videos-music-script
description: Generate BGM/music script from video script and video config. For CosyVoice/Suno or user-uploaded BGM. Use after ph-videos-script-generation produces final script.
---

# ph-videos 音乐脚本生成 Skill

## 概述

根据视频分镜脚本和视频生成配置（时长、分段、特效、情景等），综合生成适合 AI 音乐生成的 BGM 描述。可选结合用户音乐关键词。

## 输入

- 视频分镜脚本（来自 ph-videos-script-generation）
- 视频配置：总时长、分段数、分辨率、特效模板等
- 用户音乐关键词（可选）：风格、乐器、情绪等

## 输出规范

1. 50 字以内，直接描述音乐风格
2. 必须包含：风格（轻柔/激昂/治愈/史诗）、情绪、节奏、乐器（钢琴/弦乐/电子）
3. 与视频内容、时长节奏、情景氛围匹配
4. 若有用户关键词，需自然融入，不得直接照抄

## 关键词

- BGM、背景音乐、配乐、音乐脚本
