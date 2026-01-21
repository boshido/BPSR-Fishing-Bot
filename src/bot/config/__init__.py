from .bot_config import BotConfig
from .base_config import BaseConfig
from .fishing_config import FishingConfig
from .config_registry import ConfigRegistry
from .paths import PACKAGE_ROOT, ASSETS_PATH, TEMPLATES_PATH

# Register configuration classes
ConfigRegistry.register_config("fishing", FishingConfig)


class Config:
    """Legacy Config class for backward compatibility"""

    def __init__(self):
        self.bot = BotConfig()

        self.paths = {
            "package_root": PACKAGE_ROOT,
            "assets": ASSETS_PATH,
            "templates": TEMPLATES_PATH,
        }

    def get_template_path(self, template_name):
        filename = self.bot.detection.templates.get(template_name)

        if filename:
            return self.paths["templates"] / filename
        return None
