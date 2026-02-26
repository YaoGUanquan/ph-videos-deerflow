"""
ComfyUI 视频生成（对接 ph-videos-text 或内置实现）
"""
import os
import asyncio
from typing import Optional, Callable

_PH_VIDEOS_PATH = os.getenv("PH_VIDEOS_TEXT_PATH")


def _use_ph_videos_text():
    if _PH_VIDEOS_PATH and os.path.isdir(_PH_VIDEOS_PATH):
        import sys
        if _PH_VIDEOS_PATH not in sys.path:
            sys.path.insert(0, _PH_VIDEOS_PATH)
        try:
            from src.services.video.comfyui_video_client import generate_video_segment
            return generate_video_segment
        except ImportError:
            pass
    return None


async def generate_video_segment(
    prompt: str,
    save_path: str,
    mode: str = "local",
    comfyui_url: str = "http://127.0.0.1:8188",
    workflow_path: Optional[str] = None,
    width: int = 512,
    height: int = 288,
    cancel_check: Optional[Callable[[], bool]] = None,
    poll_timeout: int = 600,
    **kwargs,
) -> str:
    """使用 ComfyUI 生成单段视频"""
    fn = _use_ph_videos_text()
    if fn:
        return await fn(
            prompt=prompt,
            save_path=save_path,
            mode=mode,
            comfyui_url=comfyui_url,
            workflow_path=workflow_path,
            width=width,
            height=height,
            cancel_check=cancel_check,
            poll_timeout=poll_timeout,
            **kwargs,
        )
    try:
        from comfykit import ComfyKit
    except ImportError:
        raise ImportError(
            "请安装 comfykit: pip install comfykit "
            "或设置 PH_VIDEOS_TEXT_PATH 指向 ph-videos-text 项目"
        )
    # 工作流路径：PH_VIDEOS_TEXT_PATH 或当前技能目录的 workflows
    ph_path = os.getenv("PH_VIDEOS_TEXT_PATH")
    if ph_path:
        default_workflow = os.path.join(ph_path, "workflows", "comfyui", "video_wan2.1_fusionx.json")
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        default_workflow = os.path.join(script_dir, "..", "..", "..", "..", "workflows", "comfyui", "video_wan2.1_fusionx.json")
    workflow = workflow_path or default_workflow
    if not os.path.isfile(workflow):
        raise FileNotFoundError(f"工作流不存在: {workflow}")
    kit = ComfyKit(comfyui_url=(comfyui_url or "").strip() or "http://127.0.0.1:8188")
    result = await kit.execute(workflow, {"prompt": prompt, "width": width, "height": height})
    if result.status != "completed":
        raise RuntimeError(result.msg or "ComfyUI 执行失败")
    if not result.videos:
        raise RuntimeError("未生成视频")
    import requests
    video_url = result.videos[0]
    if video_url.startswith("/"):
        video_url = f"{comfyui_url.rstrip('/')}{video_url}"
    elif not video_url.startswith("http"):
        video_url = f"{comfyui_url.rstrip('/')}/{video_url.lstrip('/')}"
    os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
    content = await asyncio.to_thread(lambda: requests.get(video_url, timeout=120).content)
    with open(save_path, "wb") as f:
        f.write(content)
    return save_path
