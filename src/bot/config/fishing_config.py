from typing import Dict, Any
from .base_config import BaseConfig

try:
    from .screen_config import ScreenConfig
except ImportError:
    from .screen_config_safe import ScreenConfig
from .detection_config import DetectionConfig
from ..framework.registration import register_config


@register_config("fishing")
class FishingConfig(BaseConfig):
    """Configuration for fishing bot"""

    def __init__(self):
        super().__init__()

        # Core configurations
        self.screen = ScreenConfig()
        self.detection = DetectionConfig()

        # Fishing-specific timeouts
        self.state_timeouts = {
            "STARTING": 10,
            "CHECKING_ROD": 15,
            "CASTING_BAIT": 15,
            "WAITING_FOR_BITE": 25,
            "PLAYING_MINIGAME": 30,
            "FINISHING": 10,
        }

        # Fishing-specific settings
        self.quick_finish_enabled = False
        self.casting_delay = 0.5
        self.finish_wait_delay = 0.5

        # Initialize bot-specific defaults
        self._bot_specific = {
            "auto_rod_swap": True,
            "preferred_rod": "sturdy",
            "minigame_strategy": "balanced",
        }

    def get_bot_type(self) -> str:
        return "fishing"

    def get_state_timeouts(self) -> Dict[str, Any]:
        return self.state_timeouts.copy()

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary"""
        base_dict = super().to_dict()
        base_dict.update(
            {
                "quick_finish_enabled": self.quick_finish_enabled,
                "casting_delay": self.casting_delay,
                "finish_wait_delay": self.finish_wait_delay,
                "screen": self.screen.__dict__,
                "detection": self.detection.__dict__,
            }
        )
        return base_dict

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FishingConfig":
        """Create config from dictionary"""
        config = cls()

        # Update basic properties
        for key in [
            "debug_mode",
            "target_fps",
            "default_delay",
            "quick_finish_enabled",
            "casting_delay",
            "finish_wait_delay",
        ]:
            if key in data:
                setattr(config, key, data[key])

        # Update state timeouts
        if "state_timeouts" in data:
            config.state_timeouts.update(data["state_timeouts"])

        # Update screen config
        if "screen" in data:
            for key, value in data["screen"].items():
                if hasattr(config.screen, key):
                    setattr(config.screen, key, value)

        # Update detection config
        if "detection" in data:
            for key, value in data["detection"].items():
                if hasattr(config.detection, key):
                    setattr(config.detection, key, value)

        # Update bot-specific settings
        if "bot_specific" in data:
            config._bot_specific.update(data["bot_specific"])

        return config
