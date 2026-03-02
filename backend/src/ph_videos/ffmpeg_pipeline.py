"""FFmpeg 管线封装，复用 skills 中的 ffmpeg_utils。"""

import os
import subprocess
import sys
import tempfile
from pathlib import Path


def _load_ffmpeg_utils():
    """延迟加载 ffmpeg_utils，避免循环依赖。"""
    backend_dir = Path(__file__).resolve().parent.parent.parent
    skill_root = backend_dir.parent / "skills" / "public" / "ph-videos-video-generation"
    if skill_root.exists() and str(skill_root) not in sys.path:
        sys.path.insert(0, str(skill_root))
    try:
        from lib.ffmpeg_utils import (
            get_ffmpeg_path,
            get_ffmpeg_run_env,
            merge_video_with_bgm,
        )
        return get_ffmpeg_path, get_ffmpeg_run_env, merge_video_with_bgm
    except ImportError:
        return None, None, None


class FFmpegPipeline:
    """FFmpeg 视频处理管线，封装 concat 与 BGM 混入。"""

    def __init__(self) -> None:
        gf, ge, _ = _load_ffmpeg_utils()
        self._ffmpeg_path = gf() if gf else None
        env = ge() if ge else None
        self._run_env = env if isinstance(env, dict) else {}

    def is_available(self) -> bool:
        """检查 FFmpeg 是否可用。"""
        return bool(self._ffmpeg_path)

    def concat_videos(self, paths: list[str], output: str) -> str:
        """
        将多个视频文件按顺序合并为一个。

        Args:
            paths: 视频文件路径列表
            output: 输出文件路径

        Returns:
            输出文件路径

        Raises:
            RuntimeError: FFmpeg 不可用或合并失败
        """
        if not self._ffmpeg_path:
            raise RuntimeError("未找到 FFmpeg，无法合并视频")
        if not paths:
            raise ValueError("paths 不能为空")

        if len(paths) == 1:
            import shutil
            os.makedirs(os.path.dirname(output) or ".", exist_ok=True)
            shutil.copy(paths[0], output)
            return output

        run_env = os.environ.copy()
        run_env.update(self._run_env)

        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            list_path = f.name
            for p in paths:
                abs_p = os.path.abspath(p)
                f.write(f"file '{abs_p}'\n")

        try:
            os.makedirs(os.path.dirname(output) or ".", exist_ok=True)
            subprocess.run(
                [
                    self._ffmpeg_path,
                    "-y",
                    "-f", "concat",
                    "-safe", "0",
                    "-i", list_path,
                    "-c", "copy",
                    output,
                ],
                check=True,
                capture_output=True,
                env=run_env,
                timeout=300,
            )
            return output
        finally:
            try:
                os.unlink(list_path)
            except OSError:
                pass

    def add_bgm(
        self,
        video_path: str,
        bgm_path: str,
        output_path: str,
        bgm_volume: float = 0.3,
    ) -> str:
        """
        将 BGM 混入视频。若视频有原音轨则混音，若无则添加 BGM 为 sole 音轨。

        Args:
            video_path: 视频文件路径
            bgm_path: BGM 音频文件路径（mp3/wav 等）
            output_path: 输出路径
            bgm_volume: BGM 音量 0.0-1.0，默认 0.3

        Returns:
            输出文件路径
        """
        _, _, merge_fn = _load_ffmpeg_utils()
        if merge_fn is None:
            raise RuntimeError("ffmpeg_utils 未加载，无法混入 BGM")
        return merge_fn(
            video_path=video_path,
            bgm_path=bgm_path,
            output_path=output_path,
            bgm_volume=bgm_volume,
        )
