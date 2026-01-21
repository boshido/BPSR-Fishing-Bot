import time
from typing import Dict, Any
from ...framework.base_bot import BaseBot
from ...core.interceptors.base_interceptor import BaseInterceptor
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
        
        # Check if this is just a temporary instance for getting description/config
        self._temp_instance = (config is None)

        if not self._temp_instance:
            # Initialize with a compatible config structure for actual bot instances
            compatibility_config = self._create_compatibility_config(self.fishing_config)
            super().__init__(compatibility_config)

            # Override config with our fishing-specific one
            self.config = self.fishing_config
        else:
            # For temporary instances, just call super with minimal config
            # This avoids loading templates unnecessarily
            from ...framework.base_bot import BaseBot
            BaseBot.__init__(self, self.fishing_config)

    def get_bot_type(self) -> str:
        return "fishing"

    def _create_compatibility_config(self, fishing_config: FishingConfig):
        """Create a compatibility config for the base classes"""
        # Create a simple object that has the expected structure
        class CompatibilityConfig:
            def __init__(self, fishing_config):
                self.bot = type('BotConfig', (), {})()
                self.bot.detection = fishing_config.detection
                self.bot.screen = fishing_config.screen
                self.bot.target_fps = fishing_config.target_fps
                # Copy other needed attributes
                self.debug_mode = fishing_config.debug_mode
                self.target_fps = fishing_config.target_fps
                self.default_delay = fishing_config.default_delay
                self.fishing_config = fishing_config
            
            def get_template_path(self, name):
                # Get template filename from detection config
                if name in self.bot.detection.templates:
                    filename = self.bot.detection.templates[name]
                    # Construct full path using the templates path
                    from pathlib import Path
                    templates_path = Path(__file__).parent.parent.parent / "assets" / "templates"
                    return templates_path / filename
                return None
        
        return CompatibilityConfig(fishing_config)

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
        # Only initialize for actual bot instances, not temporary ones
        if hasattr(self, '_temp_instance') and self._temp_instance:
            return

        # Initialize core components first
        self.detector = Detector(self.config)
        self.controller = GameController(self.config)
        self.state_machine = StateMachine(self)

        # Stats tracking
        self.stats = StatsTracker()
        self.stats.add_stat("fish_caught")
        self.stats.add_stat("fish_escaped")
        self.stats.add_stat("rod_breaks")

        # TODO: Fix interceptor type mismatch
        # self.level_check_interceptor = LevelCheckInterceptor(self)
        # self.add_interceptor(self.level_check_interceptor)

    def _register_states(self) -> None:
        """Register fishing states"""
        # Only register states for actual bot instances
        if hasattr(self, '_temp_instance') and self._temp_instance:
            return

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
        self.state_machine.add_state(
            StateType.FINISHING, FishingFinishingState(self)
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
