"""Built-in subagent configurations."""

from .bash_agent import BASH_AGENT_CONFIG
from .general_purpose import GENERAL_PURPOSE_CONFIG
from .ph_videos_scorer_cinematography import PH_VIDEOS_SCORER_CINEMATOGRAPHY_CONFIG
from .ph_videos_scorer_description import PH_VIDEOS_SCORER_DESCRIPTION_CONFIG
from .ph_videos_scorer_coherence import PH_VIDEOS_SCORER_COHERENCE_CONFIG
from .ph_videos_scorer_character import PH_VIDEOS_SCORER_CHARACTER_CONFIG
from .ph_videos_scorer_feasibility import PH_VIDEOS_SCORER_FEASIBILITY_CONFIG
from .ph_videos_scorer_user_intent import PH_VIDEOS_SCORER_USER_INTENT_CONFIG
from .ph_videos_scorer_style_atmosphere import PH_VIDEOS_SCORER_STYLE_ATMOSPHERE_CONFIG

__all__ = [
    "GENERAL_PURPOSE_CONFIG",
    "BASH_AGENT_CONFIG",
    "PH_VIDEOS_SCORER_CINEMATOGRAPHY_CONFIG",
    "PH_VIDEOS_SCORER_DESCRIPTION_CONFIG",
    "PH_VIDEOS_SCORER_COHERENCE_CONFIG",
    "PH_VIDEOS_SCORER_CHARACTER_CONFIG",
    "PH_VIDEOS_SCORER_FEASIBILITY_CONFIG",
    "PH_VIDEOS_SCORER_USER_INTENT_CONFIG",
    "PH_VIDEOS_SCORER_STYLE_ATMOSPHERE_CONFIG",
]

# Registry of built-in subagents
BUILTIN_SUBAGENTS = {
    "general-purpose": GENERAL_PURPOSE_CONFIG,
    "bash": BASH_AGENT_CONFIG,
    "ph-videos-scorer-cinematography": PH_VIDEOS_SCORER_CINEMATOGRAPHY_CONFIG,
    "ph-videos-scorer-description": PH_VIDEOS_SCORER_DESCRIPTION_CONFIG,
    "ph-videos-scorer-coherence": PH_VIDEOS_SCORER_COHERENCE_CONFIG,
    "ph-videos-scorer-character": PH_VIDEOS_SCORER_CHARACTER_CONFIG,
    "ph-videos-scorer-feasibility": PH_VIDEOS_SCORER_FEASIBILITY_CONFIG,
    "ph-videos-scorer-user-intent": PH_VIDEOS_SCORER_USER_INTENT_CONFIG,
    "ph-videos-scorer-style-atmosphere": PH_VIDEOS_SCORER_STYLE_ATMOSPHERE_CONFIG,
}
