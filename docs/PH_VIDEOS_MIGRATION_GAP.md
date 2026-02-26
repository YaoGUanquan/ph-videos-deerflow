# ph-videos-text → ph-videos-deerflow 移植情况对照

**检查日期**: 2026-02-26

---

## 一、已移植功能 ✅

| 功能模块 | ph-videos-text | ph-videos-deerflow | 说明 |
|----------|----------------|-------------------|------|
| **视频客户端** | seedance_video_client, wanxiang_video_client, comfyui_video_client | lib/seedance_client, wanxiang_client, comfyui_client | 优先 PH_VIDEOS_TEXT_PATH 复用，否则内置 |
| **视频生成脚本** | video_generation_task 调用各 client | scripts/generate.py | 支持 volcano/wanxiang/comfyui，多段 FFmpeg 合并 |
| **FFmpeg** | ffmpeg_path.py, setup_ffmpeg.py | ffmpeg_utils.py, scripts/setup_ffmpeg.py, ffmpeg/ | 含 imageio-ffmpeg、项目内置、PH_VIDEOS_TEXT_PATH |
| **脚本风格** | skills.py SCRIPT_SKILLS (8 种) | prompt_templates.md | video_generation, cinematic_shot, product_intro, knowledge_popular 等 |
| **平台公式** | prompt_variants (volcano/wanxiang/comfyui) | prompt_templates.md | 火山/通义 t2v/i2v/r2v/ComfyUI 公式 |
| **脚本评分** | script_quality_reviewer (7 维度) | 5 个 ph-videos-scorer-* Sub-Agent | 镜头语言、描述质量、连贯性、角色一致性、可执行性 |
| **BGM 描述** | 无独立模块，在 video_params 中 | ph-videos-music-script Skill | 生成 BGM 描述供 CosyVoice/Suno 或用户上传 |
| **前端配置** | sessionStorage (ph_videos_llm_config) | localStorage (ph_videos_config) | API Key、provider 等仅前端存储 |

---

## 二、未移植 / 部分移植 ⚠️

### 1. 场景拆分（intelligent_scene_splitter）

| 项目 | 状态 |
|------|------|
| ph-videos-text | `intelligent_scene_splitter.split_scenes()`：根据 prompt、scene_count、duration 智能拆分场景 |
| ph-videos-deerflow | **未移植**。脚本生成由 Agent 直接输出多段，无独立场景拆分服务 |

**影响**：DeerFlow 依赖 Agent 在 prompt 中要求「每段一行」，由 LLM 自行分段，逻辑上等价但无显式 scene_count/duration 控制。

---

### 2. 音视频合并（BGM 混入）

| 项目 | 状态 |
|------|------|
| ph-videos-text | `audio_video_merger`：视频 + BGM 混音、保留原音轨混音、音量控制 |
| ph-videos-deerflow | **未移植**。generate.py 仅做多段视频 concat，无 BGM 混入 |

**影响**：无 BGM 混入能力。ph-videos-music-script 只生成 BGM 描述，需用户自行用 CosyVoice/Suno 生成音频后混入。

---

### 3. 脚本质量把关（7 维度 + 迭代优化）

| 项目 | 状态 |
|------|------|
| ph-videos-text | `script_quality_reviewer`：7 维度评分、多格式解析、迭代优化、`/api/script/optimize-with-review` |
| ph-videos-deerflow | **部分移植**：5 个 Sub-Agent 覆盖 5 个维度，无「与用户意图匹配」「风格与氛围」；主 Agent 负责选优/迭代，无独立 API |

**差异**：ph-videos-text 有 7 维（含与用户意图匹配、风格与氛围），DeerFlow 精简为 5 维（精简版 3 维）。

---

### 4. 提示词解析链路（script_prompt_resolver）

| 项目 | 状态 |
|------|------|
| ph-videos-text | `script_prompt_resolver.get_script_prompt(skill_cfg, video_provider, wanxiang_mode, shot_type)` 动态选择 prompt |
| ph-videos-deerflow | **未移植**。prompt_templates.md 为静态参考，由 Agent/Skill 自行选用，无程序化 resolver |

**影响**：依赖 Agent 理解 prompt_templates，无按 video_provider/wanxiang_mode 自动选 prompt 的逻辑。

