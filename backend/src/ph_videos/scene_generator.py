"""镜头生成器：调用 generate.py，带质量评分与重试。"""

import asyncio
import logging
import os
import tempfile
from pathlib import Path

from src.ph_videos.budget import BudgetController, BudgetExceededError
from src.ph_videos.quality_scorer import QualityScorer

logger = logging.getLogger(__name__)

_BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
_GENERATE_SCRIPT = _BACKEND_DIR.parent / "skills" / "public" / "ph-videos-video-generation" / "scripts" / "generate.py"


def _build_env(api_keys: dict[str, str]) -> dict[str, str]:
    """根据 api_keys 构建子进程环境变量。"""
    env = os.environ.copy()
    if "volcano" in api_keys and api_keys["volcano"]:
        env["VOLCANO_API_KEY"] = api_keys["volcano"]
        env["ARK_API_KEY"] = api_keys["volcano"]
    if "dashscope" in api_keys and api_keys["dashscope"]:
        env["DASHSCOPE_API_KEY"] = api_keys["dashscope"]
    return env


async def _run_generate(
    provider: str,
    scene_prompt: str,
    output_path: str,
    api_keys: dict[str, str],
    video_style: str = "2D",
    aspect_ratio: str = "16:9",
) -> str:
    """调用 generate.py 生成单镜头视频。"""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8") as f:
        f.write(scene_prompt + "\n")
        script_path = f.name

    try:
        env = _build_env(api_keys)
        cmd = [
            "python",
            str(_GENERATE_SCRIPT),
            "--provider", provider,
            "--script-file", script_path,
            "--output", output_path,
            "--video-style", video_style,
            "--aspect-ratio", aspect_ratio,
        ]
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            env=env,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode != 0:
            raise RuntimeError(f"generate.py 失败: {stderr.decode('utf-8', errors='replace')}")
        return output_path
    finally:
        try:
            os.unlink(script_path)
        except OSError:
            pass


class SceneGenerator:
    """镜头生成器，带质量评分与重试。"""

    def __init__(
        self,
        scorer: QualityScorer,
        budget: BudgetController,
        max_retry: int = 2,
        threshold: float = 0.75,
    ) -> None:
        self.scorer = scorer
        self.budget = budget
        self.max_retry = max_retry
        self.threshold = threshold

    async def generate_with_retry(
        self,
        scene_prompt: str,
        model_name: str,
        api_keys: dict[str, str],
        output_path: str,
        video_style: str = "2D",
        aspect_ratio: str = "16:9",
    ) -> str:
        """
        生成镜头，不达标则重试（最多 max_retry 次）。

        Args:
            scene_prompt: 镜头描述
            model_name: volcano | wanxiang | comfyui
            api_keys: API 密钥
            output_path: 输出路径
            video_style: 视频风格
            aspect_ratio: 画幅

        Returns:
            生成的视频路径

        Raises:
            BudgetExceededError: 预算耗尽
            RuntimeError: 质量不达标达最大重试
        """
        last_error: Exception | None = None
        for attempt in range(self.max_retry + 1):
            if not self.budget.can_afford(model_name):
                raise BudgetExceededError("预算耗尽，无法继续生成镜头")

            self.budget.consume(model_name)

            try:
                video_path = await _run_generate(
                    provider=model_name,
                    scene_prompt=scene_prompt,
                    output_path=output_path,
                    api_keys=api_keys,
                    video_style=video_style,
                    aspect_ratio=aspect_ratio,
                )
                score = await self.scorer.score(video_path, scene_prompt)
                if score >= self.threshold:
                    return video_path
                last_error = RuntimeError(f"质量不达标: score={score:.2f}")
            except Exception as e:
                last_error = e

            logger.warning("SceneGenerator attempt %d failed: %s", attempt + 1, last_error)

        raise RuntimeError(f"镜头生成失败（已重试 {self.max_retry + 1} 次）: {last_error}")
