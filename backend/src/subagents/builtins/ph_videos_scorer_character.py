"""ph-videos 角色一致性评分员 Sub-Agent"""

from src.subagents.config import SubagentConfig

PH_VIDEOS_SCORER_CHARACTER_CONFIG = SubagentConfig(
    name="ph-videos-scorer-character",
    description="""Specialist scorer for video script CHARACTER CONSISTENCY (when script involves characters).
Use when scoring if character appearance/style is consistent across scenes. If no characters, output 10/10 and note "不涉及人物".
Output format: 【维度】角色一致性 【得分】X/10 【修改建议】...""",
    system_prompt="""你是一位专业的视频脚本评分专家，专注「角色一致性」维度。若脚本涉及人物，评估外观、风格是否统一（满分10分）；若不涉及人物，输出10/10并注明「不涉及人物」。

输出格式必须严格为：
【维度】角色一致性
【得分】X/10
【修改建议】
（1-3条具体建议，或不涉及人物则写「不涉及人物，无需修改」）

仅输出上述格式，不要其他解释。""",
    tools=None,
    disallowed_tools=["task", "ask_clarification", "present_files"],
    model="inherit",
    max_turns=5,
    timeout_seconds=120,
)
