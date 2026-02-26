# ph-videos Skills 说明

基于 ph-videos-text 能力迁移，结合 DeerFlow 2.0 的 Sub-Agents、并行任务等特性进行优化。

## 核心优化

### 1. 多稿生成（精简版：2 份）

- 一次性生成 **2 份**脚本初稿，每份使用不同风格（video_generation、cinematic_shot）
- 通过 Sub-Agent 并行执行
- 支持 8 种脚本风格，精简版默认使用前 2 种

### 2. 专业评分员（精简版：3 个）

| Sub-Agent | 维度 | 满分 | 精简版 |
|-----------|------|------|--------|
| ph-videos-scorer-cinematography | 镜头语言 | 15 | ✅ 使用 |
| ph-videos-scorer-description | 描述质量 | 15 | ✅ 使用 |
| ph-videos-scorer-feasibility | 可执行性 | 15 | ✅ 使用 |
| ph-videos-scorer-coherence | 连贯性 | 15 | 完整版 |
| ph-videos-scorer-character | 角色一致性 | 10 | 完整版 |

- 精简版总分 45，达标线 36（80%）
- 建议**串行调用**评分员，避免并发过高卡顿

### 3. 迭代优化（精简版：1 轮）

- 若最高分未达标，收集 3 个评分员的修改建议
- 根据反馈优化脚本，重新评分
- **仅执行 1 轮**，不再重复

### 4. 提示词与平台适配

- 火山/ComfyUI：Seedance 公式（主体+动作+镜头+风格）
- 通义万相：t2v/i2v/r2v 分别有专用公式
- 涉及人物时：主角设定、画面风格、外观锚点

### 5. 视频生成对接

- `ph-videos-video-generation` 已对接 ph-videos-text 的 video clients
- 支持火山 Seedance、通义万相、ComfyUI
- 可设置 `PH_VIDEOS_TEXT_PATH` 复用 ph-videos-text 项目，或使用技能内置 lib

## 使用流程

1. 用户输入主题/大纲
2. 加载 `ph-videos-script-generation` Skill
3. Agent 按流程：多稿生成 → 多评分员评分（使用 ph-videos-scorer-* Sub-Agent）→ 选优/迭代 → 输出
4. 可选加载 `ph-videos-music-script` 生成 BGM 描述
5. 可选加载 `ph-videos-video-generation` 调用视频 API 生成视频

## 关键词触发

- 视频脚本、分镜、脚本优化、视频文案
- 火山、豆包、Seedance、通义万相、ComfyUI
- 文生视频、图生视频、小说转视频
