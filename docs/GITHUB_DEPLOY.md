# ph-videos-deerflow 项目文件与 GitHub 部署说明

仓库地址：https://github.com/YaoGUanquan/ph-videos-deerflow.git

---

## 一、不应上传到 GitHub 的文件（已配置 .gitignore）

以下文件/目录包含敏感信息或本地生成内容，**已通过 .gitignore 排除**，不会被提交：

### 1. 配置文件（含 API Key、密钥等）

| 文件 | 说明 |
|------|------|
| `config.yaml` | 主配置，含 models、api_key、sandbox 等 |
| `config.local.yaml` | exe 模式本地配置（Local 沙箱） |
| `mcp_config.json` | MCP 服务器配置（可能含 token） |
| `extensions_config.json` | MCP/Skills 扩展配置 |
| `.env` | 环境变量（API Key 等） |

### 2. 运行时 / 缓存 / 生成物

| 目录/文件 | 说明 |
|-----------|------|
| `docker/.cache/` | Docker 镜像缓存 |
| `logs/` | 日志 |
| `coverage/`、`coverage.xml` | 测试覆盖率报告 |
| `.deer-flow/`、`.claude/` | 本地工作区缓存 |
| `skills/custom/*` | 自定义 Skills（个人） |
| `.githooks/` | 本地 Git 钩子 |
| `.pnpm-store` | pnpm 缓存 |
| `sandbox_image_cache.tar` | 沙箱镜像缓存 |

### 3. 开发环境

| 目录/文件 | 说明 |
|-----------|------|
| `.venv/`、`venv/` | Python 虚拟环境 |
| `__pycache__/`、`*.pyc` | Python 缓存 |
| `.idea/` | JetBrains IDE 配置 |
| `web/` | 旧版 web 目录（已废弃） |

---

## 二、应上传到 GitHub 的文件

### 1. 配置模板（无敏感信息，供用户复制使用）

| 文件 | 说明 |
|------|------|
| `config.example.yaml` | 主配置模板 |
| `config.docker.yaml` | Docker 部署配置模板 |
| `extensions_config.example.json` | MCP/Skills 扩展模板 |
| `.env.example` | 环境变量模板 |

### 2. 项目文档

| 文件 | 说明 |
|------|------|
| `README.md` | DeerFlow 主说明 |
| `PROJECT_README.md` | ph-videos 项目说明 |
| `CONTRIBUTING.md` | 贡献指南 |
| `docs/` | 文档目录（含迁移、Skills 等） |

### 3. 源代码

- `backend/`：Python 后端
- `frontend/`：Web 前端
- `skills/public/`：公开 Skills（ph-videos-*）
- `docker/`：Docker 配置
- `electron/`：Electron 打包
- `scripts/`：构建脚本
- `ffmpeg/`：FFmpeg 相关

---

## 三、首次推送前检查清单

```powershell
# 1. 确认敏感文件未被跟踪
git status

# 2. 确认 .gitignore 生效（以下文件不应出现在 git status 中）
#    - config.yaml
#    - config.local.yaml
#    - .env
#    - extensions_config.json
#    - mcp_config.json

# 3. 推送
git remote add origin https://github.com/YaoGUanquan/ph-videos-deerflow.git  # 若尚未添加
git add .
git commit -m "feat: ph-videos-deerflow 项目初始化"
git push -u origin main
```

---

## 四、新环境部署时需本地生成的文件

克隆仓库后，运行 `make config` 或手动复制模板：

```bash
cp config.example.yaml config.yaml
cp extensions_config.example.json extensions_config.json
cp .env.example .env
# 然后编辑 config.yaml、.env 填入 API Key 等
```

Docker 部署时，可将 `config.docker.yaml` 复制为 `config.yaml` 或设置 `DEER_FLOW_CONFIG_PATH=config.docker.yaml`。
