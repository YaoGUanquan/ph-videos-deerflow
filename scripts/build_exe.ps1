# ph-videos-deerflow exe 打包脚本
# 生成 Electron + 内嵌后端的桌面安装包

$ErrorActionPreference = "Stop"
$ProjectRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $ProjectRoot

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  ph-videos-deerflow exe 打包" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# 1. 检查依赖
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "错误: 未找到 Node.js" -ForegroundColor Red
    exit 1
}
if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    Write-Host "错误: 未找到 uv (Python 包管理)" -ForegroundColor Red
    exit 1
}

# 2. 生成配置（Local 沙箱，无需 Docker）
if (-not (Test-Path "config.yaml")) {
    Copy-Item "config.example.yaml" "config.yaml"
    Write-Host "已生成 config.yaml（Local 沙箱模式）" -ForegroundColor Green
}

# 3. 构建前端
Write-Host "构建前端..." -ForegroundColor Green
Set-Location "$ProjectRoot\frontend"
pnpm run build
if ($LASTEXITCODE -ne 0) { exit 1 }
Set-Location $ProjectRoot

# 4. 安装 Electron 依赖
Write-Host "安装 Electron 依赖..." -ForegroundColor Green
Set-Location "$ProjectRoot\electron"
npm install
if ($LASTEXITCODE -ne 0) { exit 1 }

# 5. 打包 Electron
Write-Host "打包 Electron..." -ForegroundColor Green
npm run build:win
if ($LASTEXITCODE -ne 0) { exit 1 }

Set-Location $ProjectRoot
Write-Host ""
Write-Host "打包完成！" -ForegroundColor Green
Write-Host "输出目录: electron\dist"
Write-Host ""
Write-Host "注意: 当前 Electron 仅打包前端壳，后端需单独运行。" -ForegroundColor Yellow
Write-Host "完整 exe（内嵌后端）需额外配置 PyInstaller 打包 Python，详见 PROJECT_README.md" -ForegroundColor Yellow
