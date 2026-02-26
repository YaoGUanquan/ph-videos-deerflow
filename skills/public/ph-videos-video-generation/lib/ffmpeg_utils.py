"""
FFmpeg 路径解析（移植自 ph-videos-text）

优先级：
1. PH_VIDEOS_TEXT_PATH 指向 ph-videos-text 时，复用其 src.utils.ffmpeg_path
2. 本项目 ffmpeg/ 目录（ph-videos-deerflow 根目录或 skill 根目录）
3. imageio-ffmpeg（pip install 即用，含完整 DLL）
4. 系统 PATH 中的 ffmpeg
5. PH_VIDEOS_TEXT_PATH/ffmpeg/ 或 tools/ffmpeg/ 下的内置二进制
"""

import os
import platform
import shutil
import sys
from pathlib import Path

# 项目根目录：lib -> ph-videos-video-generation -> public -> skills -> ph-videos-deerflow
_SKILL_ROOT = Path(__file__).resolve().parent.parent
_DEERFLOW_ROOT = _SKILL_ROOT.parent.parent.parent
_FFMPEG_BASES = [_DEERFLOW_ROOT / "ffmpeg", _SKILL_ROOT / "ffmpeg"]


def _use_ph_videos_text_ffmpeg():
    """优先从 ph-videos-text 导入 ffmpeg 工具"""
    ph_path = os.getenv("PH_VIDEOS_TEXT_PATH")
    if ph_path and os.path.isdir(ph_path):
        if ph_path not in sys.path:
            sys.path.insert(0, ph_path)
        try:
            from src.utils.ffmpeg_path import get_ffmpeg_path, get_ffmpeg_run_env
            return get_ffmpeg_path, get_ffmpeg_run_env
        except ImportError:
            pass
    return None, None


def _platform_subdir() -> str:
    """当前平台子目录名"""
    system = platform.system().lower()
    if system == "windows":
        return "windows"
    if system == "linux":
        return "linux"
    if system == "darwin":
        return "darwin"
    return ""


def _find_ffmpeg_in_bases(bases: list[Path], system: str, subdir: str) -> str | None:
    """在指定目录列表中查找 ffmpeg"""
    for base in bases:
        if not base.exists():
            continue
        if subdir:
            platform_dir = base / subdir
            if system == "windows":
                candidates = [platform_dir / "ffmpeg.exe", platform_dir / "bin" / "ffmpeg.exe"]
            else:
                candidates = [platform_dir / "ffmpeg", platform_dir / "bin" / "ffmpeg"]
        else:
            candidates = []
        if system == "windows":
            candidates.extend([base / "ffmpeg.exe", base / "bin" / "ffmpeg.exe"])
        else:
            candidates.extend([base / "ffmpeg", base / "bin" / "ffmpeg"])
        for p in candidates:
            if p.exists() and (system == "windows" or os.access(p, os.X_OK)):
                return str(p)
    return None


def get_ffmpeg_path() -> str | None:
    """
    获取 ffmpeg 可执行文件路径

    优先级：
    1. ph-videos-text 的 ffmpeg_path（若 PH_VIDEOS_TEXT_PATH 已设置）
    2. 本项目 ffmpeg/ 目录（ph-videos-deerflow 或 skill 根目录）
    3. imageio-ffmpeg（pip 安装即用，含完整 DLL）
    4. 系统 PATH 中的 ffmpeg
    5. PH_VIDEOS_TEXT_PATH/ffmpeg/ 或 tools/ffmpeg/ 下的内置
    """
    fn, _ = _use_ph_videos_text_ffmpeg()
    if fn:
        return fn()

    system = platform.system().lower()
    subdir = _platform_subdir()

    # 2. 本项目 ffmpeg/ 目录
    path = _find_ffmpeg_in_bases(_FFMPEG_BASES, system, subdir)
    if path:
        return path

    # 3. imageio-ffmpeg
    try:
        import imageio_ffmpeg
        path = imageio_ffmpeg.get_ffmpeg_exe()
        if path and os.path.isfile(path):
            return path
    except ImportError:
        pass

    # 4. 系统 PATH
    path = shutil.which("ffmpeg")
    if path:
        return path

    # 5. PH_VIDEOS_TEXT_PATH 下的项目内置
    ph_path = os.getenv("PH_VIDEOS_TEXT_PATH")
    if ph_path:
        path = _find_ffmpeg_in_bases(
            [Path(ph_path) / "ffmpeg", Path(ph_path) / "tools" / "ffmpeg"],
            system, subdir,
        )
        if path:
            return path

    return None


