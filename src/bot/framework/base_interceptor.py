from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseInterceptor(ABC):
    """Abstract base class for all bot interceptors"""

    def __init__(self, bot, priority: int = 0):
        self.bot = bot
        self.priority = priority  # Higher priority = checked first
        self.enabled = True

    @abstractmethod
    def check(self, screen: Any) -> bool:
        """
        Check if interceptor condition is met

        Args:
            screen: Screen capture data

        Returns:
            bool: True if condition is met
        """
        pass

    @abstractmethod
    def execute(self, screen: Any) -> Optional[Any]:
        """
        Execute interceptor action when condition is met

        Args:
            screen: Screen capture data

        Returns:
            Optional result or None
        """
        pass

    def intercept(self, screen: Any) -> Optional[Any]:
        """Main interception method"""
        if not self.enabled:
            return None

        if self.check(screen):
            return self.execute(screen)
        return None

    def enable(self) -> None:
        """Enable this interceptor"""
        self.enabled = True

    def disable(self) -> None:
        """Disable this interceptor"""
        self.enabled = False

    def set_priority(self, priority: int) -> None:
        """Set interceptor priority"""
        self.priority = priority
