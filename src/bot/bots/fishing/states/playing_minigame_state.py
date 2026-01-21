import time
from typing import Any
from ....framework.base_state import BaseState
from ....framework.state_type import StateType


class FishingPlayingMinigameState(BaseState):
    """Fishing bot minigame playing state"""

    def __init__(self, bot):
        super().__init__(bot)
        self._current_direction = None
        self.switch_delay = 0.5

    def _handle_arrow(self, direction: str, screen: Any) -> None:
        """Handle arrow detection and key presses"""
        arrow_template = f"{direction}_arrow"
        key_to_press = "a" if direction == "left" else "d"
        key_to_release = "d" if direction == "left" else "a"
        opposite_direction = "right" if direction == "left" else "left"

        if self.detector.find(screen, arrow_template):
            if self._current_direction is None:
                self.bot.log(
                    f"[MINIGAME] ▶️ Moving to the {direction} (Holding '{key_to_press}')"
                )
                self.controller.key_down(key_to_press)
                self._current_direction = direction
                time.sleep(self.switch_delay)

            if self._current_direction == opposite_direction:
                self.bot.log(
                    f"[MINIGAME] ◀️ Switching to the {direction} (Releasing '{key_to_release}')"
                )
                self.controller.key_up(key_to_release)
                self._current_direction = None
                time.sleep(self.switch_delay)

    def handle(self, screen: Any) -> StateType:
        """Handle minigame logic"""
        fish_complete = 0
        failed = 0

        if self.detector.find(screen, "success", 1, debug=False):
            fish_complete = 1
            self.bot.log("[MINIGAME] 🐟 Fish caught!")
            self.bot.stats.increment("fish_caught")

        if fish_complete == 0 and self.detector.find(screen, "failure", 1, debug=False):
            fish_complete = 1
            failed = 1
            self.bot.log("[MINIGAME] 🐟 Fish got away!")
            self.bot.stats.increment("fish_escaped")

        if fish_complete == 1:
            self.controller.release_all_controls()
            self._current_direction = None

            quick_finish_enabled = getattr(
                self.bot.config, "quick_finish_enabled", False
            )
            if quick_finish_enabled:
                self.bot.log("[MINIGAME] ⏩ Quick finishing...")
                self.controller.press_key("esc")
                time.sleep(0.5)
                return StateType.STARTING
            else:
                if failed == 0:
                    return StateType.FINISHING
                else:
                    time.sleep(2)
                    return StateType.CHECKING_ROD

        self._handle_arrow("left", screen)
        self._handle_arrow("right", screen)

        return StateType.PLAYING_MINIGAME

    def get_state_type(self) -> StateType:
        return StateType.PLAYING_MINIGAME

    def get_timeout_limit(self) -> float:
        return 30.0
