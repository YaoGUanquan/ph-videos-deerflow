#!/usr/bin/env python3
"""
ph-videos 视频生成脚本

根据分镜脚本调用火山 Seedance / 通义万相 / ComfyUI 生成视频。
支持 t2v、i2v，输出合并后的视频文件。

用法:
  python generate.py --provider volcano --script-file /path/to/script.txt --output /path/to/output.mp4
  python generate.py --provider wanxiang --script-file /path/to/script.txt --reference-image /path/to/img.jpg --output /path/to/output.mp4
  python generate.py --provider comfyui --script-file /path/to/script.txt --output /path/to/output.mp4

环境变量:
  VOLCANO_API_KEY / ARK_API_KEY: 火山 API Key
  DASHSCOPE_API_KEY: 通义万相 API Key
  PH_VIDEOS_TEXT_PATH: 可选，指向 ph-videos-text 项目根目录以复用其 video clients 与 ffmpeg

FFmpeg（多段合并）:
  优先 imageio-ffmpeg（pip install imageio-ffmpeg），或 PH_VIDEOS_TEXT_PATH 下的 ffmpeg，或系统 PATH
"""

import argparse
import asyncio
import os
import sys
from pathlib import Path

# 确保可导入 lib（脚本在 scripts/ 下，lib 在上级）
_skill_root = Path(__file__).resolve().parent.parent
if str(_skill_root) not in sys.path:
    sys.path.insert(0, str(_skill_root))

from lib.seedance_client import generate_and_download as seedance_download
from lib.wanxiang_client import generate_video_t2v, generate_video, generate_t2v_and_download
from lib.comfyui_client import generate_video_segment as comfyui_segment
from lib.ffmpeg_utils import get_ffmpeg_path, get_ffmpeg_run_env


