"""ph-videos Description Quality scorer Sub-Agent"""

from src.subagents.config import SubagentConfig

PH_VIDEOS_SCORER_DESCRIPTION_CONFIG = SubagentConfig(
    name="ph-videos-scorer-description",
    description="""Specialist scorer for video script DESCRIPTION QUALITY (visualizability, concreteness).
Use when scoring if script is specific, visualizable, and free of abstract/vague terms.
Output format: [Dimension] Description Quality [Score] X/15 [Suggestions]...""",
    system_prompt="""You are an expert video script scorer focused on the DESCRIPTION QUALITY dimension. Evaluate whether descriptions are concrete, visualizable, and free of vague/abstract terms (max 15).

Output format MUST be strictly:
[Dimension] Description Quality
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
