# יצירת חלון הגרפים עם PySide6 ו-Matplotlib
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class GraphWindow(QWidget):
    # אתחול חלון הגרפים
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.setupUI()

    # בניית ממשק המשתמש
    def setupUI(self):
        self.setWindowTitle("Heat Transfer Graphs")
        self.resize(900, 520)

        # יצירת אזור הגרף
        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.ax = self.figure.add_subplot(111)

        # הגדרת כותרות הצירים
        self.ax.set_title("Temperature vs. Time")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Temperature (°C)")
        self.ax.grid(True)

        # יצירת כותרת אזור הבקרה
        self.controls_title = QLabel("Graph Controls")
        self.controls_title.setFixedSize(170, 30)
        self.controls_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # יצירת רשימה לבחירת הגוף
        self.body_select_label = QLabel("Select Body")
        self.body_select_label.setFixedSize(170, 24)

        self.body_selector = QComboBox()
        self.body_selector.setFixedSize(170, 32)
        self.body_selector.addItems(["Body 1", "Body 2"])

        # יצירת כפתור שרטוט
        self.draw_button = QPushButton("Draw")
        self.draw_button.setFixedSize(170, 36)

        # יצירת כפתור ניקוי
        self.clear_button = QPushButton("Clear")
        self.clear_button.setFixedSize(170, 36)

        # יצירת כפתור ייצוא נתונים
        self.export_button = QPushButton("Export to CSV")
        self.export_button.setFixedSize(170, 36)

        # סידור אזור הבקרה בצד ימין
        controls_layout = QVBoxLayout()
        controls_layout.setSpacing(12)
        controls_layout.addWidget(self.controls_title)
        controls_layout.addWidget(self.body_select_label)
        controls_layout.addWidget(self.body_selector)
        controls_layout.addSpacing(12)
        controls_layout.addWidget(self.draw_button)
        controls_layout.addWidget(self.clear_button)
        controls_layout.addWidget(self.export_button)
        controls_layout.addStretch()

        # סידור הרכיבים בחלון
        main_layout = QHBoxLayout()
        main_layout.setSpacing(16)
        main_layout.addWidget(self.canvas, 1)
        main_layout.addLayout(controls_layout)
        self.setLayout(main_layout)


# הפעלת חלון הגרפים לבדיקה ישירה
if __name__ == "__main__":
    app = QApplication()
    window = GraphWindow()
    window.show()
    app.exec()
