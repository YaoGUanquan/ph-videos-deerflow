# ph-videos-deerflow Docker 构建脚本
# 用于云服务器部署

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $ProjectRoot

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  ph-videos-deerflow Docker 构建" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# 检查 Docker
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Write-Host "错误: 未找到 Docker，请先安装 Docker Desktop" -ForegroundColor Red
    exit 1
}

# 生成配置（若不存在）
if (-not (Test-Path "config.yaml")) {
    Write-Host "生成 config.yaml..."
    Copy-Item "config.example.yaml" "config.yaml"
}
if (-not (Test-Path ".env")) {
    Write-Host "生成 .env..."
    Copy-Item ".env.example" ".env"
}

# 使用 Docker 模式配置
$env:DEER_FLOW_CONFIG_PATH = Join-Path $ProjectRoot "config.docker.yaml"
if (-not (Test-Path "config.docker.yaml")) {
    Write-Host "创建 config.docker.yaml（Docker 沙箱模式）..."
    Copy-Item "config.example.yaml" "config.docker.yaml"
}

Write-Host "构建 Docker 镜像..." -ForegroundColor Green
docker compose -p ph-videos-deerflow -f docker/docker-compose-dev.yaml build

Write-Host ""
Write-Host "构建完成！" -ForegroundColor Green
Write-Host "启动: docker compose -p ph-videos-deerflow -f docker/docker-compose-dev.yaml up -d"
Write-Host "访问: http://localhost:2026"
