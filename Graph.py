# יצירת חלון הגרפים עם PySide6 ו-Matplotlib
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT,
)
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
        self.setObjectName("graphWindow")
        self.setWindowTitle("Heat Transfer Graphs")
        self.resize(1200, 880)

        # יצירת כרטיס הכותרת העליון
        self.header_card = QWidget()
        self.header_card.setObjectName("graphHeaderCard")

        self.header_title = QLabel("Heat Transfer Graphs")
        self.header_title.setObjectName("headerTitle")

        self.header_subtitle = QLabel("Simulation Results & Comparison")
        self.header_subtitle.setObjectName("headerSubtitle")

        header_text_layout = QVBoxLayout()
        header_text_layout.setContentsMargins(0, 0, 0, 0)
        header_text_layout.setSpacing(2)
        header_text_layout.addWidget(self.header_title)
        header_text_layout.addWidget(self.header_subtitle)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(18, 14, 18, 14)
        header_layout.addLayout(header_text_layout)
        header_layout.addStretch()
        self.header_card.setLayout(header_layout)

        # יצירת כרטיס הגרף בצד שמאל
        self.plot_card = QWidget()
        self.plot_card.setObjectName("graphPlotCard")

        self.plot_section_title = QLabel("Temperature Analysis")
        self.plot_section_title.setObjectName("sectionTitle")

        plot_divider = QWidget()
        plot_divider.setObjectName("dividerLine")
        plot_divider.setFixedHeight(1)

        # יצירת אזור הגרף, סרגל הניווט והגדרת עיצוב הצירים
        self.figure = Figure(figsize=(8, 3.3))
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.ax = self.figure.add_subplot(111)
        self.style_axes("Temperature vs. Time")

        self.toolbar = NavigationToolbar2QT(self.canvas, self)
        self.toolbar.setObjectName("graphToolbar")

        plot_card_layout = QVBoxLayout()
        plot_card_layout.setContentsMargins(16, 12, 16, 10)
        plot_card_layout.setSpacing(6)
        plot_card_layout.addWidget(self.plot_section_title)
        plot_card_layout.addWidget(plot_divider)
        plot_card_layout.addWidget(self.canvas, 1)
        plot_card_layout.addWidget(self.toolbar)
        self.plot_card.setLayout(plot_card_layout)

        # יצירת כרטיס הבקרה בצד ימין
        self.controls_card = QWidget()
        self.controls_card.setObjectName("graphControlsCard")
        self.controls_card.setFixedWidth(250)

        self.controls_title = QLabel("Graph Controls")
        self.controls_title.setObjectName("cardTitle")
        self.controls_title.setFixedHeight(28)
        self.controls_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        controls_divider = QWidget()
        controls_divider.setObjectName("dividerLine")
        controls_divider.setFixedHeight(1)

        # יצירת רשימה לבחירת הסימולציה
        self.simulation_select_label = QLabel("Select Simulation")
        self.simulation_select_label.setObjectName("secondaryLabel")
        self.simulation_select_label.setFixedSize(214, 20)

        self.simulation_selector = QComboBox()
        self.simulation_selector.setFixedSize(214, 34)

        # יצירת רשימה לבחירת הגוף
        self.body_select_label = QLabel("Select Body")
        self.body_select_label.setObjectName("secondaryLabel")
        self.body_select_label.setFixedSize(214, 20)

        self.body_selector = QComboBox()
        self.body_selector.setFixedSize(214, 34)
        self.body_selector.addItems(["Body 1", "Body 2", "Both Bodies"])
        self.body_selector.setCurrentText("Both Bodies")

        # יצירת כפתור שרטוט
        self.draw_button = QPushButton("Draw")
        self.draw_button.setObjectName("drawButton")
        self.draw_button.setFixedSize(214, 38)
        self.draw_button.setEnabled(False)
        self.draw_button.clicked.connect(self.draw_graph)

        # יצירת כפתור ניקוי
        self.clear_button = QPushButton("Clear")
        self.clear_button.setObjectName("graphSecondaryButton")
        self.clear_button.setFixedSize(214, 38)
        self.clear_button.clicked.connect(self.clear_graph)

        # יצירת כפתור ייצוא נתונים
        self.export_button = QPushButton("Export Data")
        self.export_button.setObjectName("graphSecondaryButton")
        self.export_button.setFixedSize(214, 38)
        self.export_button.clicked.connect(self.open_export_window)

        # סידור רכיבי הבקרה בתוך כרטיס הבקרה
        controls_layout = QVBoxLayout()
        controls_layout.setContentsMargins(18, 12, 18, 14)
        controls_layout.setSpacing(8)
        controls_layout.addWidget(self.controls_title)
        controls_layout.addWidget(controls_divider)
        controls_layout.addSpacing(4)
        controls_layout.addWidget(self.simulation_select_label)
        controls_layout.addWidget(self.simulation_selector)
        controls_layout.addSpacing(4)
        controls_layout.addWidget(self.body_select_label)
        controls_layout.addWidget(self.body_selector)
        controls_layout.addSpacing(10)
        controls_layout.addWidget(self.draw_button)
        controls_layout.addWidget(self.clear_button)
        controls_layout.addWidget(self.export_button)
        controls_layout.addStretch()
        self.controls_card.setLayout(controls_layout)

        # סידור אזור הגרף והבקרה בשורה העליונה
        top_content_layout = QHBoxLayout()
        top_content_layout.setSpacing(14)
        top_content_layout.addWidget(self.plot_card, 1)
        top_content_layout.addWidget(self.controls_card)

        # יצירת כרטיס טבלת פרמטרי הסימולציה
        self.table_card = QWidget()
        self.table_card.setObjectName("graphTableCard")

        self.parameters_title = QLabel("Simulation Parameters")
        self.parameters_title.setObjectName("sectionTitle")

        self.simulations_count_label = QLabel("0 completed simulations")
        self.simulations_count_label.setObjectName("secondaryLabel")

        # יצירת כפתור להצגה והסתרה של טבלת הפרמטרים
        self.toggle_table_button = QPushButton("Show Simulation Parameters ▼")
        self.toggle_table_button.setObjectName("toggleTableButton")
        self.toggle_table_button.setFixedHeight(30)
        self.toggle_table_button.clicked.connect(self.toggle_parameters_table)

        table_header_layout = QHBoxLayout()
        table_header_layout.setSpacing(12)
        table_header_layout.addWidget(self.parameters_title)
        table_header_layout.addWidget(self.simulations_count_label)
        table_header_layout.addStretch()
        table_header_layout.addWidget(self.toggle_table_button)

        self.table_divider = QWidget()
        self.table_divider.setObjectName("dividerLine")
        self.table_divider.setFixedHeight(1)
        self.table_divider.setVisible(False)

        # הגדרת טבלת הפרמטרים
        self.parameters_table = QTableWidget(12, 2)
        self.parameters_table.setObjectName("parametersTable")
        self.parameters_table.setHorizontalHeaderLabels(["Category", "Parameter"])
        self.parameters_table.setColumnWidth(0, 110)
        self.parameters_table.setColumnWidth(1, 290)
        self.parameters_table.setAlternatingRowColors(True)
        self.parameters_table.verticalHeader().setVisible(False)
        self.parameters_table.verticalHeader().setDefaultSectionSize(26)
        self.parameters_table.horizontalHeader().setFixedHeight(32)
        self.parameters_table.setFixedHeight(348)
        self.parameters_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.parameters_table.setVisible(False)

        # הגדרת קטגוריות מעוצבות ומיזוג תאים אנכי בעמודת הקטגוריה
        general_label = QLabel("General")
        general_label.setObjectName("categoryGeneral")
        general_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.parameters_table.setSpan(0, 0, 2, 1)
        self.parameters_table.setCellWidget(0, 0, general_label)

        body1_label = QLabel("Body 1")
        body1_label.setObjectName("categoryBody1")
        body1_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.parameters_table.setSpan(2, 0, 5, 1)
        self.parameters_table.setCellWidget(2, 0, body1_label)

        body2_label = QLabel("Body 2")
        body2_label.setObjectName("categoryBody2")
        body2_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.parameters_table.setSpan(7, 0, 5, 1)
        self.parameters_table.setCellWidget(7, 0, body2_label)

        # מילוי שמות הפרמטרים בעמודה השנייה והוספת קו הפרדה בין הקבוצות
        parameter_names = [
            "Thermal Conductance (W/°C)",
            "Simulation Duration (s)",
            "Material",
            "Initial Temperature (°C)",
            "Mass (kg)",
            "Specific Heat Capacity (J/(kg·°C))",
            "Heating Power (W)",
            "Material",
            "Initial Temperature (°C)",
            "Mass (kg)",
            "Specific Heat Capacity (J/(kg·°C))",
            "Heating Power (W)",
        ]
        for row in range(len(parameter_names)):
            if row == 1 or row == 6:
                param_label = QLabel(parameter_names[row])
                param_label.setObjectName("tableSeparatorParam")
                param_label.setAlignment(
                    Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
                )
                self.parameters_table.setCellWidget(row, 1, param_label)
            else:
                self.parameters_table.setItem(
                    row, 1, QTableWidgetItem(parameter_names[row])
                )

        table_card_layout = QVBoxLayout()
        table_card_layout.setContentsMargins(16, 12, 16, 12)
        table_card_layout.setSpacing(10)
        table_card_layout.addLayout(table_header_layout)
        table_card_layout.addWidget(self.table_divider)
        table_card_layout.addWidget(self.parameters_table)
        self.table_card.setLayout(table_card_layout)

        # סידור כל הכרטיסים בחלון הראשי של הגרפים
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(14)
        main_layout.addWidget(self.header_card)
        main_layout.addLayout(top_content_layout, 1)
        main_layout.addWidget(self.table_card)
        self.setLayout(main_layout)

    # עיצוב אחיד לצירים, כותרות ורשת הגרף
    def style_axes(self, title):
        self.figure.set_facecolor("#FFFFFF")
        self.ax.set_facecolor("#FFFFFF")
        self.ax.set_title(
            title, color="#23364D", fontsize=13, fontweight="bold", pad=12
        )
        self.ax.set_xlabel("Time (s)", color="#23364D", fontsize=11)
        self.ax.set_ylabel("Temperature (°C)", color="#23364D", fontsize=11)
        self.ax.grid(True, linestyle="--", color="#E2E8F0")
        self.ax.tick_params(colors="#64748B", labelsize=10)

        # עיצוב גבולות הצירים בגוון עדין
        self.ax.spines["top"].set_color("#E2E8F0")
        self.ax.spines["right"].set_color("#E2E8F0")
        self.ax.spines["left"].set_color("#CBD5E1")
        self.ax.spines["bottom"].set_color("#CBD5E1")
        self.figure.subplots_adjust(left=0.09, right=0.97, top=0.86, bottom=0.19)

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

        # ניקוי הגרף והגדרת כותרות, עיצוב ורשת
        self.ax.clear()
        self.style_axes(f"Simulation {number} - Temperature vs. Time")

        # שרטוט הגוף הראשון
        if selected_body == "Body 1" or selected_body == "Both Bodies":
            self.ax.plot(
                simulation["time"],
                simulation["temperature1"],
                label=f"Body 1 ({material1})",
                color="#DC2626",
                linewidth=2.2,
            )

        # שרטוט הגוף השני
        if selected_body == "Body 2" or selected_body == "Both Bodies":
            self.ax.plot(
                simulation["time"],
                simulation["temperature2"],
                label=f"Body 2 ({material2})",
                color="#2871B8",
                linewidth=2.2,
            )

        # הצגת המקרא, עדכון הגרף ואיפוס היסטוריית הניווט לתצוגה המלאה
        self.ax.legend(
            facecolor="#FFFFFF",
            edgecolor="#CBD5E1",
            frameon=True,
            fontsize=10,
        )
        self.canvas.draw()
        self.toolbar.update()
        self.toolbar.push_current()

    # ניקוי הגרף המוצג ואיפוס היסטוריית הניווט
    def clear_graph(self):
        self.ax.clear()
        self.style_axes("Temperature vs. Time")
        self.canvas.draw()
        self.toolbar.update()
        self.toolbar.push_current()

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

        # עדכון תווית מספר הסימולציות שהסתיימו
        count = len(simulations)
        if count == 1:
            self.simulations_count_label.setText("1 completed simulation")
        else:
            self.simulations_count_label.setText(f"{count} completed simulations")

        # הגדרת מספר העמודות וכותרותיהן
        self.parameters_table.setColumnCount(count + 2)

        headers = ["Category", "Parameter"]
        for simulation in simulations:
            headers.append(f"Simulation {simulation['number']}")
        self.parameters_table.setHorizontalHeaderLabels(headers)

        # מילוי נתוני כל הסימולציות בעמודות הטבלה
        for i in range(count):
            simulation = simulations[i]
            column = i + 2
            self.parameters_table.setColumnWidth(column, 135)

            values = [
                f"{simulation['conductance']:.2f}",
                f"{simulation['duration']:.2f}",
                simulation["material1"],
                f"{simulation['initial_temp1']:.2f}",
                f"{simulation['mass1']:.2f}",
                f"{simulation['heat_capacity1']:.2f}",
                f"{simulation['heating_power1']:.2f}",
                simulation["material2"],
                f"{simulation['initial_temp2']:.2f}",
                f"{simulation['mass2']:.2f}",
                f"{simulation['heat_capacity2']:.2f}",
                f"{simulation['heating_power2']:.2f}",
            ]

            for row in range(len(values)):
                if row == 1 or row == 6:
                    existing_label = self.parameters_table.cellWidget(row, column)
                    if existing_label is None:
                        value_label = QLabel(values[row])
                        value_label.setObjectName("tableSeparatorValue")
                        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.parameters_table.setCellWidget(
                            row, column, value_label
                        )
                    else:
                        existing_label.setText(values[row])
                else:
                    item = QTableWidgetItem(values[row])
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    self.parameters_table.setItem(row, column, item)

    # הצגה או הסתרה של טבלת פרמטרי הסימולציה באותו חלון
    def toggle_parameters_table(self):
        is_visible = not self.parameters_table.isVisible()
        self.parameters_table.setVisible(is_visible)
        self.table_divider.setVisible(is_visible)

        if is_visible:
            self.toggle_table_button.setText("Hide Simulation Parameters ▲")
        else:
            self.toggle_table_button.setText("Show Simulation Parameters ▼")

    # פתיחת חלון ייצוא הנתונים
    def open_export_window(self):
        self.export_window.refresh_options()
        self.export_window.show()

# הפעלת חלון הגרפים לבדיקה ישירה
if __name__ == "__main__":
    app = QApplication()
    with open("style.qss", encoding="utf-8") as f:
        app.setStyleSheet(f.read())
    window = GraphWindow()
    window.show()
    app.exec()
