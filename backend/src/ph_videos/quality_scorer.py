"""视频质量评分（简化版）：文件存在 + 时长校验。"""

import json
import logging
import os
import platform
import shutil
import subprocess
from pathlib import Path

logger = logging.getLogger(__name__)

# 添加 skill lib 路径
_BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
_SKILL_ROOT = _BACKEND_DIR.parent / "skills" / "public" / "ph-videos-video-generation"


def _get_ffmpeg_path() -> str | None:
    """获取 ffprobe 路径（与 ffmpeg 同目录）。"""
    sys_path = _SKILL_ROOT
    if sys_path.exists():
        import sys
        if str(sys_path) not in sys.path:
            sys.path.insert(0, str(sys_path))
    try:
        from lib.ffmpeg_utils import get_ffmpeg_path
        path = get_ffmpeg_path()
        if path:
            ffprobe_dir = os.path.dirname(path)
            name = "ffprobe.exe" if platform.system().lower() == "windows" else "ffprobe"
            ffprobe = os.path.join(ffprobe_dir, name)
            if os.path.isfile(ffprobe):
                return ffprobe
            return shutil.which("ffprobe")
    except ImportError:
        pass
    return shutil.which("ffprobe")


def _get_duration_seconds(video_path: str) -> float:
    """获取视频时长（秒）。"""
    ffprobe = _get_ffmpeg_path()
    if not ffprobe:
        return 0.0
    try:
        r = subprocess.run(
            [
                ffprobe,
                "-v", "quiet",
                "-print_format", "json",
                "-show_format",
                "-i", video_path,
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if r.returncode != 0:
            return 0.0
        data = json.loads(r.stdout)
        dur = data.get("format", {}).get("duration")
        return float(dur) if dur else 0.0
    except Exception:
        return 0.0


class QualityScorer:
    """简化版视频质量评分：文件存在 + 时长 > 0。"""

    def __init__(self, min_duration_sec: float = 0.5) -> None:
        self.min_duration_sec = min_duration_sec

    async def score(self, video_path: str, scene_prompt: str = "") -> float:
        """
        对生成视频打分，0-1。

        简化版：文件存在且时长 > min_duration_sec 则返回 0.85，否则 0.3。

        Args:
            video_path: 视频文件路径
            scene_prompt: 场景描述（预留，后续可接入 vision 模型）

        Returns:
            0.0-1.0
        """
        if not video_path or not os.path.isfile(video_path):
            return 0.0
        size = os.path.getsize(video_path)
        if size < 1024:
            return 0.0
        duration = _get_duration_seconds(video_path)
        if duration < self.min_duration_sec:
            return 0.3
        return 0.85
