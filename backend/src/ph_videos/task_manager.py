"""内存任务队列，纯内存，重启后任务视为失败。"""

import asyncio
import logging
from typing import Callable

from src.ph_videos.models import VideoTask

logger = logging.getLogger(__name__)


class TaskManager:
    """内存任务管理器。"""

    def __init__(self) -> None:
        self._tasks: dict[str, VideoTask] = {}
        self._lock = asyncio.Lock()

    async def create(self, task: VideoTask) -> str:
        """创建任务并返回 task_id。"""
        async with self._lock:
            self._tasks[task.task_id] = task
            logger.info("ph-videos task created: %s", task.task_id)
            return task.task_id

    async def get(self, task_id: str) -> VideoTask | None:
        """获取任务。"""
        async with self._lock:
            return self._tasks.get(task_id)

    async def update_status(
        self,
        task_id: str,
        status: str,
        error: str = "",
        result_path: str = "",
        **kwargs: object,
    ) -> bool:
        """更新任务状态。"""
        async with self._lock:
            task = self._tasks.get(task_id)
            if not task:
                return False
            task.status = status
            if error:
                task.error = error
            if result_path:
                task.result_path = result_path
            for k, v in kwargs.items():
                if hasattr(task, k):
                    setattr(task, k, v)
            return True

    async def list_tasks(self) -> list[dict]:
        """列出所有任务（对外格式，不含 api_keys）。"""
        async with self._lock:
            return [t.to_public_dict() for t in self._tasks.values()]

    def run_background(
        self,
        task_id: str,
        coro_fn: Callable[[VideoTask], object],
    ) -> None:
        """
        在后台运行任务。任务失败时自动更新状态为 failed。

        Args:
            task_id: 任务 ID
            coro_fn: 异步协程函数，接收 VideoTask，执行编排逻辑
        """
        async def _run() -> None:
            task = await self.get(task_id)
            if not task:
                logger.error("ph-videos task not found: %s", task_id)
                return
            try:
                await coro_fn(task)
            except Exception as e:
                logger.exception("ph-videos task %s failed: %s", task_id, e)
                await self.update_status(
                    task_id,
                    "failed",
                    error=str(e),
                )

        asyncio.create_task(_run())