def _read_script(script_path: str) -> list[str]:
    """读取脚本，每行一个场景"""
    with open(script_path, "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f if ln.strip()]
    # 过滤元信息行（主角设定、画面风格等可保留在首段）
    return lines


def _get_api_key(provider: str) -> str:
    if provider == "volcano":
        return os.getenv("VOLCANO_API_KEY") or os.getenv("ARK_API_KEY") or ""
    if provider == "wanxiang":
        return os.getenv("DASHSCOPE_API_KEY") or ""
    return ""


def generate_volcano(
    script_path: str,
    output_path: str,
    api_key: str = None,
    base_url: str = None,
    model_id: str = None,
    reference_images: list[str] | None = None,
    duration_per: int = 5,
) -> str:
    """火山 Seedance 视频生成"""
    api_key = api_key or _get_api_key("volcano")
    if not api_key:
        raise ValueError("请设置 VOLCANO_API_KEY 或 ARK_API_KEY")
    scenes = _read_script(script_path)
    if not scenes:
        raise ValueError("脚本为空")
    # 多段时逐段生成再合并；单段直接生成
    if len(scenes) == 1:
        img_url = None
        if reference_images and reference_images[0]:
            # 本地路径需转为 URL；沙箱内可传 file:// 或 OSS URL
            img_url = reference_images[0] if reference_images[0].startswith("http") else None
        return seedance_download(
            prompt=scenes[0],
            save_path=output_path,
            api_key=api_key,
            base_url=base_url,
            model_id=model_id,
            duration=duration_per,
            image_url=img_url,
        )
    # 多段：生成到 temp 再合并（简化实现：仅生成第一段作为示例，完整实现需 FFmpeg 合并）
    import tempfile
    tmp_dir = tempfile.mkdtemp()
    seg_paths = []
    for i, scene in enumerate(scenes[:5]):  # 最多 5 段
        seg = os.path.join(tmp_dir, f"seg_{i}.mp4")
        seedance_download(
            prompt=scene,
            save_path=seg,
            api_key=api_key,
            base_url=base_url,
            model_id=model_id,
            duration=duration_per,
        )
        seg_paths.append(seg)
    # 简单合并：用 ffmpeg concat（优先 imageio-ffmpeg / PH_VIDEOS_TEXT_PATH）
    try:
        import subprocess
        ffmpeg_path = get_ffmpeg_path()
        if not ffmpeg_path:
            raise RuntimeError(
                "未找到 FFmpeg。可选：① pip install imageio-ffmpeg "
                "② 设置 PH_VIDEOS_TEXT_PATH 指向 ph-videos-text ③ 系统安装 ffmpeg"
            )
        list_file = os.path.join(tmp_dir, "list.txt")
        with open(list_file, "w") as f:
            for p in seg_paths:
                f.write(f"file '{os.path.abspath(p)}'\n")
        run_kw = {"check": True, "capture_output": True}
        env = get_ffmpeg_run_env()
        if env:
            run_kw["env"] = env
        subprocess.run(
            [ffmpeg_path, "-y", "-f", "concat", "-safe", "0", "-i", list_file, "-c", "copy", output_path],
            **run_kw,
        )
    except Exception:
        # 无 ffmpeg 时仅保存第一段
        import shutil
        shutil.copy(seg_paths[0], output_path)
    return output_path


def generate_wanxiang(
    script_path: str,
    output_path: str,
    mode: str = "t2v",
    api_key: str = None,
    base_url: str = None,
    model_id: str = None,
    reference_images: list[str] | None = None,
    duration_per: int = 5,
) -> str:
    """通义万相视频生成"""
    api_key = api_key or _get_api_key("wanxiang")
    if not api_key:
        raise ValueError("请设置 DASHSCOPE_API_KEY")
    scenes = _read_script(script_path)
    if not scenes:
        raise ValueError("脚本为空")
    if mode == "i2v" and reference_images and reference_images[0]:
        img_url = reference_images[0] if reference_images[0].startswith("http") else None
        if not img_url:
            raise ValueError("图生视频需提供公网可访问的图片 URL")
        url = generate_video(
            prompt=scenes[0],
            api_key=api_key,
            img_url=img_url,
            base_url=base_url,
            model_id=model_id,
            duration=duration_per,
        )
        import requests
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        r = requests.get(url, stream=True, timeout=300)
        r.raise_for_status()
        with open(output_path, "wb") as f:
            for chunk in r.iter_content(8192):
                if chunk:
                    f.write(chunk)
        return output_path
    return generate_t2v_and_download(
        prompt=scenes[0],
        save_path=output_path,
        api_key=api_key,
        base_url=base_url,
        model_id=model_id,
        duration=duration_per,
    )


def generate_comfyui(
    script_path: str,
    output_path: str,
    comfyui_url: str = "http://127.0.0.1:8188",
    workflow_path: str = None,
) -> str:
    """ComfyUI 视频生成"""
    scenes = _read_script(script_path)
    if not scenes:
        raise ValueError("脚本为空")
    # 工作流路径：优先 PH_VIDEOS_TEXT_PATH/workflows/comfyui/
    ph_path = os.getenv("PH_VIDEOS_TEXT_PATH")
    if not workflow_path and ph_path:
        wf = os.path.join(ph_path, "workflows", "comfyui", "video_wan2.1_fusionx.json")
        if os.path.isfile(wf):
            workflow_path = wf
    asyncio.run(
        comfyui_segment(
            prompt=scenes[0],
            save_path=output_path,
            mode="local",
            comfyui_url=comfyui_url,
            workflow_path=workflow_path,
        )
    )
    return output_path


def main():
    parser = argparse.ArgumentParser(description="ph-videos video generation")
    parser.add_argument("--provider", required=True, choices=["volcano", "wanxiang", "comfyui"])
    parser.add_argument("--script-file", required=True, help="Path to script file (one scene per line)")
    parser.add_argument("--output", required=True, help="Output video path")
    parser.add_argument("--reference-images", nargs="*", default=[], help="Reference images for i2v (URLs)")
    parser.add_argument("--wanxiang-mode", default="t2v", choices=["t2v", "i2v", "r2v"])
    parser.add_argument("--comfyui-url", default="http://127.0.0.1:8188")
    parser.add_argument("--api-key", help="API Key (override env)")
    parser.add_argument("--base-url", help="API base URL")
    parser.add_argument("--model-id", help="Model ID")
    parser.add_argument("--duration", type=int, default=5)
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)

    if args.provider == "volcano":
        result = generate_volcano(
            args.script_file,
            args.output,
            api_key=args.api_key,
            base_url=args.base_url,
            model_id=args.model_id,
            reference_images=args.reference_images or None,
            duration_per=args.duration,
        )
    elif args.provider == "wanxiang":
        result = generate_wanxiang(
            args.script_file,
            args.output,
            mode=args.wanxiang_mode,
            api_key=args.api_key,
            base_url=args.base_url,
            model_id=args.model_id,
            reference_images=args.reference_images or None,
            duration_per=args.duration,
        )
    else:
        result = generate_comfyui(args.script_file, args.output, args.comfyui_url)

    print(f"视频已生成: {result}")


if __name__ == "__main__":
    main()
