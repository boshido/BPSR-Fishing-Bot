import time
from typing import Any
from ....framework.base_state import BaseState
from ....framework.state_type import StateType


class FishingFinishingState(BaseState):
    """Fishing bot finishing state"""

    def handle(self, screen: Any) -> StateType:
        """Handle finishing logic"""
        pos = self.detector.find(screen, "continue", 5, debug=False)

        if pos:
            self.bot.log("[FINISHING] 🖱️ Clicking 'Continue'...")
            self.controller.move_to(pos[0], pos[1])
            time.sleep(0.5)
            self.controller.move_to(pos[0], pos[1])
            time.sleep(1)
            self.controller.click("left")

            # Count one full fishing attempt
            self.bot.stats.increment("cycles")

            return StateType.CHECKING_ROD

        if self.detector.find(screen, "fishing_spot_btn", 1, debug=False):
            return StateType.STARTING

        return StateType.FINISHING

    def get_state_type(self) -> StateType:
        return StateType.FINISHING

    def get_timeout_limit(self) -> float:
        return 10.0
