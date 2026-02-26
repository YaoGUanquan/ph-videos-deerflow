"""ph-videos 镜头语言评分员 Sub-Agent"""

from src.subagents.config import SubagentConfig

PH_VIDEOS_SCORER_CINEMATOGRAPHY_CONFIG = SubagentConfig(
    name="ph-videos-scorer-cinematography",
    description="""Specialist scorer for video script CINEMATOGRAPHY dimension (shot types, camera movements).
Use when the lead agent needs to score a video script on cinematography: 景别（全景/中景/近景/特写）、运镜（推进/拉远/跟随）是否清晰合理.
Output format: 【维度】镜头语言 【得分】X/15 【修改建议】...""",
    system_prompt="""你是一位专业的视频脚本评分专家，专注「镜头语言」维度。请对视频分镜脚本的景别、运镜、构图进行评分（满分15分）。

输出格式必须严格为：
【维度】镜头语言
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
