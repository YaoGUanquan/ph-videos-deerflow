"""
通义万相视频生成（对接 ph-videos-text 或内置实现）
"""
import os
import time
import requests
from typing import Optional, Callable, List

DEFAULT_BASE = "https://dashscope.aliyuncs.com"
VIDEO_PATH = "/api/v1/services/aigc/video-generation/video-synthesis"
TASKS_PATH = "/api/v1/tasks"

_PH_VIDEOS_PATH = os.getenv("PH_VIDEOS_TEXT_PATH")


def _use_ph_videos_text():
    if _PH_VIDEOS_PATH and os.path.isdir(_PH_VIDEOS_PATH):
        import sys
        if _PH_VIDEOS_PATH not in sys.path:
            sys.path.insert(0, _PH_VIDEOS_PATH)
        try:
            from src.services.video.wanxiang_video_client import (
                generate_video,
                generate_video_t2v,
                generate_t2v_and_download,
            )
            return True, (generate_video, generate_video_t2v, generate_t2v_and_download)
        except ImportError:
            pass
    return False, None


def _poll_wanxiang(base: str, task_id: str, api_key: str, cancel_check, poll_interval: float, poll_timeout: float) -> str:
    start = time.time()
    while True:
        if cancel_check and cancel_check():
            raise RuntimeError("用户取消任务")
        if time.time() - start > poll_timeout:
            raise TimeoutError(f"通义万相任务超时: {task_id}")
        r = requests.get(
            f"{base}{TASKS_PATH}/{task_id}",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=30,
        )
        r.raise_for_status()
        data = r.json()
        output = data.get("output", {})
        status = output.get("task_status") or data.get("status")
        if status == "SUCCEEDED":
            url = output.get("video_url") or output.get("url")
            if not url and output.get("results"):
                url = output["results"][0].get("url") or output["results"][0].get("video_url")
            if url:
                return url
            raise ValueError(f"任务成功但无视频 URL: {data}")
        elif status == "FAILED":
            raise RuntimeError(output.get("message") or data.get("message", str(data)))
        time.sleep(poll_interval)


def generate_video_t2v(
    prompt: str,
    api_key: str,
    base_url: str = None,
    model_id: str = None,
    duration: int = 5,
    size: str = "1280*720",
    cancel_check: Optional[Callable[[], bool]] = None,
    poll_interval: float = 5.0,
    poll_timeout: float = 600.0,
) -> str:
    """文生视频"""
    ok, tup = _use_ph_videos_text()
    if ok and tup:
        return tup[1](
            prompt=prompt,
            api_key=api_key,
            base_url=base_url,
            model_id=model_id,
            duration=duration,
            size=size,
            cancel_check=cancel_check,
            poll_interval=poll_interval,
            poll_timeout=poll_timeout,
        )
    base = (base_url or DEFAULT_BASE).rstrip("/")
    model = model_id or "wan2.6-t2v"
    payload = {
        "model": model,
        "input": {"prompt": prompt},
        "parameters": {"size": size, "duration": duration, "prompt_extend": True, "watermark": True},
    }
    r = requests.post(
        base + VIDEO_PATH,
        json=payload,
        headers={"X-DashScope-Async": "enable", "Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        timeout=60,
    )
    r.raise_for_status()
    data = r.json()
    task_id = data.get("output", {}).get("task_id") or data.get("task_id")
    if not task_id:
        raise RuntimeError(f"未返回 task_id: {data}")
    return _poll_wanxiang(base, task_id, api_key, cancel_check, poll_interval, poll_timeout)


def generate_video(
    prompt: str,
    api_key: str,
    img_url: str,
    base_url: str = None,
    model_id: str = None,
    duration: int = 5,
    resolution: str = "720P",
    cancel_check: Optional[Callable[[], bool]] = None,
    poll_interval: float = 5.0,
    poll_timeout: float = 600.0,
) -> str:
    """图生视频"""
    ok, tup = _use_ph_videos_text()
    if ok and tup:
        return tup[0](
            prompt=prompt,
            api_key=api_key,
            img_url=img_url,
            base_url=base_url,
            model_id=model_id,
            duration=duration,
            resolution=resolution,
            cancel_check=cancel_check,
            poll_interval=poll_interval,
            poll_timeout=poll_timeout,
        )
    base = (base_url or DEFAULT_BASE).rstrip("/")
    model = model_id or "wan2.6-i2v-flash"
    res = resolution.upper() if resolution else "720P"
    if "P" not in res and res.isdigit():
        res = res + "P"
    payload = {
        "model": model,
        "input": {"prompt": prompt, "img_url": img_url},
        "parameters": {"resolution": res, "duration": duration, "prompt_extend": True, "watermark": True},
    }
    r = requests.post(
        base + VIDEO_PATH,
        json=payload,
        headers={"X-DashScope-Async": "enable", "Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        timeout=60,
    )
    r.raise_for_status()
    data = r.json()
    task_id = data.get("output", {}).get("task_id") or data.get("task_id")
    if not task_id:
        raise RuntimeError(f"未返回 task_id: {data}")
    return _poll_wanxiang(base, task_id, api_key, cancel_check, poll_interval, poll_timeout)


def generate_t2v_and_download(prompt: str, save_path: str, api_key: str, **kwargs) -> str:
    """文生视频并下载"""
    cancel_check = kwargs.pop("cancel_check", None)
    url = generate_video_t2v(prompt=prompt, api_key=api_key, cancel_check=cancel_check, **kwargs)
    os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
    resp = requests.get(url, stream=True, timeout=300)
    resp.raise_for_status()
    with open(save_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    return save_path
