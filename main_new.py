import time
from src.bot.framework.bot_factory import BotFactory
from src.bot.framework.bot_selector import ConsoleBotSelector
from src.bot.bots.fishing import FishingBot
from src.bot.bots.mining import MiningBot
from src.bot.core.game.hotkeys import Hotkeys
from src.bot.utils.logger import log
from src.bot.config.fishing_config import FishingConfig
from src.bot.config.mining_config import MiningConfig


def show_bot_menu():
    """Display interactive bot selection menu"""
    available_bots = BotFactory.get_available_bots()

    if not available_bots:
        log("[ERROR] No bot types available!")
        return None, None

    descriptions = BotFactory.get_bot_descriptions()

    while True:
        print("\n" + "="*50)
        print("🤖 BOT SELECTION MENU")
        print("="*50)
        print("Available Bots:")
        for i, bot_type in enumerate(available_bots, 1):
            description = descriptions.get(bot_type, f"{bot_type} bot")
            print(f"  {i}. {bot_type} - {description}")
        print("  0. Exit")
        print("="*50)

        try:
            choice = input(f"\nSelect bot (0-{len(available_bots)}): ").strip()
            if choice == '0':
                print("👋 Goodbye!")
                return None, None

            choice_num = int(choice)
            if 1 <= choice_num <= len(available_bots):
                selected_bot_type = available_bots[choice_num - 1]
                print(f"✅ Selected: {selected_bot_type}")

                # Create proper config object based on bot type
                if selected_bot_type == "fishing":
                    bot_config = FishingConfig()
                elif selected_bot_type == "mining":
                    bot_config = MiningConfig()
                else:
                    print(f"[ERROR] Unknown bot type: {selected_bot_type}")
                    continue

                # Set some default values
                bot_config.debug_mode = False
                bot_config.target_fps = 0
                bot_config.default_delay = 0.5

                return selected_bot_type, bot_config
            else:
                print("❌ Invalid selection. Please try again.")
        except ValueError:
            print("❌ Please enter a valid number.")
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            return None, None


def show_runtime_menu(current_bot_type, bot, hotkeys):
    """Show runtime menu for bot management"""
    print(f"\n🎮 Currently running: {current_bot_type}")
    print("Runtime Options:")
    print("  1. Switch Bot")
    print("  2. Resume/Pause (if hotkeys available)")
    print("  3. Show Statistics")
    print("  Press '0' anytime to return to menu, '8' to exit")

    try:
        choice = input("Select option (1-3): ").strip()
        return choice
    except KeyboardInterrupt:
        return "0"


def create_bot_instance(bot_type, bot_config):
    """Create a bot instance"""
    return BotFactory.create_bot(bot_type, bot_config)


def run_bot_with_menu(bot, hotkeys, bot_type):
    """Run bot and return when interrupted for menu"""
    log(f"[INFO] Bot running. Press '7' to pause/resume, '0' to return to menu, '8' to exit, '9' for ROI visualizer.")

    iteration_count = 0
    while not bot.is_stopped():
        if hotkeys is not None:
            if not hotkeys.paused:
                bot.update()
            # Check if return to menu was requested
            if hasattr(hotkeys, 'return_to_menu') and hotkeys.return_to_menu:
                log("[INFO] Returning to main menu...")
                hotkeys.return_to_menu = False  # Reset the flag
                return True
        else:
            bot.update()

        iteration_count += 1
        time.sleep(0.1)

        # Show status every 1000 iterations (less spam)
        if iteration_count % 1000 == 0:
            log(f"[INFO] Bot running... ({iteration_count} cycles)")

    return False


def main():
    """Main entry point with bot selection"""

    # Initial bot selection
    selected_bot_type, bot_config = show_bot_menu()
    if selected_bot_type is None:
        return

    # Create bot instance
    bot = create_bot_instance(selected_bot_type, bot_config)

    # Setup hotkeys with error handling
    hotkeys = None
    try:
        hotkeys = Hotkeys(bot)
        log(f"[INFO] Hotkeys registered: '7' (Pause/Resume), '8' (Exit), '0' (Return to Menu), '9' (ROI Visualizer)")
    except Exception as e:
        log(f"[WARNING] Could not initialize hotkeys: {e}")
        log(f"[WARNING] Bot will start automatically in 3 seconds...")
        time.sleep(3)

    # Start the bot
    bot.start()

    # Main runtime loop
    while True:
        # Run bot until interrupted
        interrupted = run_bot_with_menu(bot, hotkeys, selected_bot_type)

        if interrupted:
            # Return to bot selection menu
            log("[INFO] Returning to bot selection...")
            
            # Clean up current bot and hotkeys
            if hotkeys is not None:
                hotkeys.cleanup()
            bot = None
            
            selected_bot_type, bot_config = show_bot_menu()
            if selected_bot_type is None:
                break
            
            # Create new bot instance
            bot = create_bot_instance(selected_bot_type, bot_config)
            
            # Re-setup hotkeys if available
            if hotkeys is not None:
                try:
                    hotkeys = Hotkeys(bot)
                    log(f"[INFO] Hotkeys registered for new bot")
                except Exception as e:
                    log(f"[WARNING] Could not re-initialize hotkeys: {e}")
                    hotkeys = None
            
            bot.start()
            continue
        else:
            # Bot was not interrupted, check if it stopped naturally
            if bot.is_stopped():
                log("[INFO] Bot stopped naturally.")
                break

    # Final cleanup
    if hotkeys is not None:
        hotkeys.cleanup()
    
    log("[INFO] Bot finished.")


if __name__ == "__main__":
    main()
