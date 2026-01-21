import time
from src.bot.framework.bot_factory import BotFactory
from src.bot.framework.bot_selector import ConsoleBotSelector
from src.bot.bots.fishing import FishingBot
from src.bot.bots.mining import MiningBot
from src.bot.core.game.hotkeys import Hotkeys
from src.bot.utils.logger import log


def main():
    """Main entry point with bot selection"""

    # Get available bots from factory
    available_bots = BotFactory.get_available_bots()

    if not available_bots:
        log("[ERROR] No bot types available!")
        return

    # Get bot descriptions
    descriptions = BotFactory.get_bot_descriptions()

    # Create bot selector
    selector = ConsoleBotSelector(available_bots, descriptions)

    # Let user select bot type
    selected_bot_type = selector.select_bot()

    # Get bot configuration
    bot_config_dict = selector.get_bot_config(selected_bot_type)

    # Create bot instance
    bot = BotFactory.create_bot(selected_bot_type, bot_config_dict)

    # Setup hotkeys
    hotkeys = Hotkeys(bot)

    # Start the bot
    bot.start()

    log(f"[INFO] Press '7' to start the bot.")

    while not bot.is_stopped():
        if not hotkeys.paused:
            bot.update()

        time.sleep(0.1)

    log("[INFO] Bot finished.")


if __name__ == "__main__":
    main()
