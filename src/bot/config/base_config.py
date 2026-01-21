from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseConfig(ABC):
    """Base configuration class for all bots"""

    def __init__(self):
        # Common configurations
        self.debug_mode = False
        self.target_fps = 0  # 0 means unlimited
        self.default_delay = 0.5

        # Bot-specific configuration
        self._bot_specific = {}

    @abstractmethod
    def get_bot_type(self) -> str:
        """Return the bot type this config is for"""
        pass

    def get_state_timeouts(self) -> Dict[str, float]:
        """Return state timeout configuration (can be overridden)"""
        return {}

    def get_bot_specific(self) -> Dict[str, Any]:
        """Get bot-specific configuration"""
        return self._bot_specific

    def set_bot_specific(self, key: str, value: Any) -> None:
        """Set bot-specific configuration value"""
        self._bot_specific[key] = value

    def get_bot_specific_value(self, key: str, default: Any = None) -> Any:
        """Get bot-specific configuration value"""
        return self._bot_specific.get(key, default)

    def update_from_dict(self, data: Dict[str, Any]) -> None:
        """Update configuration from dictionary"""
        for key, value in data.items():
            if hasattr(self, key) and not key.startswith("_"):
                setattr(self, key, value)
            else:
                self.set_bot_specific(key, value)

    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary for serialization"""
        return {
            "bot_type": self.get_bot_type(),
            "debug_mode": self.debug_mode,
            "target_fps": self.target_fps,
            "default_delay": self.default_delay,
            "state_timeouts": self.get_state_timeouts(),
            "bot_specific": self._bot_specific,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseConfig":
        """Create config from dictionary"""
        config = cls()
        config.update_from_dict(data)
        return config
