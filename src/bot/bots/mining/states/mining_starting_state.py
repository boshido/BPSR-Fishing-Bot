import time
from typing import Any
from ....framework.base_state import BaseState
from ....framework.state_type import StateType


class MiningStartingState(BaseState):
    """Mining bot starting state"""

    def handle(self, screen: Any) -> StateType:
        """Handle starting state logic"""
        self.bot.log("[MINING_STARTING] 🎯 Initializing mining bot...")
        time.sleep(1)

        # Simulate finding mining location
        self.bot.log("[MINING_STARTING] ✅ Mining location found")
        return StateType.SCANNING_FOR_ORE

    def get_state_type(self) -> StateType:
        return StateType.MINING_STARTING

    def get_timeout_limit(self) -> float:
        return 10.0
