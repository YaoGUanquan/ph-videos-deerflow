"""模型路由，根据场景与预算选择视频生成模型。"""

from src.ph_videos.budget import BudgetController

# 支持的 provider：volcano, wanxiang, comfyui
PRIORITY_ORDER = ["volcano", "wanxiang", "comfyui"]


class ModelRouter:
    """根据场景类型与预算选择视频生成 provider。"""

    def __init__(self, prefer_quality: bool = True) -> None:
        """
        Args:
            prefer_quality: 若 True，优先选 volcano；否则按预算从高到低尝试
        """
        self.prefer_quality = prefer_quality

    def select_model(
        self,
        scene: dict[str, str] | str,
        budget: BudgetController,
    ) -> str:
        """
        选择视频生成 provider。

        Args:
            scene: 场景描述（dict 或 str），若为 dict 可含 type 等字段
            budget: 预算控制器

        Returns:
            volcano | wanxiang | comfyui
        """
        if isinstance(scene, str):
            scene = {"prompt": scene, "type": "normal"}

        scene_type = scene.get("type", "normal")
        order = PRIORITY_ORDER if self.prefer_quality else ["comfyui", "wanxiang", "volcano"]

        for provider in order:
            if budget.can_afford(provider):
                return provider

        # 预算不足时返回成本最低的
        return "comfyui"
