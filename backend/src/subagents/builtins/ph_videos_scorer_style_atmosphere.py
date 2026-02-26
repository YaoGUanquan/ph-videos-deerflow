"""ph-videos Style & Atmosphere scorer Sub-Agent"""

from src.subagents.config import SubagentConfig

PH_VIDEOS_SCORER_STYLE_ATMOSPHERE_CONFIG = SubagentConfig(
    name="ph-videos-scorer-style-atmosphere",
    description="""Specialist scorer for video script STYLE AND ATMOSPHERE consistency.
Use when scoring if visual style, mood, lighting, and aesthetic tone are unified across scenes.
Output format: [Dimension] Style & Atmosphere [Score] X/10 [Suggestions]...""",
    system_prompt="""You are an expert video script scorer focused on the STYLE AND ATMOSPHERE dimension. Evaluate whether visual style, lighting, mood, and aesthetic tone are consistent across scenes (max 10).

Output format MUST be strictly:
[Dimension] Style & Atmosphere
[Score] X/10
[Suggestions]
(1-3 actionable, specific suggestions)

Output only the above format, no other explanation.""",
    tools=None,
    disallowed_tools=["task", "ask_clarification", "present_files"],
    model="inherit",
    max_turns=5,
    timeout_seconds=120,
)
