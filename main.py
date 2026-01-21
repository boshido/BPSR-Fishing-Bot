import time

from src.bot.core.fishing_bot import FishingBot
from src.bot.core.game.hotkeys import Hotkeys
from src.bot.utils.logger import log


def main():
    bot = FishingBot()
    hotkeys = Hotkeys(bot)

    bot.start()

    log("[INFO] Press '7' to start the bot.")

    while not bot.is_stopped():
        if not hotkeys.paused:
            bot.update()

        time.sleep(0.1)

    log("[INFO] Bot finished.")


if __name__ == "__main__":
    main()
