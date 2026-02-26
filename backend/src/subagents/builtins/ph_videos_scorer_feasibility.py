"""ph-videos Feasibility scorer Sub-Agent"""

from src.subagents.config import SubagentConfig

PH_VIDEOS_SCORER_FEASIBILITY_CONFIG = SubagentConfig(
    name="ph-videos-scorer-feasibility",
    description="""Specialist scorer for video script FEASIBILITY (model compatibility).
Use when scoring if script is suitable for Seedance/Wanxiang/ComfyUI video models.
Output format: [Dimension] Feasibility [Score] X/15 [Suggestions]...""",
    system_prompt="""You are an expert video script scorer focused on the FEASIBILITY dimension. Evaluate whether the script is suitable for Seedance/Wanxiang/ComfyUI video models (max 15). Do NOT evaluate user intent or style/atmosphere (handled by other scorers).

Output format MUST be strictly:
[Dimension] Feasibility
[Score] X/15
[Suggestions]
(1-3 actionable, specific suggestions)

Output only the above format, no other explanation.""",
    tools=None,
    disallowed_tools=["task", "ask_clarification", "present_files"],
    model="inherit",
    max_turns=5,
    timeout_seconds=120,
)
