"""ph-videos 数据模型。"""

from dataclasses import dataclass, field
from typing import Any

import uuid


# 任务状态：与对外暴露一致
TASK_STATUS_PENDING = "pending"
TASK_STATUS_SCRIPTING = "scripting"
TASK_STATUS_GENERATING_SCENES = "generating_scenes"
TASK_STATUS_GENERATING_AUDIO = "generating_audio"
TASK_STATUS_RENDERING = "rendering"
TASK_STATUS_COMPLETED = "completed"
TASK_STATUS_FAILED = "failed"


@dataclass
class VideoTask:
    """视频生成任务。"""

    topic: str
    api_keys: dict[str, str]
    budget: float
    task_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    status: str = TASK_STATUS_PENDING
    result_path: str = ""
    error: str = ""
    script: dict[str, Any] | None = None
    scene_paths: list[str] = field(default_factory=list)
    progress: dict[str, Any] = field(default_factory=dict)

    def to_public_dict(self) -> dict[str, Any]:
        """转为对外暴露的字典（不含 api_keys）。"""
        return {
            "task_id": self.task_id,
            "topic": self.topic,
            "status": self.status,
            "result_path": self.result_path,
            "error": self.error,
            "progress": self.progress,
        }
