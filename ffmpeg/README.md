# FFmpeg 内置二进制

视频生成（多段合并）需要 FFmpeg。首次使用前请执行：

```bash
python scripts/setup_ffmpeg.py
```

或使用 `--all` 同时下载 Linux 和 Windows 版本（用于 CI/跨平台打包）。

下载完成后，`ffmpeg/windows/` 或 `ffmpeg/linux/` 下将包含 `ffmpeg` 和 `ffprobe`。

**备选方案**：
- `pip install imageio-ffmpeg`（ph-videos-video-generation 的 requirements.txt 已包含）
- 设置 `PH_VIDEOS_TEXT_PATH` 指向 ph-videos-text 项目以复用其 ffmpeg
