from enum import Enum, auto


class StateType(Enum):
    # Generic states
    STARTING = auto()
    FINISHING = auto()
    IDLE = auto()

    # Fishing states (backward compatibility)
    CHECKING_ROD = auto()
    CASTING_BAIT = auto()
    WAITING_FOR_BITE = auto()
    PLAYING_MINIGAME = auto()

    # Mining states (for future implementation)
    MINING_STARTING = auto()
    SCANNING_FOR_ORE = auto()
    MINING_ORE = auto()
    RETURNING_TO_BASE = auto()

    # Add more states for other bot types as needed
