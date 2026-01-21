import time
from typing import Dict, Any
from ...framework.base_bot import BaseBot
from ...framework.base_interceptor import BaseInterceptor
from ...framework.state_type import StateType
from ...framework.registration import register_bot
from ...config.mining_config import MiningConfig
from ...config.base_config import BaseConfig
from ...shared.state_machine import StateMachine
from ...shared.stats_tracker import StatsTracker
from .states import (
    MiningStartingState,
    ScanningForOreState,
    MiningOreState,
    ReturningToBaseState,
)


@register_bot(
    "mining", "Automated mining bot that scans for ore deposits and manages inventory"
)
class MiningBot(BaseBot):
    """Mining bot implementation using framework"""

    def __init__(self, config: MiningConfig = None):
        # Use provided config or create default
        self.mining_config = config or MiningConfig()
        
        # Check if this is just a temporary instance for getting description/config
        self._temp_instance = (config is None)

        if not self._temp_instance:
            # Create compatible config for base classes
            compatibility_config = self._create_compatibility_config(self.mining_config)
            super().__init__(compatibility_config)

            # Override config with our mining-specific one
            self.config = self.mining_config
        else:
            # For temporary instances, just call super with minimal config
            from ...framework.base_bot import BaseBot
            BaseBot.__init__(self, self.mining_config)

    def get_bot_type(self) -> str:
        return "mining"

    def _create_compatibility_config(self, mining_config: MiningConfig):
        """Create a compatibility config for the base classes"""
        # Create a simple object that has the expected structure
        class CompatibilityConfig:
            def __init__(self, mining_config):
                self.bot = type('BotConfig', (), {})()
                # Mining bot might not have detection/screen configs, create basic ones
                if hasattr(mining_config, 'detection'):
                    self.bot.detection = mining_config.detection
                else:
                    # Create basic detection config
                    from ...config.detection_config import DetectionConfig
                    self.bot.detection = DetectionConfig()
                
                if hasattr(mining_config, 'screen'):
                    self.bot.screen = mining_config.screen
                else:
                    # Create basic screen config
                    from ...config.screen_config import ScreenConfig
                    self.bot.screen = ScreenConfig()
                
                self.bot.target_fps = mining_config.target_fps
                # Copy other needed attributes
                self.debug_mode = mining_config.debug_mode
                self.target_fps = mining_config.target_fps
                self.default_delay = mining_config.default_delay
                self.mining_config = mining_config
            
            def get_template_path(self, name):
                # Get template filename from detection config
                if name in self.bot.detection.templates:
                    filename = self.bot.detection.templates[name]
                    # Construct full path using the templates path
                    from pathlib import Path
                    templates_path = Path(__file__).parent.parent.parent / "assets" / "templates"
                    return templates_path / filename
                return None
        
        return CompatibilityConfig(mining_config)

    def _init_components(self) -> None:
        """Initialize components after config is properly set"""
        # Core components - simplified for demo
        self.state_machine = StateMachine(self)

        # Stats tracking
        self.stats = StatsTracker()
        self.stats.add_stat("ore_collected")
        self.stats.add_stat("tools_broken")

    def _initialize_components(self) -> None:
        """Initialize mining-specific components"""
        # Only initialize for actual bot instances, not temporary ones
        if hasattr(self, '_temp_instance') and self._temp_instance:
            return

        # Initialize core components first
        from ...core.game.detector import Detector
        from ...core.game.controller import GameController
        
        self.detector = Detector(self.config)
        self.controller = GameController(self.config)
        self.state_machine = StateMachine(self)

        # Stats tracking
        self.stats = StatsTracker()
        self.stats.add_stat("ore_collected")
        self.stats.add_stat("tools_broken")

        # Add mining-specific interceptors if needed
        pass

    def _register_states(self) -> None:
        """Register mining states"""
        # Only register states for actual bot instances
        if hasattr(self, '_temp_instance') and self._temp_instance:
            return

        self.state_machine.add_state(
            StateType.MINING_STARTING, MiningStartingState(self)
        )
        self.state_machine.add_state(
            StateType.SCANNING_FOR_ORE, ScanningForOreState(self)
        )
        self.state_machine.add_state(StateType.MINING_ORE, MiningOreState(self))
        self.state_machine.add_state(
            StateType.RETURNING_TO_BASE, ReturningToBaseState(self)
        )

    def _register_states(self) -> None:
        """Register mining states"""
        self.state_machine.add_state(
            StateType.MINING_STARTING, MiningStartingState(self)
        )
        self.state_machine.add_state(
            StateType.SCANNING_FOR_ORE, ScanningForOreState(self)
        )
        self.state_machine.add_state(StateType.MINING_ORE, MiningOreState(self))
        self.state_machine.add_state(
            StateType.RETURNING_TO_BASE, ReturningToBaseState(self)
        )

    def get_default_config(self) -> Dict[str, Any]:
        """Return default configuration for mining bot"""
        config = MiningConfig()
        return config.to_dict()

    def _start_main_state(self) -> None:
        """Start mining in the initial state"""
        self.state_machine.set_state(StateType.MINING_STARTING)

    def _on_start(self) -> None:
        """Called when mining bot starts"""
        self.log("[INFO] ⛏️ Mining bot ready!")
        self.log("[INFO] ⚠️ IMPORTANT: Keep the game in FOCUS (active window)")
        self.log(f"[INFO] ⚙️ Target ores: {self.mining_config.target_ores}")
        self.log(
            f"[INFO] ⚙️ Target FPS: {'MAX' if self.mining_config.target_fps == 0 else self.mining_config.target_fps}"
        )

    def _on_stop(self) -> None:
        """Called when mining bot stops"""
        if hasattr(self, "stats"):
            self.stats.show()

    @classmethod
    def get_description(cls) -> str:
        """Get bot description"""
        return "Automated mining bot that scans for ore deposits and manages inventory"
