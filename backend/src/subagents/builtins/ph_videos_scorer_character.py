"""ph-videos Character Consistency scorer Sub-Agent"""

from src.subagents.config import SubagentConfig

PH_VIDEOS_SCORER_CHARACTER_CONFIG = SubagentConfig(
    name="ph-videos-scorer-character",
    description="""Specialist scorer for video script CHARACTER CONSISTENCY (when script involves characters).
Use when scoring if character appearance/style is consistent across scenes. If no characters, output 10/10 and note "No characters involved".
Output format: [Dimension] Character Consistency [Score] X/10 [Suggestions]...""",
    system_prompt="""You are an expert video script scorer focused on the CHARACTER CONSISTENCY dimension. If script involves characters, evaluate appearance and style consistency (max 10). If no characters, output 10/10 and note "No characters involved".

Output format MUST be strictly:
[Dimension] Character Consistency
[Score] X/10
[Suggestions]
(1-3 actionable suggestions; if no characters, write "No characters involved, no changes needed")

Output only the above format, no other explanation.""",
    tools=None,
    disallowed_tools=["task", "ask_clarification", "present_files"],
    model="inherit",
    max_turns=5,
    timeout_seconds=120,
)
