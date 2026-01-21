from typing import Dict, Type, Any
from .base_config import BaseConfig


class ConfigRegistry:
    """Registry for configuration classes"""

    _config_types: Dict[str, Type[BaseConfig]] = {}

    @classmethod
    def register_config(cls, bot_type: str, config_class: Type[BaseConfig]) -> None:
        """Register a configuration class for a bot type"""
        cls._config_types[bot_type] = config_class

    @classmethod
    def create_config(cls, bot_type: str, data: Dict[str, Any] = None) -> BaseConfig:
        """Create configuration instance for bot type"""
        if bot_type not in cls._config_types:
            raise ValueError(f"No config class registered for bot type: {bot_type}")

        config_class = cls._config_types[bot_type]

        if data:
            return config_class.from_dict(data)
        else:
            return config_class()

    @classmethod
    def get_available_configs(cls) -> list:
        """Get list of available bot types with configs"""
        return list(cls._config_types.keys())