---

### 5. 视频处理流水线（video_pipeline）

| 项目 | 状态 |
|------|------|
| ph-videos-text | `VideoPipeline`、`HTMLFrameGenerator`：图文流水线、HTML 模板生成 |
| ph-videos-deerflow | **未移植**。无 pipeline 编排、无 HTML 模板生成 |

**影响**：无「图文流水线」类复杂编排能力。

---

### 6. 其他视频客户端（runcomfy、liblibai）

| 项目 | 状态 |
|------|------|
| ph-videos-text | `runcomfy_video_client`、`liblibai_video_client`：ComfyUI 云端 API |
| ph-videos-deerflow | **未移植**。仅 comfyui_client（本地/ComfyKit） |

**影响**：无 RunComfy、LibLibAI 等云端 ComfyUI 能力。

---

### 7. OSS 素材上传

| 项目 | 状态 |
|------|------|
| ph-videos-text | `oss_client.upload_materials_to_oss`：图生视频/参考生视频需公网 URL 时上传 OSS |
| ph-videos-deerflow | **未移植**。generate.py 注释「本地路径需转为 URL」，无 OSS 实现 |

**影响**：i2v/r2v 需公网图片/参考视频 URL 时，需用户自行上传或配置。

---

### 8. BGM 生成（bgm_generator）

| 项目 | 状态 |
|------|------|
| ph-videos-text | `bgm_generator`：根据音乐脚本调用 AI 生成 BGM 音频 |
| ph-videos-deerflow | **未移植**。ph-videos-music-script 仅生成 BGM 描述，无音频生成 |

**影响**：BGM 需用户自行用 CosyVoice/Suno 等生成或上传。

---

### 9. 完整 Web 界面

| 项目 | 状态 |
|------|------|
| ph-videos-text | `templates/index.html`：配置、脚本输入、视频预览、进度、BGM、合并方案选择等 |
| ph-videos-deerflow | **部分**：设置中「视频生成」页仅 API Key 等配置，无脚本输入、预览、进度等 |

**影响**：DeerFlow 以 Agent 对话为主，无 ph-videos-text 那种完整配置+预览界面。

---

## 三、架构差异说明

| 维度 | ph-videos-text | ph-videos-deerflow |
|------|----------------|-------------------|
| **运行模式** | Flask Web + 同步任务 API | Agent 对话 + 沙箱执行脚本 |
| **配置传递** | 请求体 llm_config 随每次请求传递 | 前端 localStorage，沙箱需 env 或另行注入 |
| **脚本生成** | 后端 LLM 直接调用 | Agent 通过 Sub-Agent 多稿生成 + 评分 |
| **视频生成** | 后端 task 调用 video clients | Agent 调用 generate.py（沙箱内） |
| **API Key** | 请求体传入，不落盘 | 前端 localStorage，沙箱需 VOLCANO_API_KEY 等 env |

---

## 四、建议补齐项（按优先级）

| 优先级 | 项目 | 说明 |
|--------|------|------|
| P1 | **API Key 注入沙箱** | 前端 localStorage 的配置需在沙箱执行时注入为 env，否则 generate.py 无法获取 |
| P2 | **BGM 混入** | 在 generate.py 或独立脚本中接入 audio_video_merger 逻辑 |
| P3 | **场景拆分** | 可选：将 intelligent_scene_splitter 封装为 Sub-Agent 或脚本 |
| P4 | **OSS 上传** | 若支持 i2v/r2v 且需公网 URL，可接入 oss_client |
| P5 | **runcomfy/liblibai** | 若需云端 ComfyUI，可移植对应 client |

---

## 五、总结

**已移植**：视频客户端（Seedance/Wanxiang/ComfyUI）、FFmpeg、脚本风格与平台公式、5 个评分员 Sub-Agent、BGM 描述生成、前端配置存储。

**未移植**：场景拆分、音视频合并（BGM 混入）、7 维质量把关+迭代 API、提示词 resolver、视频流水线、runcomfy/liblibai、OSS、BGM 音频生成、完整 Web 界面。

**关键缺口**：前端保存的 API Key 未注入沙箱，视频生成脚本在沙箱内无法直接使用这些配置。
