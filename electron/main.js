/**
 * ph-videos-deerflow Electron 主进程
 * 打开 WebView 访问 DeerFlow (localhost:2026)
 *
 * 使用方式:
 * 1. 开发: 先运行 make dev 启动后端，再运行 electron .
 * 2. 打包: 需先启动后端，或后续集成 PyInstaller 内嵌后端
 */

const { app, BrowserWindow } = require('electron');
const path = require('path');
const http = require('http');

const PORT = 2026;
const BACKEND_URL = `http://localhost:${PORT}`;

let mainWindow = null;

function waitForBackend(maxAttempts = 60, interval = 500) {
  return new Promise((resolve, reject) => {
    let attempts = 0;
    const check = () => {
      http.get(BACKEND_URL, (res) => {
        resolve();
      }).on('error', () => {
        attempts++;
        if (attempts >= maxAttempts) {
          reject(new Error('后端未启动，请先运行 make dev 或 docker compose up'));
        } else {
          setTimeout(check, interval);
        }
      });
    };
    check();
  });
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1280,
    height: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
    },
  });

  mainWindow.loadURL(BACKEND_URL);
  mainWindow.on('closed', () => {
    mainWindow = null;
    app.quit();
  });
}

app.whenReady().then(async () => {
  try {
    await waitForBackend();
    createWindow();
  } catch (err) {
    console.error(err.message);
    const { dialog } = require('electron');
    dialog.showErrorBox('ph-videos-deerflow', err.message + '\n\n请先启动后端: make dev 或 docker compose up');
    app.quit();
  }
});

app.on('window-all-closed', () => {
  app.quit();
});
