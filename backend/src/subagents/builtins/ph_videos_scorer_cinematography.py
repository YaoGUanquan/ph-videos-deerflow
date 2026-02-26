"""ph-videos Cinematography scorer Sub-Agent"""

from src.subagents.config import SubagentConfig

PH_VIDEOS_SCORER_CINEMATOGRAPHY_CONFIG = SubagentConfig(
    name="ph-videos-scorer-cinematography",
    description="""Specialist scorer for video script CINEMATOGRAPHY dimension (shot types, camera movements).
Use when scoring shot types (wide/medium/close-up), camera movements (push/pull/follow), composition clarity.
Output format: [Dimension] Cinematography [Score] X/15 [Suggestions]...""",
    system_prompt="""You are an expert video script scorer focused on the CINEMATOGRAPHY dimension. Score shot types (wide/medium/close-up), camera movements (push/pull/follow/orbit), and composition clarity (max 15).

Output format MUST be strictly:
[Dimension] Cinematography
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
