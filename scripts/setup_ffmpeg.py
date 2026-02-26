#!/usr/bin/env python3
"""
下载 FFmpeg 到项目 ffmpeg/ 目录（移植自 ph-videos-text）

按平台自动选择并下载：
- Linux: johnvansickle.com 静态构建
- Windows: gyan.dev essentials 构建

支持 --all 参数同时下载 Linux 和 Windows 版本（用于 CI 或跨平台打包）

用法:
  python scripts/setup_ffmpeg.py
  python scripts/setup_ffmpeg.py --all
"""

import argparse
import os
import platform
import shutil
import stat
import sys
import tarfile
import zipfile
from pathlib import Path

FFMPEG_URLS = {
    "linux": "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz",
    "windows": "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip",
}

# 项目根目录（ph-videos-deerflow）
PROJECT_ROOT = Path(__file__).resolve().parent.parent
FFMPEG_BASE = PROJECT_ROOT / "ffmpeg"


def download_file(url: str, dest: Path) -> bool:
    """下载文件"""
    try:
        import urllib.request

        print(f"下载: {url}")
        urllib.request.urlretrieve(url, dest)
        return True
    except Exception as e:
        print(f"下载失败: {e}")
        return False


def setup_linux(target_dir: Path) -> bool:
    """Linux: 下载 tar.xz 并解压到 target_dir"""
    url = FFMPEG_URLS["linux"]
    archive = target_dir.parent / "ffmpeg-linux.tar.xz"
    target_dir.mkdir(parents=True, exist_ok=True)

    if not download_file(url, archive):
        return False

    print("解压 Linux 版本...")
    with tarfile.open(archive, "r:xz") as tf:
        extract_dir = target_dir.parent / "_extract_linux"
        extract_dir.mkdir(exist_ok=True)
        tf.extractall(extract_dir)

        for item in extract_dir.iterdir():
            if item.is_dir():
                src_ffmpeg = item / "ffmpeg"
                src_ffprobe = item / "ffprobe"
                if src_ffmpeg.exists():
                    shutil.copy2(src_ffmpeg, target_dir / "ffmpeg")
                    if src_ffprobe.exists():
                        shutil.copy2(src_ffprobe, target_dir / "ffprobe")
                    break

        shutil.rmtree(extract_dir, ignore_errors=True)

    archive.unlink(missing_ok=True)
    for name in ["ffmpeg", "ffprobe"]:
        p = target_dir / name
        if p.exists():
            p.chmod(p.stat().st_mode | stat.S_IEXEC)
    return True


def setup_windows(target_dir: Path) -> bool:
    """Windows: 下载 zip 并解压到 target_dir"""
    url = FFMPEG_URLS["windows"]
    archive = target_dir.parent / "ffmpeg-windows.zip"
    target_dir.mkdir(parents=True, exist_ok=True)

    if not download_file(url, archive):
        return False

    print("解压 Windows 版本...")
    with zipfile.ZipFile(archive, "r") as zf:
        extract_dir = target_dir.parent / "_extract_win"
        extract_dir.mkdir(exist_ok=True)
        zf.extractall(extract_dir)

        for root, _, files in os.walk(extract_dir):
            for f in files:
                if f == "ffmpeg.exe":
                    shutil.copy2(Path(root) / f, target_dir / "ffmpeg.exe")
                elif f == "ffprobe.exe":
                    shutil.copy2(Path(root) / f, target_dir / "ffprobe.exe")

        shutil.rmtree(extract_dir, ignore_errors=True)

    archive.unlink(missing_ok=True)
    return True


def main():
    parser = argparse.ArgumentParser(description="下载 FFmpeg 到项目 ffmpeg/ 目录")
    parser.add_argument(
        "--all",
        action="store_true",
        help="同时下载 Linux 和 Windows 版本（用于 CI 或跨平台打包）",
    )
    args = parser.parse_args()

    system = platform.system().lower()
    if args.all:
        platforms = ["linux", "windows"]
        print("将下载 Linux 和 Windows 版本...")
    else:
        if system == "linux":
            platforms = ["linux"]
        elif system == "windows":
            platforms = ["windows"]
        else:
            print(f"暂不支持 {system}，请使用 --all 或手动安装")
            sys.exit(1)

    FFMPEG_BASE.mkdir(parents=True, exist_ok=True)
    ok = True
    for plat in platforms:
        target = FFMPEG_BASE / plat
        print(f"\n=== 处理 {plat} ===")
        if plat == "linux":
            ok = setup_linux(target) and ok
        else:
            ok = setup_windows(target) and ok

    if ok:
        print(f"\nFFmpeg 已安装到: {FFMPEG_BASE}")
        print("目录结构: ffmpeg/linux/ 或 ffmpeg/windows/")
        print("可运行: ffmpeg -version 验证")
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
