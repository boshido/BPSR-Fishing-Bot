from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class BotSelector(ABC):
    """Abstract interface for bot selection"""

    @abstractmethod
    def get_available_bots(self) -> List[str]:
        """Get list of available bot types"""
        pass

    @abstractmethod
    def select_bot(self) -> str:
        """Prompt user to select a bot type"""
        pass

    @abstractmethod
    def get_bot_config(self, bot_type: str) -> Dict[str, Any]:
        """Get configuration for selected bot"""
        pass


class ConsoleBotSelector(BotSelector):
    """Console-based bot selector"""

    def __init__(self, available_bots: List[str], descriptions: Dict[str, str] = None):
        self.available_bots = available_bots
        self.descriptions = descriptions or {}

    def get_available_bots(self) -> List[str]:
        return self.available_bots

    def select_bot(self) -> str:
        print("\n🤖 Available Bot Types:")
        for i, bot_type in enumerate(self.available_bots, 1):
            description = self.descriptions.get(bot_type, f"{bot_type} bot")
            print(f"  {i}. {bot_type} - {description}")

        while True:
            try:
                choice = input(f"\nSelect bot (1-{len(self.available_bots)}): ")
                index = int(choice) - 1
                if 0 <= index < len(self.available_bots):
                    selected_bot = self.available_bots[index]
                    print(f"✅ Selected: {selected_bot}")
                    return selected_bot
                else:
                    print("❌ Invalid selection. Please try again.")
            except ValueError:
                print("❌ Please enter a valid number.")

    def get_bot_config(self, bot_type: str) -> Dict[str, Any]:
        """Simple console config (can be extended)"""
        print(f"\n⚙️ {bot_type.title()} Bot Configuration:")
        print("Press Enter to use default values.")

        config = {}

        # Ask for common settings
        debug_input = input("Enable debug mode? (y/N): ").lower().strip()
        config["debug_mode"] = debug_input == "y"

        fps_input = input("Target FPS (0 for unlimited): ").strip()
        config["target_fps"] = int(fps_input) if fps_input.isdigit() else 0

        delay_input = input("Default delay in seconds (0.5): ").strip()
        config["default_delay"] = float(delay_input) if delay_input else 0.5

        return config


class FileBasedBotSelector(BotSelector):
    """File-based bot selector using config files"""

    def __init__(
        self, config_file: str = "bot_config.json", available_bots: List[str] = None
    ):
        self.config_file = config_file
        self.available_bots = available_bots or ["fishing"]
        self.config_data = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        try:
            import json

            with open(self.config_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            return {"selected_bot": "fishing", "configs": {}}

    def _save_config(self) -> None:
        """Save configuration to file"""
        try:
            import json

            with open(self.config_file, "w") as f:
                json.dump(self.config_data, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save config to {self.config_file}: {e}")

    def get_available_bots(self) -> List[str]:
        return self.available_bots

    def select_bot(self) -> str:
        """Use configured bot or return default"""
        bot_type = self.config_data.get("selected_bot")
        if bot_type and bot_type in self.available_bots:
            print(f"🤖 Using configured bot: {bot_type}")
            return bot_type
        return "fishing"  # Default

    def get_bot_config(self, bot_type: str) -> Dict[str, Any]:
        return self.config_data.get("configs", {}).get(bot_type, {})

    def set_selected_bot(self, bot_type: str) -> None:
        """Set the selected bot type"""
        self.config_data["selected_bot"] = bot_type
        self._save_config()

    def set_bot_config(self, bot_type: str, config: Dict[str, Any]) -> None:
        """Set configuration for a bot type"""
        if "configs" not in self.config_data:
            self.config_data["configs"] = {}
        self.config_data["configs"][bot_type] = config
        self._save_config()
