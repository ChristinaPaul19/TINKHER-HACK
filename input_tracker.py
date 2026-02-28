from pynput import mouse, keyboard
import time


class InputTracker:
    def __init__(self):
        self.click_count = 0
        self.key_count = 0
        self.last_input_time = time.time()

        # Start listeners
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press)

        self.mouse_listener.start()
        self.keyboard_listener.start()

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.click_count += 1
            self.last_input_time = time.time()

    def on_press(self, key):
        self.key_count += 1
        self.last_input_time = time.time()

    def inactivity_time(self):
        return time.time() - self.last_input_time

    def get_click_count(self):
        return self.click_count

    def get_key_count(self):
        return self.key_count