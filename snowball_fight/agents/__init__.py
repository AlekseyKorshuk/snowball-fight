from .base import BaseAgent
from .all_c import AllCAgent
from .all_d import AllDAgent
from .tit_for_tat import TitForTatAgent

ALL_AGENTS = [
    AllCAgent,
    AllDAgent,
    TitForTatAgent,
]
