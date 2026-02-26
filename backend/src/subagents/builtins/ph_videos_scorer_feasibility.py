"""ph-videos 可执行性评分员 Sub-Agent"""

from src.subagents.config import SubagentConfig

PH_VIDEOS_SCORER_FEASIBILITY_CONFIG = SubagentConfig(
    name="ph-videos-scorer-feasibility",
    description="""Specialist scorer for video script FEASIBILITY (user intent match, model compatibility, style consistency).
Use when scoring if script matches user intent and is suitable for Seedance/Wanxiang/ComfyUI.
Output format: 【维度】可执行性 【得分】X/15 【修改建议】...""",
    system_prompt="""你是一位专业的视频脚本评分专家，专注「可执行性」维度。评估与用户意图匹配、是否适合Seedance/通义万相/ComfyUI、风格氛围统一（满分15分）。

输出格式必须严格为：
【维度】可执行性
【得分】X/15
【修改建议】
（1-3条具体建议，可操作、针对性强）

仅输出上述格式，不要其他解释。""",
    tools=None,
    disallowed_tools=["task", "ask_clarification", "present_files"],
    model="inherit",
    max_turns=5,
    timeout_seconds=120,
)
