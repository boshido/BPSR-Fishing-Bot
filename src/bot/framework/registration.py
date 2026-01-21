from typing import Type, Callable, Any
from .base_bot import BaseBot
from .bot_factory import BotFactory
from ..config.config_registry import ConfigRegistry


def register_bot(bot_type: str, description: str = None):
    """
    Decorator to register a bot type

    Args:
        bot_type: String identifier for the bot
        description: Optional description of the bot
    """

    def decorator(bot_class: Type[BaseBot]) -> Type[BaseBot]:
        # Register the bot with the factory
        BotFactory.register_bot(bot_type, bot_class)

        # Add description if provided
        if description:
            bot_class.get_description = classmethod(lambda cls: description)

        return bot_class

    return decorator


def register_config(bot_type: str):
    """
    Decorator to register a configuration class for a bot type

    Args:
        bot_type: String identifier for the bot
    """

    def decorator(config_class) -> Any:
        ConfigRegistry.register_config(bot_type, config_class)
        return config_class

    return decorator
