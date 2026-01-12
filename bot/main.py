import time

from bot.src.fishbot.core.fishing_bot import FishingBot
from bot.src.fishbot.core.game import Hotkeys
from bot.src.fishbot.utils import log


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