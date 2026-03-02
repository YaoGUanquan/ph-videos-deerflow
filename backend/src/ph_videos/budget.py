"""成本预算控制器。"""

# 成本模型：覆盖 script、scene、audio
COST_MODEL = {
    "llm_script": 0.05,  # 每千 token 估算
    "volcano": 3.0,
    "wanxiang": 1.0,
    "comfyui": 0.2,
    "tts": 0.1,  # 预留，暂不实现旁白
}


class BudgetExceededError(Exception):
    """预算耗尽异常。"""

    pass


class BudgetController:
    """成本预算控制器，确保任务在预算范围内运行。"""

    def __init__(self, total_budget: float) -> None:
        self.total_budget = total_budget
        self.spent = 0.0

    def can_afford(self, cost_key: str) -> bool:
        """检查是否还有足够预算支付指定成本。"""
        cost = COST_MODEL.get(cost_key, 0.0)
        return self.spent + cost <= self.total_budget

    def consume(self, cost_key: str) -> float:
        """
        扣减预算。

        Args:
            cost_key: 成本项键名（llm_script, volcano, wanxiang, comfyui, tts）

        Returns:
            本次扣减的成本

        Raises:
            BudgetExceededError: 预算不足
        """
        cost = COST_MODEL.get(cost_key, 0.0)
        if self.spent + cost > self.total_budget:
            raise BudgetExceededError(
                f"预算耗尽: 已用 {self.spent:.2f}, 需 {cost:.2f}, 总额 {self.total_budget:.2f}"
            )
        self.spent += cost
        return cost

    def consume_custom(self, amount: float) -> None:
        """
        扣减自定义金额（如按 token 估算的 LLM 成本）。

        Raises:
            BudgetExceededError: 预算不足
        """
        if self.spent + amount > self.total_budget:
            raise BudgetExceededError(
                f"预算耗尽: 已用 {self.spent:.2f}, 需 {amount:.2f}, 总额 {self.total_budget:.2f}"
            )
        self.spent += amount
