import math

class FocusEngine:
    def calculate_score(self, window_switches, inactivity, gaze, emotion):
        score = 100

        if window_switches > 5:
            score -= 20

        if inactivity > 60:
            score -= 15

        if gaze != "center":
            score -= 10

        if emotion in ["sad", "angry"]:
            score -= 10

        return max(0, min(100, score))