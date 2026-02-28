import math


class Gamification:
    def __init__(self):
        self.xp = 0

    def add_xp(self, focus_score):
        # XP gained based on focus
        if focus_score > 70:
            self.xp += 5
        elif focus_score > 50:
            self.xp += 2

    def get_level(self):
        return int(math.sqrt(self.xp / 10)) + 1

    def get_xp(self):
        return self.xp