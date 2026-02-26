"""ph-videos Coherence scorer Sub-Agent"""

from src.subagents.config import SubagentConfig

PH_VIDEOS_SCORER_COHERENCE_CONFIG = SubagentConfig(
    name="ph-videos-scorer-coherence",
    description="""Specialist scorer for video script COHERENCE (scene transitions, narrative logic).
Use when scoring scene continuity and narrative flow.
Output format: [Dimension] Coherence [Score] X/15 [Suggestions]...""",
    system_prompt="""You are an expert video script scorer focused on the COHERENCE dimension. Evaluate scene transitions, narrative logic, and continuity in action/camera/mood across segments (max 15).

Output format MUST be strictly:
[Dimension] Coherence
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
