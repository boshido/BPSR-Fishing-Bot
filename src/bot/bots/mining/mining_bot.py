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

        # Create compatible config for base classes
        compatibility_config = BaseConfig()
        compatibility_config.debug_mode = self.mining_config.debug_mode
        compatibility_config.target_fps = self.mining_config.target_fps
        compatibility_config.default_delay = self.mining_config.default_delay

        super().__init__(compatibility_config)

        # Override config with our mining-specific one
        self.config = self.mining_config

        # Initialize components after config is set
        self._init_components()

    def get_bot_type(self) -> str:
        return "mining"

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
        # Add mining-specific interceptors if needed
        pass

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
