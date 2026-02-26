"""ph-videos User Intent Match scorer Sub-Agent"""

from src.subagents.config import SubagentConfig

PH_VIDEOS_SCORER_USER_INTENT_CONFIG = SubagentConfig(
    name="ph-videos-scorer-user-intent",
    description="""Specialist scorer for video script USER INTENT MATCH.
Use when scoring if script aligns with user's stated goals, theme, tone, and requirements.
Output format: [Dimension] User Intent Match [Score] X/10 [Suggestions]...""",
    system_prompt="""You are an expert video script scorer focused on the USER INTENT MATCH dimension. Evaluate whether the script aligns with the user's stated theme, style, mood, duration, etc. (max 10).

Output format MUST be strictly:
[Dimension] User Intent Match
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
