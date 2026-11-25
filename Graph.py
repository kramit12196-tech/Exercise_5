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
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from Export import ExportWindow

class GraphWindow(QWidget):
    # אתחול חלון הגרפים
    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.export_window = ExportWindow(self.main_window, self)
        self.setupUI()

    # בניית ממשק המשתמש
    def setupUI(self):
        self.setWindowTitle("Heat Transfer Graphs")
        self.resize(1200, 800)

        # יצירת אזור הגרף
        self.figure = Figure()
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.ax = self.figure.add_subplot(111)

        # הגדרת כותרות הצירים
        self.ax.set_title("Temperature vs. Time")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Temperature (°C)")
        self.ax.grid(True)

        # יצירת כותרת וטבלת פרמטרי הסימולציה
        self.parameters_title = QLabel("Simulation Parameters")
        self.parameters_table = QTableWidget(10, 2)
        self.parameters_table.setHorizontalHeaderLabels(["Category", "Parameter"])
        self.parameters_table.setColumnWidth(0, 90)
        self.parameters_table.setColumnWidth(1, 280)
        self.parameters_table.setFixedHeight(335)
        self.parameters_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )

        # הגדרת קטגוריות ומיזוג תאים אנכי בעמודת הקטגוריה
        general_item = QTableWidgetItem("General")
        general_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.parameters_table.setItem(0, 0, general_item)
        self.parameters_table.setSpan(0, 0, 2, 1)

        body1_item = QTableWidgetItem("Body 1")
        body1_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.parameters_table.setItem(2, 0, body1_item)
        self.parameters_table.setSpan(2, 0, 4, 1)

        body2_item = QTableWidgetItem("Body 2")
        body2_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.parameters_table.setItem(6, 0, body2_item)
        self.parameters_table.setSpan(6, 0, 4, 1)

        # מילוי שמות הפרמטרים בעמודה השנייה
        parameter_names = [
            "Thermal Conductance (W/°C)",
            "Simulation Duration (s)",
            "Material",
            "Initial Temperature (°C)",
            "Mass (kg)",
            "Specific Heat Capacity (J/(kg·°C))",
            "Material",
            "Initial Temperature (°C)",
            "Mass (kg)",
            "Specific Heat Capacity (J/(kg·°C))",
        ]
        for row in range(len(parameter_names)):
            self.parameters_table.setItem(
                row, 1, QTableWidgetItem(parameter_names[row])
            )

        # סידור אזור הגרף והטבלה בצד שמאל
        left_layout = QVBoxLayout()
        left_layout.setSpacing(10)
        left_layout.addWidget(self.canvas, 1)
        left_layout.addWidget(self.parameters_title)
        left_layout.addWidget(self.parameters_table)

        # יצירת כותרת אזור הבקרה
        self.controls_title = QLabel("Graph Controls")
        self.controls_title.setFixedSize(200, 30)
        self.controls_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # יצירת רשימה לבחירת הסימולציה
        self.simulation_select_label = QLabel("Select Simulation")
        self.simulation_select_label.setFixedSize(200, 24)

        self.simulation_selector = QComboBox()
        self.simulation_selector.setFixedSize(200, 32)

        # יצירת רשימה לבחירת הגוף
        self.body_select_label = QLabel("Select Body")
        self.body_select_label.setFixedSize(200, 24)

        self.body_selector = QComboBox()
        self.body_selector.setFixedSize(200, 32)
        self.body_selector.addItems(["Body 1", "Body 2", "Both Bodies"])
        self.body_selector.setCurrentText("Both Bodies")

        # יצירת כפתור שרטוט
        self.draw_button = QPushButton("Draw")
        self.draw_button.setFixedSize(200, 36)
        self.draw_button.setEnabled(False)
        self.draw_button.clicked.connect(self.draw_graph)

        # יצירת כפתור ניקוי
        self.clear_button = QPushButton("Clear")
        self.clear_button.setFixedSize(200, 36)
        self.clear_button.clicked.connect(self.clear_graph)

        # יצירת כפתור ייצוא נתונים
        self.export_button = QPushButton("Export Data")
        self.export_button.setFixedSize(200, 36)
        self.export_button.clicked.connect(self.open_export_window)

        # סידור אזור הבקרה בצד ימין
        controls_layout = QVBoxLayout()
        controls_layout.setSpacing(10)
        controls_layout.addWidget(self.controls_title)
        controls_layout.addWidget(self.simulation_select_label)
        controls_layout.addWidget(self.simulation_selector)
        controls_layout.addSpacing(6)
        controls_layout.addWidget(self.body_select_label)
        controls_layout.addWidget(self.body_selector)
        controls_layout.addSpacing(16)
        controls_layout.addWidget(self.draw_button)
        controls_layout.addWidget(self.clear_button)
        controls_layout.addWidget(self.export_button)
        controls_layout.addStretch()

        # סידור הרכיבים בחלון
        main_layout = QHBoxLayout()
        main_layout.setSpacing(16)
        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(controls_layout)
        self.setLayout(main_layout)

    # שרטוט הסימולציה והגופים שנבחרו
    def draw_graph(self):
        if self.main_window is None:
            return

        index = self.simulation_selector.currentIndex()
        if index < 0 or index >= len(self.main_window.simulation_history):
            return

        # קריאת נתוני הסימולציה והגוף שנבחרו
        simulation = self.main_window.simulation_history[index]
        number = simulation["number"]
        material1 = simulation["material1"]
        material2 = simulation["material2"]
        selected_body = self.body_selector.currentText()

        # ניקוי הגרף והגדרת כותרות ורשת
        self.ax.clear()
        self.ax.set_title(f"Simulation {number} - Temperature vs. Time")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Temperature (°C)")
        self.ax.grid(True)

        # שרטוט הגוף הראשון
        if selected_body == "Body 1" or selected_body == "Both Bodies":
            self.ax.plot(
                simulation["time"],
                simulation["temperature1"],
                label=f"Body 1 ({material1})",
                color="red",
                linewidth=2,
            )

        # שרטוט הגוף השני
        if selected_body == "Body 2" or selected_body == "Both Bodies":
            self.ax.plot(
                simulation["time"],
                simulation["temperature2"],
                label=f"Body 2 ({material2})",
                color="blue",
                linewidth=2,
            )

        # הצגת המקרא ועדכון תצוגת הגרף
        self.ax.legend()
        self.canvas.draw()

    # ניקוי הגרף המוצג בלבד
    def clear_graph(self):
        self.ax.clear()
        self.ax.set_title("Temperature vs. Time")
        self.ax.set_xlabel("Time (s)")
        self.ax.set_ylabel("Temperature (°C)")
        self.ax.grid(True)
        self.canvas.draw()

    # עדכון רשימת הסימולציות והטבלה
    def refresh_simulations(self):
        if self.main_window is None:
            return

        # הוספת סימולציות חדשות בלבד לרשימת הבחירה
        current_count = self.simulation_selector.count()
        total_count = len(self.main_window.simulation_history)

        for i in range(current_count, total_count):
            number = self.main_window.simulation_history[i]["number"]
            self.simulation_selector.addItem(f"Simulation {number}")

        # הפעלת כפתור השרטוט ובחירת הסימולציה החדשה ביותר
        if total_count > 0:
            self.draw_button.setEnabled(True)
            if total_count > current_count:
                self.simulation_selector.setCurrentIndex(total_count - 1)
        else:
            self.draw_button.setEnabled(False)

        # עדכון טבלת הפרמטרים עבור כל הסימולציות
        self.update_parameters_table()

    # עדכון טבלת הפרמטרים עבור כל הסימולציות שהסתיימו
    def update_parameters_table(self):
        if self.main_window is None:
            return

        simulations = self.main_window.simulation_history

        # הגדרת מספר העמודות וכותרותיהן
        self.parameters_table.setColumnCount(len(simulations) + 2)

        headers = ["Category", "Parameter"]
        for simulation in simulations:
            headers.append(f"Simulation {simulation['number']}")
        self.parameters_table.setHorizontalHeaderLabels(headers)

        # מילוי נתוני כל הסימולציות בעמודות הטבלה
        for i in range(len(simulations)):
            simulation = simulations[i]
            column = i + 2
            self.parameters_table.setColumnWidth(column, 120)

            values = [
                f"{simulation['conductance']:.2f}",
                f"{simulation['duration']:.2f}",
                simulation["material1"],
                f"{simulation['initial_temp1']:.2f}",
                f"{simulation['mass1']:.2f}",
                f"{simulation['heat_capacity1']:.2f}",
                simulation["material2"],
                f"{simulation['initial_temp2']:.2f}",
                f"{simulation['mass2']:.2f}",
                f"{simulation['heat_capacity2']:.2f}",
            ]

            for row in range(len(values)):
                item = QTableWidgetItem(values[row])
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.parameters_table.setItem(row, column, item)

    # פתיחת חלון ייצוא הנתונים
    def open_export_window(self):
        self.export_window.refresh_options()
        self.export_window.show()

# הפעלת חלון הגרפים לבדיקה ישירה
if __name__ == "__main__":
    app = QApplication()
    window = GraphWindow()
    window.show()
    app.exec()
