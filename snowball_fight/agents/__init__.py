from .base import BaseAgent
from .all_c import AllCAgent
from .all_d import AllDAgent
from .tit_for_tat import TitForTatAgent
from .spiteful import Spiteful
from .soft_majo import SoftMojo
from .hard_majo import HardMojo

ALL_AGENTS = [
    AllCAgent,
    AllDAgent,
    TitForTatAgent,
    Spiteful,
    SoftMojo,
    HardMojo,
]
