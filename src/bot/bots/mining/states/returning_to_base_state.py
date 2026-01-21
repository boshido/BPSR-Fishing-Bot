import time
from typing import Any
from ....framework.base_state import BaseState
from ....framework.state_type import StateType


class ReturningToBaseState(BaseState):
    """Mining bot returning to base state"""

    def __init__(self, bot):
        super().__init__(bot)
        self._return_start_time = None

    def handle(self, screen: Any) -> StateType:
        """Handle returning to base logic"""
        if self._return_start_time is None:
            self._return_start_time = time.time()
            self.bot.log("[RETURNING_TO_BASE] 🏠 Returning to base...")

        # Simulate travel time
        elapsed_time = time.time() - self._return_start_time

        if elapsed_time > 3:  # Assume at base after 3 seconds
            self.bot.log("[RETURNING_TO_BASE] ✅ Arrived at base!")
            self.bot.log("[RETURNING_TO_BASE] 🎒 Unloading inventory...")
            self.bot.stats.set("ore_collected", 0)  # Reset counter
            self._return_start_time = None

            # Return to mining
            return StateType.MINING_STARTING

        # Continue returning
        return StateType.RETURNING_TO_BASE

    def get_state_type(self) -> StateType:
        return StateType.RETURNING_TO_BASE

    def get_timeout_limit(self) -> float:
        return 15.0
