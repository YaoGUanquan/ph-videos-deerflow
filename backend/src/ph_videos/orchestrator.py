"""视频生成编排器，串联各模块。"""

import logging
import os
from pathlib import Path

from src.ph_videos.budget import BudgetController, BudgetExceededError
from src.ph_videos.ffmpeg_pipeline import FFmpegPipeline
from src.ph_videos.model_router import ModelRouter
from src.ph_videos.models import (
    TASK_STATUS_COMPLETED,
    TASK_STATUS_FAILED,
    TASK_STATUS_GENERATING_AUDIO,
    TASK_STATUS_GENERATING_SCENES,
    TASK_STATUS_RENDERING,
    TASK_STATUS_SCRIPTING,
    VideoTask,
)
from src.ph_videos.quality_scorer import QualityScorer
from src.ph_videos.scene_generator import SceneGenerator
from src.ph_videos.script_generator import ScriptGenerator
from src.ph_videos.task_manager import TaskManager

logger = logging.getLogger(__name__)


def _get_output_base() -> Path:
    """获取输出根目录。"""
    base = os.getenv("PH_VIDEOS_OUTPUT_BASE", "output")
    return Path(base).resolve()


def _get_task_output_dir(task_id: str) -> Path:
    """获取任务输出目录。"""
    return _get_output_base() / task_id


class VideoOrchestrator:
    """视频生成编排器。"""

    def __init__(self, task_manager: TaskManager) -> None:
        self.task_manager = task_manager

    async def run(self, task: VideoTask) -> None:
        """
        执行完整视频生成流程。

        流程：scripting → generating_scenes → generating_audio → rendering → completed | failed
        暂不考虑旁白，generating_audio 跳过。
        """
        task_id = task.task_id
        output_dir = _get_task_output_dir(task_id)
        output_dir.mkdir(parents=True, exist_ok=True)
        scenes_dir = output_dir / "scenes"
        scenes_dir.mkdir(parents=True, exist_ok=True)

        try:
            budget = BudgetController(task.budget)

            # 1. Scripting
            await self.task_manager.update_status(task_id, TASK_STATUS_SCRIPTING)
            script_gen = ScriptGenerator(
                api_key=task.api_keys.get("llm") or task.api_keys.get("openai"),
            )
            script = await script_gen.generate(task.topic, budget)
            task.script = script
            task.progress["scenes_count"] = len(script.get("scenes", []))

            # 2. Generating scenes
            await self.task_manager.update_status(task_id, TASK_STATUS_GENERATING_SCENES)
            scorer = QualityScorer()
            scene_gen = SceneGenerator(scorer=scorer, budget=budget)
            router = ModelRouter()

            video_paths: list[str] = []
            scenes = script.get("scenes", [])
            video_style = script.get("video_style", "2D")
            aspect_ratio = script.get("aspect_ratio", "16:9")

            for i, scene_prompt in enumerate(scenes):
                if isinstance(scene_prompt, dict):
                    scene_prompt = scene_prompt.get("prompt", str(scene_prompt))
                model = router.select_model({"prompt": scene_prompt}, budget)
                seg_path = str(scenes_dir / f"seg_{i}.mp4")
                video_path = await scene_gen.generate_with_retry(
                    scene_prompt=scene_prompt,
                    model_name=model,
                    api_keys=task.api_keys,
                    output_path=seg_path,
                    video_style=video_style,
                    aspect_ratio=aspect_ratio,
                )
                video_paths.append(video_path)
                task.progress["scenes_done"] = len(video_paths)

            task.scene_paths = video_paths

            # 3. Generating audio - 暂不实现旁白，跳过
            await self.task_manager.update_status(task_id, TASK_STATUS_GENERATING_AUDIO)
            # 无 BGM 时直接合并视频

            # 4. Rendering
            await self.task_manager.update_status(task_id, TASK_STATUS_RENDERING)
            pipeline = FFmpegPipeline()
            if not pipeline.is_available():
                raise RuntimeError("FFmpeg 不可用，无法合并视频")

            merged_path = str(output_dir / "merged.mp4")
            pipeline.concat_videos(video_paths, merged_path)

            final_path = str(output_dir / "final.mp4")
            # 若有 BGM 可在此调用 pipeline.add_bgm(merged_path, bgm_path, final_path)
            # 暂无 BGM，直接复制
            import shutil
            shutil.copy(merged_path, final_path)

            await self.task_manager.update_status(
                task_id,
                TASK_STATUS_COMPLETED,
                result_path=final_path,
            )
            task.result_path = final_path
            logger.info("ph-videos task %s completed: %s", task_id, final_path)

        except BudgetExceededError as e:
            logger.warning("ph-videos task %s budget exceeded: %s", task_id, e)
            await self.task_manager.update_status(
                task_id,
                TASK_STATUS_FAILED,
                error=f"budget_exhausted: {e}",
            )
        except Exception as e:
            logger.exception("ph-videos task %s failed: %s", task_id, e)
            await self.task_manager.update_status(
                task_id,
                TASK_STATUS_FAILED,
                error=str(e),
            )
