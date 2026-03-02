"""脚本生成器，独立 LLM 调用。"""

import json
import logging
from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage

from src.config import get_app_config
from src.models.factory import create_chat_model
from src.ph_videos.budget import BudgetController

logger = logging.getLogger(__name__)

SCRIPT_SYSTEM = """你是一个 AI 视频脚本生成专家。根据用户给定的主题，生成适合 AI 视频模型（火山 Seedance、通义万相、ComfyUI）的分镜脚本。

输出要求：
1. 每行一个镜头的描述，格式为：主体 + 动作 + 镜头类型 + 风格
2. 镜头描述要具体、可视觉化，便于视频模型理解
3. 输出纯 JSON，格式：{"scenes": ["镜头1描述", "镜头2描述", ...], "video_style": "2D", "aspect_ratio": "16:9"}
4. 默认 video_style 为 2D，aspect_ratio 为 16:9
5. scenes 数量建议 3-5 个，每个镜头 5-15 秒
"""


class ScriptGenerator:
    """脚本生成器。"""

    def __init__(self, api_key: str | None = None, model_name: str | None = None) -> None:
        self._api_key = api_key
        self._model_name = model_name

    async def generate(
        self,
        topic: str,
        budget: BudgetController,
    ) -> dict[str, Any]:
        """
        根据主题生成分镜脚本。

        Args:
            topic: 视频主题
            budget: 预算控制器

        Returns:
            {"scenes": [...], "video_style": str, "aspect_ratio": str}
        """
        if not budget.can_afford("llm_script"):
            raise RuntimeError("预算不足，无法生成脚本")

        budget.consume("llm_script")

        config = get_app_config()
        model_name = self._model_name or (config.models[0].name if config.models else None)
        if not model_name:
            raise ValueError("未配置 LLM 模型")

        llm = create_chat_model(name=model_name, api_key_override=self._api_key)

        prompt = f"主题：{topic}\n\n请生成分镜脚本，输出 JSON。"
        messages = [
            SystemMessage(content=SCRIPT_SYSTEM),
            HumanMessage(content=prompt),
        ]

        response = await llm.ainvoke(messages)
        text = response.content if hasattr(response, "content") else str(response)

        # 解析 JSON（可能被 markdown 包裹）
        text = text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()

        try:
            data = json.loads(text)
        except json.JSONDecodeError as e:
            logger.warning("ScriptGenerator JSON parse failed, using fallback: %s", e)
            data = {"scenes": [f"关于「{topic}」的画面"], "video_style": "2D", "aspect_ratio": "16:9"}

        if "scenes" not in data or not data["scenes"]:
            data["scenes"] = [f"关于「{topic}」的画面"]
        data.setdefault("video_style", "2D")
        data.setdefault("aspect_ratio", "16:9")

        return data
