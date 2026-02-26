---
name: ph-videos-video-generation
description: Generate videos from scripts using Volcano Seedance, Aliyun Wanxiang, or ComfyUI. Supports text-to-video, image-to-video, and pipeline (image slideshow). Use after ph-videos-script-generation produces final script.
---

# ph-videos 视频生成 Skill

## 概述

根据 ph-videos-script-generation 产出的分镜脚本，调用视频生成 API 产出最终视频。支持三种平台：

| 平台 | video_provider | 能力 |
|------|----------------|------|
| 火山/豆包 Seedance | volcano | 文生视频(t2v)、图生视频(i2v) |
| 通义万相 | wanxiang | 文生视频(t2v)、图生视频(i2v)、参考生视频(r2v) |
| ComfyUI | comfyui | 文生视频(t2v)，需本地/云端 ComfyUI 服务 |

## 前置条件

1. 已有优化后的视频分镜脚本（来自 ph-videos-script-generation）
2. 图生视频/参考生视频需上传首帧图或参考视频
3. 配置对应平台的 API Key（环境变量或用户配置）

## 工作流

### Step 1：准备脚本与素材

- 脚本：每段一行，30-80 字，可直接输入 API
- 素材：t2v 无需；i2v 需首帧图；r2v 需参考视频

### Step 2：场景拆分

根据脚本分段，确定每段时长与分辨率（如 9:16 竖屏、16:9 横屏）。

### Step 3：调用视频生成

- **火山 Seedance**：使用 `volcengine-python-sdk` 的 `content_generation.tasks` API
- **通义万相**：使用 DashScope 视频生成 API
- **ComfyUI**：提交工作流 JSON 到 ComfyUI 服务

### Step 4：合并与后处理

- 多段视频使用 FFmpeg 或 MoviePy 合并
- 可选：混入 BGM（根据音乐脚本生成或用户上传）

## 输出

- 最终视频文件（如 `/mnt/user-data/outputs/video.mp4`）
- 使用 `present_files` 工具分享给用户

## 关键词

- 火山、豆包、Seedance、通义万相、ComfyUI
- 文生视频、图生视频、视频生成
