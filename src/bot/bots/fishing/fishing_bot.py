import time
from typing import Dict, Any
from ...framework.base_bot import BaseBot
from ...framework.base_interceptor import BaseInterceptor
from ...framework.state_type import StateType
from ...framework.registration import register_bot
from ...config.fishing_config import FishingConfig
from ...config.base_config import BaseConfig
from ...core.game.controller import GameController
from ...core.game.detector import Detector
from ...shared.state_machine import StateMachine
from ...shared.stats_tracker import StatsTracker
from ...core.interceptors.level_check_interceptor import LevelCheckInterceptor
from .states import (
    FishingStartingState,
    FishingCheckingRodState,
    FishingCastingBaitState,
    FishingWaitingForBiteState,
    FishingPlayingMinigameState,
    FishingFinishingState,
)


@register_bot(
    "fishing",
    "Automated fishing bot that detects bites, plays minigames, and manages equipment",
)
class FishingBot(BaseBot):
    """Fishing bot implementation using the new framework"""

    def __init__(self, config: FishingConfig = None):
        # Use provided config or create default
        self.fishing_config = config or FishingConfig()

        # Initialize with a compatible config structure for now
        # This maintains backward compatibility during migration
        compatibility_config = self._create_compatibility_config(self.fishing_config)

        super().__init__(compatibility_config)

        # Override config with our fishing-specific one
        self.config = self.fishing_config

        # Initialize components after config is set
        self._init_components()

    def get_bot_type(self) -> str:
        return "fishing"

    def _create_compatibility_config(self, fishing_config: FishingConfig) -> BaseConfig:
        """Create a compatibility config for the base classes"""
        compat_config = BaseConfig()
        compat_config.debug_mode = fishing_config.debug_mode
        compat_config.target_fps = fishing_config.target_fps
        compat_config.default_delay = fishing_config.default_delay

        # For backward compatibility, we'll use the existing BotConfig structure
        # This ensures the existing detector and controller still work
        return compat_config

    def _init_components(self) -> None:
        """Initialize components after config is properly set"""
        # Core components with proper config
        self.detector = Detector(self.config)
        self.controller = GameController(self.config)
        self.state_machine = StateMachine(self)

        # Stats tracking
        self.stats = StatsTracker()
        self.stats.add_stat("fish_caught")
        self.stats.add_stat("fish_escaped")
        self.stats.add_stat("rod_breaks")

    def _initialize_components(self) -> None:
        """Initialize fishing-specific components"""
        # Add fishing-specific interceptors
        self.level_check_interceptor = LevelCheckInterceptor(self, priority=100)
        self.add_interceptor(self.level_check_interceptor)

    def _register_states(self) -> None:
        """Register fishing states"""
        self.state_machine.add_state(StateType.STARTING, FishingStartingState(self))
        self.state_machine.add_state(
            StateType.CHECKING_ROD, FishingCheckingRodState(self)
        )
        self.state_machine.add_state(
            StateType.CASTING_BAIT, FishingCastingBaitState(self)
        )
        self.state_machine.add_state(
            StateType.WAITING_FOR_BITE, FishingWaitingForBiteState(self)
        )
        self.state_machine.add_state(
            StateType.PLAYING_MINIGAME, FishingPlayingMinigameState(self)
        )
        self.state_machine.add_state(StateType.FINISHING, FishingFinishingState(self))

    def get_default_config(self) -> Dict[str, Any]:
        """Return default configuration for fishing bot"""
        config = FishingConfig()
        return config.to_dict()

    def _start_main_state(self) -> None:
        """Start fishing in the initial state"""
        self.state_machine.set_state(StateType.STARTING)

    def _on_start(self) -> None:
        """Called when fishing bot starts"""
        self.log("[INFO] 🎣 Fishing bot ready!")
        self.log("[INFO] ⚠️ IMPORTANT: Keep the game in FOCUS (active window)")
        self.log(
            f"[INFO] ⚙️ Accuracy: {self.fishing_config.detection.precision * 100:.0f}%"
        )
        self.log(
            f"[INFO] ⚙️ Target FPS: {'MAX' if self.fishing_config.target_fps == 0 else self.fishing_config.target_fps}"
        )
        self.log("[INFO] ⚠️ Warming up detection system...")
        time.sleep(
            1
        )  # Allows enough time for the screen capture components to initialize

    def _on_stop(self) -> None:
        """Called when fishing bot stops"""
        # Show stats once
        if hasattr(self, "stats"):
            self.stats.show()

    @classmethod
    def get_description(cls) -> str:
        """Get bot description"""
        return "Automated fishing bot that detects bites, plays minigames, and manages equipment"
