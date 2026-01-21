import time
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from .state_type import StateType
from .base_interceptor import BaseInterceptor
from ..utils.logger import log


class BaseBot(ABC):
    """Abstract base class for all bot implementations"""

    def __init__(self, config):
        self.config = config
        self.log = log
        self._stopped = False

        # Core components (will be initialized after config is properly set up)
        self.detector = None
        self.controller = None
        self.state_machine = None

        # Interceptors
        self.interceptors: List[BaseInterceptor] = []

        # Performance settings
        self.target_delay = 0
        if hasattr(config, "bot") and hasattr(config.bot, "target_fps"):
            if config.bot.target_fps > 0:
                self.target_delay = 1.0 / config.bot.target_fps

        # Initialize bot-specific components
        self._initialize_components()
        self._register_states()

    @abstractmethod
    def get_bot_type(self) -> str:
        """Return the bot type identifier"""
        pass

    @abstractmethod
    def _initialize_components(self) -> None:
        """Initialize bot-specific components (interceptors, etc.)"""
        pass

    @abstractmethod
    def _register_states(self) -> None:
        """Register all states for this bot"""
        pass

    @abstractmethod
    def get_default_config(self) -> Dict[str, Any]:
        """Return default configuration for this bot type"""
        pass

    def start(self) -> None:
        """Start the bot"""
        self.log(f"[INFO] 🤖 {self.get_bot_type()} bot ready!")
        self._on_start()
        self._start_main_state()

    def update(self) -> None:
        """Main update loop"""
        if self._stopped:
            return

        loop_start = time.time()
        screen = self.detector.capture_screen()

        # Check interceptors first
        for interceptor in sorted(
            self.interceptors, key=lambda x: x.priority, reverse=True
        ):
            result = interceptor.intercept(screen)
            if result is not None:
                # Interceptor handled the event, continue to next frame
                break
        else:
            # No interceptor handled the event, process normally
            self.state_machine.handle(screen)

        if self.target_delay > 0:
            loop_time = time.time() - loop_start
            sleep_time = max(0, self.target_delay - loop_time)
            if sleep_time > 0:
                time.sleep(sleep_time)

    def stop(self) -> None:
        """Stop the bot"""
        if not self._stopped:
            self.log(f"[BOT] 🛑 Shutting down {self.get_bot_type()} bot...")
            self._stopped = True
            self._on_stop()

            try:
                self.controller.release_all_controls()
            except Exception as e:
                self.log(f"[ERROR] Failed to release controls: {e}")

    def is_stopped(self) -> bool:
        """Check if bot is stopped"""
        return self._stopped

    def add_interceptor(self, interceptor: BaseInterceptor) -> None:
        """Add an interceptor to the bot"""
        self.interceptors.append(interceptor)

    def remove_interceptor(self, interceptor: BaseInterceptor) -> None:
        """Remove an interceptor from the bot"""
        if interceptor in self.interceptors:
            self.interceptors.remove(interceptor)

    def _start_main_state(self) -> None:
        """Start the initial state (to be overridden by subclasses)"""
        pass

    def _on_start(self) -> None:
        """Called when bot starts (to be overridden by subclasses)"""
        pass

    def _on_stop(self) -> None:
        """Called when bot stops (to be overridden by subclasses)"""
        pass
