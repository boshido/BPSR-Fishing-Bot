import time
from typing import Any
from ....framework.base_state import BaseState
from ....framework.state_type import StateType


class FishingCastingBaitState(BaseState):
    """Fishing bot casting bait state"""

    def handle(self, screen: Any) -> StateType:
        """Handle casting bait logic"""
        casting_delay = getattr(self.bot.config, "casting_delay", 0.5)
        self.bot.log(f"[CASTING_BAIT] 🎣 Waiting {casting_delay} seconds...")
        time.sleep(casting_delay)

        center_x = (
            self.bot.config.screen.monitor_width // 2 + self.bot.config.screen.monitor_x
        )
        center_y = (
            self.bot.config.screen.monitor_height // 2
            + self.bot.config.screen.monitor_y
        )

        self.bot.log(
            f"[CASTING_BAIT] 📍 Moving mouse to center of screen ({center_x}, {center_y})"
        )
        self.controller.move_to(center_x, center_y)
        time.sleep(1)

        self.bot.log("[CASTING_BAIT] 🖱️ Clicking to ensure focus...")
        self.controller.click_at(center_x, center_y)
        time.sleep(0.5)

        self.bot.log("[CASTING_BAIT] 🎣 Casting bait...")
        self.controller.mouse_down("left")
        time.sleep(0.1)
        self.controller.mouse_up("left")
        time.sleep(2)

        return StateType.WAITING_FOR_BITE

    def get_state_type(self) -> StateType:
        return StateType.CASTING_BAIT

    def get_timeout_limit(self) -> float:
        return 15.0
