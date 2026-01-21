import time
from typing import Any
from ....framework.base_state import BaseState
from ....framework.state_type import StateType


class MiningOreState(BaseState):
    """Mining bot mining ore state"""

    def __init__(self, bot):
        super().__init__(bot)
        self._mining_start_time = None

    def handle(self, screen: Any) -> StateType:
        """Handle mining ore logic"""
        if self._mining_start_time is None:
            self._mining_start_time = time.time()
            self.bot.log("[MINING_ORE] ⛏️ Starting to mine ore...")
            time.sleep(2)  # Mining animation time

        # Simulate mining progress
        elapsed_time = time.time() - self._mining_start_time

        if elapsed_time > 5:  # Assume mining is done after 5 seconds
            self.bot.log("[MINING_ORE] ✅ Mining completed!")
            self.bot.stats.increment("ore_collected")
            self._mining_start_time = None

            # Check if inventory is full (simplified)
            if self.bot.stats.get("ore_collected", 0) % 10 == 0:  # Every 10 ores
                self.bot.log("[MINING_ORE] 🎒 Inventory getting full...")
                return StateType.RETURNING_TO_BASE

            # Continue mining
            return StateType.SCANNING_FOR_ORE

        # Continue mining
        if int(elapsed_time) % 2 == 0:
            self.bot.log(f"[MINING_ORE] ⛏️ Mining... ({int(elapsed_time)}s)")

        return StateType.MINING_ORE

    def get_state_type(self) -> StateType:
        return StateType.MINING_ORE

    def get_timeout_limit(self) -> float:
        return 60.0
