---
name: ph-videos-script-generation
description: Use when user wants to generate or optimize video scripts for AI video generation (Seedance/通义万相/ComfyUI). Employs multi-draft generation (2 versions), 3 specialist scorers, and 1 round of refinement. Lightweight for quick execution.
---

# ph-videos 视频脚本生成 Skill（精简版）

## 概述

本 Skill 用于生成或优化 AI 视频分镜脚本，支持火山 Seedance、通义万相、ComfyUI 等平台。采用 **精简流程**：2 稿生成 + 3 个评分员 + 1 轮迭代，确保快速执行、避免卡顿。

## 核心流程

### 阶段 1：双稿生成（2 份）

**必须启用 Sub-Agent 模式**，并行生成 **2 份**脚本初稿：

1. 使用 `task` 工具，同时启动 **2 个**子任务（`subagent_type: general-purpose`）
2. 稿 1：使用 `video_generation` 风格（通用平衡）
3. 稿 2：使用 `cinematic_shot` 风格（电影感增强）
4. 每份脚本需符合目标平台（volcano/wanxiang/comfyui）的提示词公式

**生成 Prompt 变体**（根据 video_provider 选择，见 `references/prompt_templates.md`）：
- 火山/ComfyUI：主体+动作+镜头+风格；涉及人物时含「主角设定」「画面风格」
- 通义万相：主体+场景+运动+美学控制+风格化

### 阶段 2：3 个评分员评分

对**每份脚本**，调用 **3 个**核心评分子任务（精简版仅保留最关键的 3 个维度）：

| 评分员 | 维度 | 满分 | 评分重点 |
|--------|------|------|----------|
| ph-videos-scorer-cinematography | 镜头语言 | 15 | 景别、运镜是否清晰合理 |
| ph-videos-scorer-description | 描述质量 | 15 | 是否具体可视觉化、无空洞 |
| ph-videos-scorer-feasibility | 可执行性 | 15 | 是否适合当前视频模型、用户意图匹配、风格氛围 |

**总分 45 分**（精简版）。**达标线**：36 分（80%）。

**操作**：对每份脚本，spawn 3 个 `task` 子任务，使用上述 3 个 Sub-Agent。**建议串行调用**，避免并发过高导致卡顿。

### 阶段 3：汇总与选优

1. 汇总每份脚本的 3 个维度得分，计算总分（满分 45）
2. **达标线**：36 分（80%）
3. **优先选择**：若存在达标的脚本，直接选用**最高分**的那份
4. **否则**：选用当前最高分，进入阶段 4

### 阶段 4：迭代优化（仅 1 轮）

若最高分未达标（< 36 分）：

1. 收集 3 个评分员的**修改建议**，合并为一份综合反馈
2. 根据反馈对脚本进行优化（spawn 1 个子任务执行优化）
3. 对优化后的脚本重新执行阶段 2（3 个评分员评分）
4. **仅执行 1 轮**，不再重复迭代

### 阶段 5：输出

- 输出最终脚本（达标则优先使用达标稿，否则使用最高分稿）
- 可选输出音乐脚本（BGM 描述）
- 输出评分摘要（各维度得分、是否达标）

## 超时与降级

- 若某子任务超时（如 120 秒），**跳过该子任务**，继续后续流程
- 若某评分员返回解析失败，**该维度计 0 分**，不计入总分
- 若 2 稿均生成失败，**直接使用主 Agent 生成 1 稿**作为备选

## 关键词与触发

- 视频脚本、分镜、脚本优化、视频文案
- 火山、豆包、Seedance、通义万相、ComfyUI
- 文生视频、图生视频、小说转视频

## 输出规范

1. 每段为一句完整、可视觉化的描述，30-80 字
2. 涉及人物时，开头含「主角设定：XXX」「画面风格：XXX」
3. 每段之间换行分隔，以句号结尾
4. 直接可用于 Seedance/通义万相/ComfyUI API

## 参考：精简版使用 3 个评分员

- `ph-videos-scorer-cinematography`：镜头语言
- `ph-videos-scorer-description`：描述质量
- `ph-videos-scorer-feasibility`：可执行性

（完整版 5 个评分员：coherence、character 可在后续扩展时启用）
