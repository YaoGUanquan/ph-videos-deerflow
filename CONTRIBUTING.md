# Contributing to ph-videos-deerflow

感谢你对 ph-videos-deerflow 项目的关注！本指南将帮助你搭建开发环境并了解开发流程。

## 开发环境搭建

我们提供两种开发环境，**推荐使用 Docker** 以获得一致、便捷的体验。

### 方式一：Docker 开发（推荐）

Docker 提供隔离、预配置的环境，无需在本地安装 Node.js、Python 或 nginx。

#### 前置要求

- Docker Desktop 或 Docker Engine
- pnpm（用于缓存优化）

#### 搭建步骤

1. **配置应用**：
   ```bash
   cp config.example.yaml config.yaml
   export OPENAI_API_KEY="your-key-here"
   # 或直接编辑 config.yaml
   ```

2. **初始化 Docker 环境**（首次）：
   ```bash
   make docker-init
   ```

3. **启动开发服务**：
   ```bash
   make docker-start
   ```

4. **访问应用**：http://localhost:2026

### 方式二：本地开发

如需在本地直接运行服务：

#### 前置要求

```bash
make check
```

需要：Node.js 22+、pnpm、uv、nginx

#### 搭建步骤

1. **配置应用**（同上）
2. **安装依赖**：`make install`
3. **启动开发服务**：`make dev`
4. **访问应用**：http://localhost:2026

## 项目结构

```
ph-videos-deerflow/
├── config.example.yaml
├── config.docker.yaml
├── Makefile
├── backend/           # Python 后端
├── frontend/         # Web 前端
├── skills/public/    # Skills（含 ph-videos-*）
├── docker/
├── electron/
└── scripts/
```

## 开发流程

1. 创建功能分支：`git checkout -b feature/your-feature-name`
2. 修改代码（支持热重载）
3. 提交：`git commit -m "feat: 描述"`
4. 推送并创建 Pull Request

## 测试

```bash
cd backend && uv run pytest
cd frontend && pnpm test
```

## 文档

- [配置指南](backend/docs/CONFIGURATION.md)
- [架构概览](backend/CLAUDE.md)
- [GitHub 部署](docs/GITHUB_DEPLOY.md)

## 需要帮助？

- 查看 [Issues](https://github.com/YaoGUanquan/ph-videos-deerflow/issues)
- 阅读 [文档](backend/docs/)

## 许可证

贡献即表示同意以 [MIT License](./LICENSE) 授权。
