"""ph-videos 视频生成 API 路由。"""

import logging
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from src.ph_videos.models import VideoTask
from src.ph_videos.orchestrator import VideoOrchestrator
from src.ph_videos.task_manager import TaskManager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/ph-videos", tags=["ph-videos"])

# 单例 TaskManager（内存）
_task_manager: TaskManager | None = None


def get_task_manager() -> TaskManager:
    global _task_manager
    if _task_manager is None:
        _task_manager = TaskManager()
    return _task_manager


class GenerateRequest(BaseModel):
    """视频生成请求。"""

    topic: str = Field(..., description="视频主题")
    api_keys: dict[str, str] = Field(
        default_factory=dict,
        description="API 密钥，不持久化。支持: llm/openai, volcano, dashscope",
    )
    budget: float = Field(default=10.0, ge=0.1, description="预算上限")


class GenerateResponse(BaseModel):
    """视频生成响应。"""

    task_id: str = Field(..., description="任务 ID")
    status: str = Field(..., description="任务状态")


class TaskResponse(BaseModel):
    """任务状态响应。"""

    task_id: str
    topic: str
    status: str
    result_path: str = ""
    error: str = ""
    progress: dict[str, Any] = Field(default_factory=dict)


@router.post("/generate", response_model=GenerateResponse)
async def create_generate_task(request: GenerateRequest) -> GenerateResponse:
    """
    创建视频生成任务，异步执行。

    API keys 仅用于本次任务，不持久化。
    """
    task = VideoTask(
        topic=request.topic,
        api_keys=request.api_keys,
        budget=request.budget,
    )
    manager = get_task_manager()
    await manager.create(task)

    orchestrator = VideoOrchestrator(manager)
    manager.run_background(task.task_id, orchestrator.run)

    return GenerateResponse(task_id=task.task_id, status=task.status)


@router.get("/tasks")
async def list_tasks() -> dict[str, list]:
    """列出所有任务。"""
    manager = get_task_manager()
    tasks = await manager.list_tasks()
    return {"tasks": tasks}


@router.get("/tasks/{task_id}/download")
async def download_result(task_id: str) -> FileResponse:
    """下载任务生成的视频。"""
    manager = get_task_manager()
    task = await manager.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    if task.status != "completed" or not task.result_path:
        raise HTTPException(status_code=400, detail="任务未完成或无可下载文件")
    path = Path(task.result_path)
    if not path.is_file():
        raise HTTPException(status_code=404, detail="文件不存在")
    return FileResponse(path=path, filename=path.name, media_type="video/mp4")


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str) -> TaskResponse:
    """获取任务状态。"""
    manager = get_task_manager()
    task = await manager.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    data = task.to_public_dict()
    return TaskResponse(**data)
