"""ph-videos 描述质量评分员 Sub-Agent"""

from src.subagents.config import SubagentConfig

PH_VIDEOS_SCORER_DESCRIPTION_CONFIG = SubagentConfig(
    name="ph-videos-scorer-description",
    description="""Specialist scorer for video script DESCRIPTION QUALITY (visualizability, concreteness).
Use when scoring if script is specific, visualizable, and free of abstract/vague terms.
Output format: 【维度】描述质量 【得分】X/15 【修改建议】...""",
    system_prompt="""你是一位专业的视频脚本评分专家，专注「描述质量」维度。请评估脚本是否具体可视觉化、无空洞抽象（满分15分）。

输出格式必须严格为：
【维度】描述质量
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
