import keyboard
import multiprocessing
from ...utils.logger import log
from ...utils.roi_visualizer import main as show_roi_visualizer

class Hotkeys:
    def __init__(self, bot):
        self.bot = bot
        self.paused = True
        self.visualizer_process = None
        self.return_to_menu = False
        self._registered_keys = []
        self._register_hotkeys()

    def _register_hotkeys(self):
        # Clear any existing hotkeys first
        self.unregister_all()
        
        keyboard.add_hotkey('7', self._toggle_pause)
        keyboard.add_hotkey('8', self._stop)
        keyboard.add_hotkey('9', self._toggle_visualizer)
        keyboard.add_hotkey('0', self._return_to_menu)
        
        self._registered_keys = ['7', '8', '9', '0']
        log("[INFO] ✅ Hotkeys registered: '7' (Pause/Resume), '8' (Exit), '0' (Return to Menu), '9' (ROI Visualizer)")

    def _toggle_pause(self):
        self.paused = not self.paused
        status = "PAUSED" if self.paused else "RUNNING"
        log(f"[HOTKEY] Bot {status}.")

    def _stop(self):
        log("[HOTKEY] Stopping the bot...")
        if self.visualizer_process and self.visualizer_process.is_alive():
            self.visualizer_process.terminate()
        self.bot.stop()

    def _return_to_menu(self):
        log("[HOTKEY] Returning to main menu...")
        self.return_to_menu = True

    def unregister_all(self):
        """Unregister all hotkeys"""
        for key in self._registered_keys:
            try:
                keyboard.remove_hotkey(key)
            except:
                pass  # Key might not be registered anymore
        self._registered_keys = []

    def _toggle_visualizer(self):
        if self.visualizer_process and self.visualizer_process.is_alive():
            log("[HOTKEY] Closing the ROI visualizer.")
            self.visualizer_process.terminate()
            self.visualizer_process = None
        else:
            log("[HOTKEY] Opening the ROI visualizer.")
            # Runs the visualizer in a separate process so it doesn’t block the main UI
            self.visualizer_process = multiprocessing.Process(target=show_roi_visualizer, daemon=True)
            self.visualizer_process.start()

    def wait_for_exit(self):
        """Keeps the script running until the exit hotkey is pressed."""
        keyboard.wait('8')

    def cleanup(self):
        """Clean up hotkeys and visualizer"""
        self.unregister_all()
        if self.visualizer_process and self.visualizer_process.is_alive():
            self.visualizer_process.terminate()
            self.visualizer_process = None