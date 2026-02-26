# ph-videos-deerflow

基于 [DeerFlow 2.0](https://github.com/bytedance/deer-flow) 的视频生成项目，整合 [ph-videos-text](https://github.com/your-org/ph-videos-text) 的脚本生成、视频生成（火山/通义/ComfyUI）等能力。

## 特性

- **双模式部署**：支持 Docker 云部署 + Electron exe 本地安装包
- **统一代码库**：一套代码，两种交付方式
- **基于 DeerFlow**：Skills、Sub-Agents、沙箱、长期记忆

## 部署方式

| 方式 | 适用场景 | 构建命令 |
|------|----------|----------|
| **Docker** | 云服务器、团队使用 | `.\scripts\build_docker.ps1` |
| **exe 安装包** | 本地 Windows 用户 | `.\scripts\build_exe.ps1` |

## 快速开始

### 1. 初始化配置

```bash
make config
```

### 2. Docker 部署（云服务器）

```powershell
# Windows
.\scripts\build_docker.ps1
docker-compose -f docker/docker-compose.prod.yaml up -d

# 访问 http://服务器IP:2026
```

### 3. 本地开发

```bash
make install
make dev
# 访问 http://localhost:2026
```

### 4. exe 打包（本地）

```powershell
.\scripts\build_exe.ps1
# 输出: electron/dist/
```

**说明**：当前 exe 为「壳」模式，需先启动后端（`make dev` 或 Docker）。完整内嵌后端的 exe 需额外配置 PyInstaller，见后续迭代。

## 目录结构

```
ph-videos-deerflow/
├── backend/           # DeerFlow Python 后端
├── frontend/          # DeerFlow Web UI
├── skills/public/     # Skills
│   ├── ph-videos-script-generation/   # 主脚本生成（多稿+多评分员+迭代）
│   ├── ph-videos-scorer-cinematography # 镜头语言评分员
│   ├── ph-videos-scorer-description    # 描述质量评分员
│   ├── ph-videos-scorer-coherence      # 连贯性评分员
│   ├── ph-videos-scorer-character      # 角色一致性评分员
│   ├── ph-videos-scorer-feasibility    # 可执行性评分员
│   ├── ph-videos-video-generation/     # 视频生成（火山/通义/ComfyUI）
│   └── ph-videos-music-script/         # 音乐脚本生成
├── docker/            # Docker 部署
├── electron/          # Electron exe 打包
├── scripts/           # 构建脚本
├── config.local.yaml  # exe 模式配置（Local 沙箱）
└── config.docker.yaml # Docker 模式配置
```

## 配置切换

- **Docker 部署**：使用 `config.docker.yaml`（Docker 沙箱）
- **exe 模式**：使用 `config.local.yaml`（Local 沙箱，无需 Docker）

## 与 ph-videos-text 的关系

- **ph-videos-text**：独立项目，Flask + PyInstaller，专注本地 exe
- **ph-videos-deerflow**：本项目，DeerFlow + Docker/Electron，支持云 + 桌面

## 许可证

MIT
