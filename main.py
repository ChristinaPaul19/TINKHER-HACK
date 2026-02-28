import sys
import random
from tracking.window_tracker import WindowTracker
from tracking.input_tracker import InputTracker
from engine.gamification import Gamification
from database.db_manager import init_db, log_session, get_today_stats
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from engine.achievements import Achievements
from matplotlib.figure import Figure
from PyQt6.QtWidgets import QTabWidget
from PyQt6.QtGui import QPixmap 

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QWidget
)
from PyQt6.QtCore import Qt, QTimer


class NeuroFocusApp(QMainWindow):
    def __init__(self):
        super().__init__()
        init_db()
        # initialize window tracker after base class initialization
        self.window_tracker = WindowTracker()
        self.input_tracker = InputTracker()
        self.game = Gamification()
        self.setWindowTitle("NeuroFocus")
        self.setMinimumSize(800, 500)
        self.streak = 0

        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.achievements = Achievements()

        # Layout
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        tabs = QTabWidget()
        layout.addWidget(tabs)

        # Dashboard tab container
        dash = QWidget()
        dash_layout = QVBoxLayout(dash)
        # move: title, timer_label, focus_label, avatar_label, canvas into dash_layout
        tabs.addTab(dash, "Dashboard")

        # Analytics tab
        analytics = QWidget()
        analytics_layout = QVBoxLayout(analytics)
        self.analytics_label = QLabel("Loading analytics...")
        analytics_layout.addWidget(self.analytics_label)
        tabs.addTab(analytics, "Analytics")

        # Achievements tab
        achievements_tab = QWidget()
        ach_layout = QVBoxLayout(achievements_tab)
        self.achievement_label = QLabel("No achievements yet")
        ach_layout.addWidget(self.achievement_label)
        tabs.addTab(achievements_tab, "Achievements")

        # Avatar label
        self.avatar_label = QLabel()
        self.avatar_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.avatar_label)

        self.update_avatar("neutral")

        # Tracking variables
        self.session_seconds = 0
        # Focus history
        self.focus_history = []

        # Create matplotlib figure
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        # Title
        title = QLabel("NeuroFocus Dashboard")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 24px;")
        layout.addWidget(title)

        # Focus score label
        self.focus_label = QLabel("Focus Score: 100")
        self.focus_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.focus_label.setStyleSheet("font-size: 20px;")
        layout.addWidget(self.focus_label)

        # Achievements display (on dashboard)
        self.achievements_label = QLabel("")
        self.achievements_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.achievements_label.setStyleSheet("font-size: 14px; color: #00ff00;")
        layout.addWidget(self.achievements_label)

        # Timer (updates every 2 seconds)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_focus)
        self.timer.start(3000)

    def update_focus(self):
        self.window_tracker.update()

        switches = self.window_tracker.get_switch_count()
        inactivity = self.input_tracker.inactivity_time()
       
        score = 100

        # Penalize window switching
        score -= switches * 5

        # Penalize inactivity
        if inactivity > 30:
            score -= 20

        score = max(0, score)
        # Update avatar state
        if score > 70:
            self.update_avatar("happy")
        elif score > 40:
            self.update_avatar("neutral")
        else:
            self.update_avatar("sad")

        # Add XP and compute level/xp before logging
        self.game.add_xp(score)
        level = self.game.get_level()
        xp = self.game.get_xp()

        # Increment session timer (2 seconds per tick)
        self.session_seconds += 2

        # Log every 10 seconds
        if self.session_seconds % 10 == 0:
            log_session(score, xp, level, self.session_seconds)

        self.focus_label.setText(
            f"Focus: {score} | Level: {level} | XP: {xp}"
        )
        # check for new achievements and show on dashboard
        unlocked = self.achievements.check(xp, level)
        if unlocked:
            self.achievements_label.setText("\n".join(unlocked))

        # Store history (keep last 20 values)
        self.focus_history.append(score)
        if len(self.focus_history) > 20:
            self.focus_history.pop(0)

        self.update_graph()

        avg_focus, max_xp, max_level = get_today_stats()
        self.analytics_label.setText(
             f"Today Avg Focus: {int(avg_focus or 0)}\nMax XP: {int(max_xp or 0)}\nMax Level: {int(max_level or 1)}"
        )
        if score > 70:
            self.streak += 1
        else:
            self.streak = 0
        f"Streak: {self.streak}"
        if switches > 10:
            self.focus_label.setText("⚠️ Too Many App Switches!")
        unlocked = self.achievements.check(xp, level)
        if unlocked:
            self.achievement_label.setText("\n".join(unlocked))
    def closeEvent(self, event):
        # Save final session data when app closes
        log_session(
            0,
            self.game.get_xp(),
            self.game.get_level(),
            self.session_seconds
        )
        event.accept()
    def update_graph(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.plot(self.focus_history)
        ax.set_title("Focus History")
        ax.set_ylim(0, 100)
        self.canvas.draw()
    def update_avatar(self, state):
        if state == "happy":
            path = "assets/avatar_happy.png.png"
        elif state == "sad":
            path = "assets/avatar_sad.png.png"
        else:
            path = "assets/avatar_neutral.png.png"

        pixmap = QPixmap(path)
        self.avatar_label.setPixmap(pixmap.scaled(150, 150))
def main():
    app = QApplication(sys.argv)
    window = NeuroFocusApp()
    window.show()
    sys.exit(app.exec())
    app.setStyleSheet("""
    QWidget {
    background-color: #121212;
    color: white;
    }
    QLabel {
    font-family: Arial;
    }
    """)


if __name__ == "__main__":
    main()