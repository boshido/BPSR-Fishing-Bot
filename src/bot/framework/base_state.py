from abc import ABC, abstractmethod
from typing import Any
from .state_type import StateType


class BaseState(ABC):
    """Abstract base class for all bot states"""

    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config
        self.detector = bot.detector
        self.controller = bot.controller

    @abstractmethod
    def handle(self, screen: Any) -> StateType:
        """
        Handle the current state and return the next state

        Args:
            screen: Screen capture data

        Returns:
            StateType: The next state to transition to
        """
        pass

    @abstractmethod
    def get_state_type(self) -> StateType:
        """Return the state type identifier"""
        pass

    def enter(self) -> None:
        """Called when entering this state (optional override)"""
        pass

    def exit(self) -> None:
        """Called when exiting this state (optional override)"""
        pass

    def get_timeout_limit(self) -> float:
        """Return timeout limit for this state (optional override)"""
        return None
