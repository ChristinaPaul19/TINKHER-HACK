import ctypes
import ctypes.wintypes
import time


class WindowTracker:
    def __init__(self):
        self.current_window = None
        self.start_time = time.time()
        self.switch_count = 0

    def get_active_window(self):
        user32 = ctypes.windll.user32
        hwnd = user32.GetForegroundWindow()
        length = user32.GetWindowTextLengthW(hwnd) + 1
        buf = ctypes.create_unicode_buffer(length)
        user32.GetWindowTextW(hwnd, buf, length)
        return buf.value

    def update(self):
        active = self.get_active_window()

        if self.current_window is None:
            self.current_window = active
            return

        if active != self.current_window:
            self.switch_count += 1
            self.current_window = active

    def get_switch_count(self):
        return self.switch_count