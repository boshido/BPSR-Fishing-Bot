import time
from typing import Any
from ....framework.base_state import BaseState
from ....framework.state_type import StateType


class FishingCheckingRodState(BaseState):
    """Fishing bot rod checking state"""

    def handle(self, screen: Any) -> StateType:
        """Handle rod checking logic"""
        self.bot.log("[CHECKING_ROD] Checking rod...")
        time.sleep(1)

        found_rod = False

        # Check for different rod types
        if self.detector.find(screen, "flex_rod", 5, debug=self.bot.config.debug_mode):
            found_rod = True
        elif self.detector.find(
            screen, "sturdy_rod", 5, debug=self.bot.config.debug_mode
        ):
            found_rod = True
        elif self.detector.find(screen, "reg_rod", 5, debug=self.bot.config.debug_mode):
            found_rod = True

        if not found_rod:
            self.bot.log("[CHECKING_ROD] ⚠️  Broken rod! Replacing...")
            self.bot.stats.increment("rod_breaks")
            time.sleep(1)

            self.controller.press_key("m")
            time.sleep(1)

            x = 1650 + self.bot.config.screen.monitor_x
            y = 580 + self.bot.config.screen.monitor_y

            self.controller.move_to(x, y)
            time.sleep(0.5)
            self.controller.move_to(x, y)
            time.sleep(0.5)
            self.controller.click("left")
            time.sleep(1)

            self.bot.log("[CHECKING_ROD] ✅ Rod replaced")
        else:
            time.sleep(1)
            self.bot.log("[CHECKING_ROD] ✅ Rod OK")

        return StateType.CASTING_BAIT

    def get_state_type(self) -> StateType:
        return StateType.CHECKING_ROD

    def get_timeout_limit(self) -> float:
        return 15.0
