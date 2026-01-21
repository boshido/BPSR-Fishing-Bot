from typing import Dict, Type, Any, List
from .base_bot import BaseBot
from ..utils.logger import log


class BotFactory:
    """Factory class for creating bot instances"""

    _bot_types: Dict[str, Type[BaseBot]] = {}
    _bot_configs: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def register_bot(cls, bot_type: str, bot_class: Type[BaseBot]) -> None:
        """
        Register a new bot type

        Args:
            bot_type: String identifier for the bot
            bot_class: Class that inherits from BaseBot
        """
        cls._bot_types[bot_type] = bot_class
        log(f"[FACTORY] ✅ Registered bot type: {bot_type}")

    @classmethod
    def get_available_bots(cls) -> List[str]:
        """Get list of available bot types"""
        return list(cls._bot_types.keys())

    @classmethod
    def create_bot(cls, bot_type: str, config: Any = None) -> BaseBot:
        """
        Create a bot instance

        Args:
            bot_type: Type of bot to create
            config: Configuration object (optional)

        Returns:
            BaseBot: Bot instance

        Raises:
            ValueError: If bot type is not registered
        """
        if bot_type not in cls._bot_types:
            available = ", ".join(cls._bot_types.keys())
            raise ValueError(f"Unknown bot type: {bot_type}. Available: {available}")

        bot_class = cls._bot_types[bot_type]

        # Use provided config or create default
        if config is None:
            config = cls._create_default_config(bot_type)

        bot = bot_class(config)
        log(f"[FACTORY] 🤖 Created {bot_type} bot")
        return bot

    @classmethod
    def _create_default_config(cls, bot_type: str) -> Any:
        """Create default configuration for a bot type"""
        if bot_type in cls._bot_types:
            # Create temporary bot instance to get default config
            temp_bot = cls._bot_types[bot_type](None)
            return temp_bot.get_default_config()
        return {}

    @classmethod
    def register_default_config(cls, bot_type: str, config: Dict[str, Any]) -> None:
        """Register default configuration for a bot type"""
        cls._bot_configs[bot_type] = config

    @classmethod
    def get_bot_descriptions(cls) -> Dict[str, str]:
        """Get descriptions for all registered bot types"""
        descriptions = {}
        for bot_type in cls._bot_types:
            # Create temporary instance to get description
            try:
                temp_bot = cls._bot_types[bot_type](None)
                descriptions[bot_type] = getattr(
                    temp_bot, "get_description", lambda: f"{bot_type} bot"
                )()
            except:
                descriptions[bot_type] = f"{bot_type} bot"
        return descriptions
