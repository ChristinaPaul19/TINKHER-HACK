class Achievements:
    def check(self, xp, level):
        unlocked = []
        if xp >= 100:
            unlocked.append("💪 100 XP Achieved")
        if level >= 5:
            unlocked.append("🚀 Level 5 Reached")
        return unlocked