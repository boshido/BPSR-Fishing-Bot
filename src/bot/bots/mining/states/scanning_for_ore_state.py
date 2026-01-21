import time
from typing import Any, List
from ....framework.base_state import BaseState
from ....framework.state_type import StateType


class ScanningForOreState(BaseState):
    """Mining bot scanning for ore state"""

    def __init__(self, bot):
        super().__init__(bot)
        self._last_scan_log = 0

    def _find_ore_positions(self, screen: Any) -> List[tuple]:
        """Simulate finding ore positions (would use detector in real implementation)"""
        # This would normally use detector.find() with ore templates
        # For demo, we'll simulate finding ore
        import random

        if random.random() > 0.7:  # 30% chance to find ore
            return [(random.randint(100, 800), random.randint(100, 600))]
        return []

    def handle(self, screen: Any) -> StateType:
        """Handle scanning for ore logic"""
        ore_positions = self._find_ore_positions(screen)

        if ore_positions:
            closest_ore = ore_positions[0]  # Simplified - just take first
            self.bot.target_ore = closest_ore
            self.bot.log(f"[SCANNING_FOR_ORE] ⛏️ Found ore at position: {closest_ore}")
            return StateType.MINING_ORE

        # Continue scanning
        current_time = time.time()
        if current_time - self._last_scan_log > 3:
            self.bot.log("[SCANNING_FOR_ORE] 🔍 Scanning for ore deposits...")
            self._perform_scan_rotation()
            self._last_scan_log = current_time

        return StateType.SCANNING_FOR_ORE

    def _perform_scan_rotation(self) -> None:
        """Perform scanning rotation"""
        # Simulate scanning by rotating view
        self.bot.log("[SCANNING_FOR_ORE] 🔄 Rotating view...")
        time.sleep(0.5)

    def get_state_type(self) -> StateType:
        return StateType.SCANNING_FOR_ORE

    def get_timeout_limit(self) -> float:
        return 30.0
