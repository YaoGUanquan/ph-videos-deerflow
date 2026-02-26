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
