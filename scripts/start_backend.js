/**
 * ph-videos-deerflow 后端启动脚本（Windows/Node）
 * 用于 Electron exe 模式：启动 langgraph + gateway
 * 注意：完整部署还需 nginx + frontend，此处为简化版
 */

const { spawn } = require('child_process');
const path = require('path');

const projectRoot = path.join(__dirname, '..');
const backendDir = path.join(projectRoot, 'backend');

const env = {
  ...process.env,
  DEER_FLOW_CONFIG_PATH: path.join(projectRoot, 'config.yaml'),
};

// 启动 LangGraph
const langgraph = spawn('uv', ['run', 'langgraph', 'dev', '--no-browser', '--allow-blocking', '--port', '2024'], {
  cwd: backendDir,
  env,
  stdio: 'inherit',
});

// 启动 Gateway
const gateway = spawn('uv', ['run', 'uvicorn', 'src.gateway.app:app', '--host', '0.0.0.0', '--port', '8001'], {
  cwd: backendDir,
  env,
  stdio: 'inherit',
});

[langgraph, gateway].forEach((p) => {
  p.on('error', (e) => console.error(e));
  p.on('exit', (code) => {
    if (code !== 0) process.exit(code || 1);
  });
});
