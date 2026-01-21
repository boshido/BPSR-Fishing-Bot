import time
from typing import Any
from ....framework.base_state import BaseState
from ....framework.state_type import StateType


class FishingStartingState(BaseState):
    """Fishing bot starting state - looking for fishing spot"""

    def __init__(self, bot):
        super().__init__(bot)
        self._last_search_log = 0

    def handle(self, screen: Any) -> StateType:
        """Handle starting state logic"""

        # Check for server connection dialog
        if self.detector.find(
            screen, "connect_server", 5, debug=self.bot.config.debug_mode
        ):
            x = 1100 + self.bot.config.screen.monitor_x
            y = 795 + self.bot.config.screen.monitor_y

            self.controller.move_to(x, y)
            time.sleep(0.5)
            self.controller.move_to(x, y)
            time.sleep(0.5)
            self.controller.click("left")
            time.sleep(1)

            self.bot.log("[RECONNECT] ✅ confirm server connection")

        # Normal case: detect the fishing spot button
        pos = self.detector.find(
            screen, "fishing_spot_btn", 5, debug=self.bot.config.debug_mode
        )

        if pos:
            self.bot.log(f"[STARTING] ✅ Fishing spot detected at {pos}")
            self.bot.log("[STARTING] Pressing 'F'...")
            time.sleep(0.5)

            self.controller.press_key("f")
            self.bot.log("[STARTING] Entering fishing mode")
            time.sleep(2)

            return StateType.CHECKING_ROD

        # Check if already in fishing mode
        already_fishing = self.detector.find(
            screen, "level_check", 5, debug=self.bot.config.debug_mode
        )

        if already_fishing:
            self.bot.log("[STARTING] 🎣 Already in fishing mode — skipping interaction")
            return StateType.CHECKING_ROD

        # Still searching for fishing spot
        current_time = time.time()
        if current_time - self._last_search_log > 2:
            self.bot.log("[STARTING] 🔍 Searching for fishing spot...")

            # Wiggle a bit to get the fishing button to come back up
            self.controller.key_down("s")
            self.controller.key_down("d")
            time.sleep(0.1)
            self.controller.key_up("s")
            self.controller.key_up("d")

            if self.bot.config.debug_mode:
                self.bot.log("[STARTING] 💡 Debug enabled")
            self._last_search_log = current_time

        return StateType.STARTING

    def get_state_type(self) -> StateType:
        return StateType.STARTING

    def get_timeout_limit(self) -> float:
        return 10.0