def get_ffmpeg_run_env() -> dict | None:
    """
    获取运行 FFmpeg 时的环境变量（用于 subprocess）。
    Windows 上使用项目内置 FFmpeg 时，需将 ffmpeg 所在目录加入 PATH，否则会报 DLL 缺失。
    """
    _, env_fn = _use_ph_videos_text_ffmpeg()
    if env_fn:
        return env_fn()

    path = get_ffmpeg_path()
    if not path:
        return None
    ffmpeg_dir = os.path.dirname(os.path.abspath(path))
    current_path = os.environ.get("PATH", "")
    if ffmpeg_dir and ffmpeg_dir not in current_path.split(os.pathsep):
        env = os.environ.copy()
        env["PATH"] = ffmpeg_dir + os.pathsep + current_path
        return env
    return None


def is_ffmpeg_available() -> bool:
    """检查 ffmpeg 是否可用"""
    path = get_ffmpeg_path()
    if not path:
        return False
    try:
        import subprocess
        env = get_ffmpeg_run_env()
        r = subprocess.run(
            [path, "-version"],
            capture_output=True,
            timeout=5,
            env=env,
            stdin=subprocess.DEVNULL,
        )
        return r.returncode == 0
    except Exception:
        return False


def _video_has_audio(video_path: str) -> bool:
    """检查视频是否包含音轨"""
    import json
    import subprocess

    ffmpeg_path = get_ffmpeg_path()
    if not ffmpeg_path:
        return False
    ffprobe_dir = os.path.dirname(ffmpeg_path)
    ffprobe_name = "ffprobe.exe" if platform.system().lower() == "windows" else "ffprobe"
    ffprobe = os.path.join(ffprobe_dir, ffprobe_name)
    if not os.path.isfile(ffprobe):
        ffprobe = shutil.which("ffprobe") or ffprobe
    try:
        r = subprocess.run(
            [
                ffprobe,
                "-v", "quiet",
                "-print_format", "json",
                "-show_streams",
                "-select_streams", "a",
                video_path,
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
        if r.returncode != 0:
            return False
        data = json.loads(r.stdout)
        return bool(data.get("streams"))
    except Exception:
        return False


def merge_video_with_bgm(
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
    import subprocess

    ffmpeg_path = get_ffmpeg_path()
    if not ffmpeg_path:
        raise RuntimeError("未找到 FFmpeg，无法混入 BGM")
    env = get_ffmpeg_run_env() or {}
    run_env = os.environ.copy()
    run_env.update(env)

    has_audio = _video_has_audio(video_path)
    vol = max(0.0, min(1.0, bgm_volume))

    if has_audio:
        # 视频有音轨：amix 混音，BGM 使用 volume
        filter_complex = (
            f"[0:a]apad=whole_dur=0[va];[1:a]volume={vol}[bgm];"
            "[va][bgm]amix=inputs=2:duration=first:dropout_transition=2[a]"
        )
        cmd = [
            ffmpeg_path, "-y",
            "-i", video_path,
            "-i", bgm_path,
            "-filter_complex", filter_complex,
            "-map", "0:v",
            "-map", "[a]",
            "-c:v", "copy",
            "-shortest",
            output_path,
        ]
    else:
        # 视频无音轨：添加 BGM 为 sole 音轨
        filter_complex = (
            f"[1:a]volume={vol},apad=whole_dur=0[bgm];"
            "[0:v][bgm]concat=n=1:v=1:a=1[v][a]"
        )
        cmd = [
            ffmpeg_path, "-y",
            "-i", video_path,
            "-i", bgm_path,
            "-filter_complex", filter_complex,
            "-map", "[v]",
            "-map", "[a]",
            "-shortest",
            output_path,
        ]

    subprocess.run(cmd, check=True, capture_output=True, env=run_env, timeout=300)
    return output_path
