#!/usr/bin/env python3
"""
ph-videos BGM 生成脚本

根据 BGM 描述（来自 ph-videos-music-script）调用 Suno/CosyVoice 等 API 生成 BGM 音频。
支持 DeerFlow 沙箱内执行，输出供 ph-videos-video-generation --bgm-file 使用。

用法:
  python generate.py --description "轻柔钢琴，治愈系，中速" --output /path/to/bgm.mp3
  python generate.py --description-file /path/to/bgm_desc.txt --output /path/to/bgm.mp3 --duration 30

环境变量:
  SUNO_API_KEY: Suno API Key（若设置则调用 Suno）
  COSYVOICE_API_URL: CosyVoice API 地址（可选）
  COSYVOICE_API_KEY: CosyVoice API Key（可选）
"""

import argparse
import os
import sys
from pathlib import Path


def _get_description(args) -> str:
    """获取 BGM 描述"""
    if args.description:
        return args.description.strip()
    if args.description_file:
        path = Path(args.description_file)
        if path.exists():
            return path.read_text(encoding="utf-8").strip()
        raise FileNotFoundError(f"描述文件不存在: {args.description_file}")
    raise ValueError("请提供 --description 或 --description-file")


def _try_suno(description: str, output_path: str, duration: int) -> bool:
    """尝试调用 Suno API。返回是否成功。"""
    api_key = os.getenv("SUNO_API_KEY")
    if not api_key:
        return False
    try:
        import requests
        # Suno API 格式（常见第三方封装）
        # 实际 Suno 官方 API 可能不同，此处为可扩展占位
        url = os.getenv("SUNO_API_URL", "https://api.suno.ai/v1/generate")
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        payload = {"prompt": description, "duration": duration}
        r = requests.post(url, json=payload, headers=headers, timeout=120)
        if r.status_code == 200 and r.content:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(r.content)
            return True
    except Exception:
        pass
    return False


def _try_cosyvoice(description: str, output_path: str, duration: int) -> bool:
    """尝试调用 CosyVoice API。返回是否成功。"""
    url = os.getenv("COSYVOICE_API_URL")
    api_key = os.getenv("COSYVOICE_API_KEY")
    if not url:
        return False
    try:
        import requests
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
        headers["Content-Type"] = "application/json"
        payload = {"text": description, "duration_seconds": duration}
        r = requests.post(url, json=payload, headers=headers, timeout=120)
        if r.status_code == 200 and r.content:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(r.content)
            return True
    except Exception:
        pass
    return False


def _fallback_save_description(description: str, output_path: str) -> None:
    """无 API 时保存描述到 .txt，供用户手动生成"""
    base = str(Path(output_path).with_suffix(""))
    txt_path = base + "_bgm_prompt.txt"
    Path(txt_path).parent.mkdir(parents=True, exist_ok=True)
    Path(txt_path).write_text(description, encoding="utf-8")
    print(f"未配置 SUNO_API_KEY 或 COSYVOICE_API_URL。已保存 BGM 描述到: {txt_path}")
    print("请使用 CosyVoice 或 Suno 根据描述生成 BGM，或手动上传音频后使用 ph-videos-video-generation --bgm-file")


def main():
    parser = argparse.ArgumentParser(description="ph-videos BGM generation")
    parser.add_argument("--description", default=None, help="BGM description from ph-videos-music-script")
    parser.add_argument("--description-file", default=None, help="Path to file containing BGM description")
    parser.add_argument("--output", required=True, help="Output audio path (mp3/wav)")
    parser.add_argument("--duration", type=int, default=30, help="Target duration in seconds")
    args = parser.parse_args()

    description = _get_description(args)
    output_path = args.output
    duration = args.duration

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    # 优先 Suno，其次 CosyVoice
    if _try_suno(description, output_path, duration):
        print(f"BGM 已生成（Suno）: {output_path}")
        return
    if _try_cosyvoice(description, output_path, duration):
        print(f"BGM 已生成（CosyVoice）: {output_path}")
        return

    _fallback_save_description(description, output_path)


if __name__ == "__main__":
    main()
