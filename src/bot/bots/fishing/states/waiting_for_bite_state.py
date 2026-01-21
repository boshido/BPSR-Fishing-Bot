import time
from typing import Any
from ....framework.base_state import BaseState
from ....framework.state_type import StateType


class FishingWaitingForBiteState(BaseState):
    """Fishing bot waiting for bite state"""

    def __init__(self, bot):
        super().__init__(bot)
        self._last_wait_log = 0

    def handle(self, screen: Any) -> StateType:
        """Handle waiting for bite logic"""
        pos = self.detector.find(
            screen, "exclamation", 1, debug=self.bot.config.debug_mode
        )

        if pos:
            self.bot.log("[WAITING_FOR_BITE] ❗ Fish hooked!")
            self.controller.mouse_down("left")
            return StateType.PLAYING_MINIGAME
        else:
            current_time = time.time()
            if current_time - self._last_wait_log > 5:
                self.bot.log("[WAITING_FOR_BITE] ⏳ Waiting for fish...")
                self._last_wait_log = current_time

            return StateType.WAITING_FOR_BITE

    def get_state_type(self) -> StateType:
        return StateType.WAITING_FOR_BITE

    def get_timeout_limit(self) -> float:
        return 25.0
