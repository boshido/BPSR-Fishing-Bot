from typing import Dict, Any
from ..config.base_config import BaseConfig


class MiningConfig(BaseConfig):
    """Configuration for mining bot"""

    def __init__(self):
        super().__init__()

        # Mining-specific timeouts
        self.state_timeouts = {
            "MINING_STARTING": 10,
            "SCANNING_FOR_ORE": 30,
            "MINING_ORE": 60,
            "RETURNING_TO_BASE": 15,
        }

        # Mining-specific settings
        self.target_ores = ["iron", "copper", "gold"]
        self.max_inventory_slots = 20
        self.mining_range = 50
        self.return_when_full = True

        # Initialize bot-specific defaults
        self._bot_specific = {
            "auto_smelt": True,
            "preferred_pickaxe": "steel",
            "mining_strategy": "efficient",
        }

    def get_bot_type(self) -> str:
        return "mining"

    def get_state_timeouts(self) -> Dict[str, Any]:
        return self.state_timeouts.copy()
