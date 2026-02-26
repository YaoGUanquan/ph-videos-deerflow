"""
火山 Seedance 视频生成（对接 ph-videos-text 或内置实现）
"""
import os
import time
from typing import Optional, Callable

# 优先从 ph-videos-text 导入
_PH_VIDEOS_PATH = os.getenv("PH_VIDEOS_TEXT_PATH")


def _use_ph_videos_text():
    if _PH_VIDEOS_PATH and os.path.isdir(_PH_VIDEOS_PATH):
        import sys
        if _PH_VIDEOS_PATH not in sys.path:
            sys.path.insert(0, _PH_VIDEOS_PATH)
        try:
            from src.services.video.seedance_video_client import generate_video, generate_and_download
            return generate_video, generate_and_download
        except ImportError:
            pass
    return None, None


def generate_video(
    prompt: str,
    api_key: str,
    base_url: str = None,
    model_id: str = None,
    duration: int = 5,
    image_url: Optional[str] = None,
    **kwargs,
) -> str:
    """生成视频，返回 URL"""
    fn, _ = _use_ph_videos_text()
    if fn:
        return fn(
            prompt=prompt,
            api_key=api_key,
            base_url=base_url,
            model_id=model_id,
            duration=duration,
            image_url=image_url,
            **kwargs,
        )
    # 内置实现：需 volcengine-python-sdk[ark]
    try:
        from volcenginesdkarkruntime import Ark
    except ImportError:
        raise ImportError(
            "请安装 volcengine-python-sdk[ark]: pip install 'volcengine-python-sdk[ark]' "
            "或设置 PH_VIDEOS_TEXT_PATH 指向 ph-videos-text 项目"
        )
    client = Ark(
        base_url=base_url or "https://ark.cn-beijing.volces.com/api/v3",
        api_key=api_key,
    )
    model = model_id or "doubao-seedance-1-5-pro-251215"
    content = [{"type": "text", "text": f"{prompt} --duration {duration} --camerafixed false --watermark true"}]
    if image_url:
        content.append({"type": "image_url", "image_url": {"url": image_url}})
    create_result = client.content_generation.tasks.create(model=model, content=content)
    task_id = create_result.id
    poll_interval = kwargs.get("poll_interval", 3.0)
    poll_timeout = kwargs.get("poll_timeout", 300.0)
    cancel_check = kwargs.get("cancel_check")
    start = time.time()
    while True:
        if cancel_check and cancel_check():
            raise RuntimeError("用户取消任务")
        if time.time() - start > poll_timeout:
            raise TimeoutError(f"Seedance 任务超时: {task_id}")
        r = client.content_generation.tasks.get(task_id=task_id)
        if r.status == "succeeded":
            c = getattr(r, "content", None)
            if c and hasattr(c, "url"):
                return c.url
            if isinstance(c, dict) and c.get("url"):
                return c["url"]
        elif r.status == "failed":
            raise RuntimeError(getattr(r, "error", str(r)))
        time.sleep(poll_interval)


def generate_and_download(
    prompt: str,
    save_path: str,
    api_key: str,
    base_url: str = None,
    model_id: str = None,
    duration: int = 5,
    image_url: Optional[str] = None,
    **kwargs,
) -> str:
    """生成并下载到本地"""
    import requests
    fn, fn_dl = _use_ph_videos_text()
    if fn_dl:
        return fn_dl(
            prompt=prompt,
            save_path=save_path,
            api_key=api_key,
            base_url=base_url,
            model_id=model_id,
            duration=duration,
            image_url=image_url,
            **kwargs,
        )
    url = generate_video(
        prompt=prompt,
        api_key=api_key,
        base_url=base_url,
        model_id=model_id,
        duration=duration,
        image_url=image_url,
        **kwargs,
    )
    os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
    resp = requests.get(url, stream=True, timeout=300)
    resp.raise_for_status()
    with open(save_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    return save_path
