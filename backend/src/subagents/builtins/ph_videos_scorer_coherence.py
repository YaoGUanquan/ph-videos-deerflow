"""ph-videos 连贯性评分员 Sub-Agent"""

from src.subagents.config import SubagentConfig

PH_VIDEOS_SCORER_COHERENCE_CONFIG = SubagentConfig(
    name="ph-videos-scorer-coherence",
    description="""Specialist scorer for video script COHERENCE (scene transitions, narrative logic).
Use when scoring scene continuity and narrative flow.
Output format: 【维度】连贯性 【得分】X/15 【修改建议】...""",
    system_prompt="""你是一位专业的视频脚本评分专家，专注「连贯性」维度。请评估场景衔接、叙事逻辑（满分15分）。

输出格式必须严格为：
【维度】连贯性
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
