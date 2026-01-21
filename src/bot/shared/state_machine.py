import time
from typing import Optional, Dict, Any
from ..framework.state_type import StateType
from ..utils.logger import log


class StateMachine:
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config
        self.states = {}
        self.current_state_name: Optional[StateType] = None
        self.current_state = None
        self.state_start_time = None

    def add_state(self, name: StateType, state_instance) -> None:
        """Add a state to the state machine"""
        self.states[name] = state_instance

    def set_state(self, new_state_name: StateType, force: bool = False) -> None:
        """Set the current state"""
        if not force and new_state_name == self.current_state_name:
            return

        if new_state_name not in self.states:
            log(f"[ERROR] Attempted to switch to unknown state: {new_state_name}")
            return

        # Exit current state if it exists
        if self.current_state:
            self.current_state.exit()

        # Log state transition
        if self.current_state_name is None:
            log(f"[INFO] Starting state machine in: {new_state_name.name}")
        elif new_state_name != self.current_state_name:
            log(
                f"[INFO] Changing state: {self.current_state_name.name} -> {new_state_name.name}"
            )
        elif force:
            log(f"[INFO] Forcing state reset: {new_state_name.name}")

        self.current_state_name = new_state_name
        self.current_state = self.states[self.current_state_name]
        self.state_start_time = time.time()

        # Enter new state
        self.current_state.enter()

    def _check_state_timeout(self) -> bool:
        """Check if current state has timed out"""
        timeout_limit = None

        # Try to get timeout from state instance
        if self.current_state and hasattr(self.current_state, "get_timeout_limit"):
            timeout_limit = self.current_state.get_timeout_limit()

        # Fallback to config-based timeouts for backward compatibility
        if (
            timeout_limit is None
            and hasattr(self.config, "bot")
            and hasattr(self.config.bot, "state_timeouts")
        ):
            state_name_str = (
                self.current_state_name.name if self.current_state_name else None
            )
            if state_name_str in self.config.bot.state_timeouts:
                timeout_limit = self.config.bot.state_timeouts[state_name_str]

        if not timeout_limit:
            return False

        elapsed_time = time.time() - self.state_start_time
        if elapsed_time > timeout_limit:
            log(
                f"[TIMEOUT] 🚨 State '{self.current_state_name.name}' exceeded {timeout_limit}s!"
            )
            log("[TIMEOUT] 🚨 Releasing controls and pressing 'ESC' to reset.")

            self.bot.controller.release_all_controls()
            self.bot.controller.press_key("esc")
            time.sleep(0.5)

            # Increment timeout stats if available
            if hasattr(self.bot, "stats"):
                self.bot.stats.increment("timeouts")

            # Reset to starting state
            self.set_state(StateType.STARTING, force=True)
            return True
        return False

    def handle(self, screen: Any) -> None:
        """Handle the current state"""
        if self._check_state_timeout():
            return

        if self.current_state:
            new_state_name = self.current_state.handle(screen)
            self.set_state(new_state_name)

    def get_current_state(self) -> Optional[StateType]:
        """Get the current state type"""
        return self.current_state_name

    def get_state_instance(self, state_type: StateType):
        """Get a specific state instance"""
        return self.states.get(state_type)
