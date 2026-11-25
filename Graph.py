# יצירת חלון הגרפים עם PySide6 ו-Matplotlib
from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg,
    NavigationToolbar2QT,
)
from matplotlib.figure import Figure
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QColor, QFont
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QTabWidget,
    QTableWidget,
    QTableWidgetItem,
    QToolButton,
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

        # מעקב אחר העקומות המוצגות כעת בכל לשונית
        self.body1_displayed = False
        self.body2_displayed = False
        self.rate_displayed_simulations = []
        self.cumulative_displayed_simulations = []

        # רשימות צבעים וסגנונות קו אחידים לפי מספר הסימולציה
        self.simulation_colors = [
            "#0D9488",
            "#7C3AED",
            "#EA580C",
            "#2871B8",
            "#DC2626",
            "#64748B",
        ]
        self.simulation_linestyles = ["-", "--", "-.", ":"]

        self.setupUI()

    # בניית ממשק המשתמש
    def setupUI(self):
        self.setObjectName("graphWindow")
        self.setWindowTitle("Heat Transfer Graphs")

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
        header_layout.setContentsMargins(16, 8, 16, 8)
        header_layout.addLayout(header_text_layout)
        header_layout.addStretch()
        self.header_card.setLayout(header_layout)

        # יצירת אזור הלשוניות לשלושת הגרפים בצד שמאל
        self.graph_tabs = QTabWidget()
        self.graph_tabs.setObjectName("graphTabs")

        # לשונית 1: גרף טמפרטורה מול זמן
        self.temperature_tab = QWidget()
        self.temperature_tab.setObjectName("graphTabPage")

        self.figure = Figure(figsize=(8, 3.3), layout="constrained")
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.canvas.setMinimumSize(300, 160)
        self.canvas.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.ax = self.figure.add_subplot(111)
        self.style_axes("Temperature vs. Time")

        self.toolbar = NavigationToolbar2QT(self.canvas, self)

        temperature_tab_layout = QVBoxLayout()
        temperature_tab_layout.setContentsMargins(10, 6, 10, 6)
        temperature_tab_layout.setSpacing(4)
        temperature_tab_layout.addWidget(self.canvas, 1)
        temperature_tab_layout.addWidget(self.toolbar)
        self.temperature_tab.setLayout(temperature_tab_layout)

        # לשונית 2: גרף קצב מעבר חום מול זמן
        self.rate_tab = QWidget()
        self.rate_tab.setObjectName("graphTabPage")

        self.rate_figure = Figure(figsize=(8, 3.3), layout="constrained")
        self.rate_canvas = FigureCanvasQTAgg(self.rate_figure)
        self.rate_canvas.setMinimumSize(300, 160)
        self.rate_canvas.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.rate_ax = self.rate_figure.add_subplot(111)
        self.style_axes(
            "Heat Transfer Rate vs. Time",
            self.rate_ax,
            self.rate_figure,
            "Heat Transfer Rate (W)",
        )

        self.rate_toolbar = NavigationToolbar2QT(self.rate_canvas, self)

        rate_tab_layout = QVBoxLayout()
        rate_tab_layout.setContentsMargins(10, 6, 10, 6)
        rate_tab_layout.setSpacing(4)
        rate_tab_layout.addWidget(self.rate_canvas, 1)
        rate_tab_layout.addWidget(self.rate_toolbar)
        self.rate_tab.setLayout(rate_tab_layout)

        # לשונית 3: גרף מעבר חום מצטבר מול זמן
        self.cumulative_tab = QWidget()
        self.cumulative_tab.setObjectName("graphTabPage")

        self.cumulative_figure = Figure(figsize=(8, 3.3), layout="constrained")
        self.cumulative_canvas = FigureCanvasQTAgg(self.cumulative_figure)
        self.cumulative_canvas.setMinimumSize(300, 160)
        self.cumulative_canvas.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.cumulative_ax = self.cumulative_figure.add_subplot(111)
        self.style_axes(
            "Cumulative Heat Transfer vs. Time",
            self.cumulative_ax,
            self.cumulative_figure,
            "Transferred Energy (kJ)",
        )

        self.cumulative_toolbar = NavigationToolbar2QT(
            self.cumulative_canvas, self
        )

        cumulative_tab_layout = QVBoxLayout()
        cumulative_tab_layout.setContentsMargins(10, 6, 10, 6)
        cumulative_tab_layout.setSpacing(4)
        cumulative_tab_layout.addWidget(self.cumulative_canvas, 1)
        cumulative_tab_layout.addWidget(self.cumulative_toolbar)
        self.cumulative_tab.setLayout(cumulative_tab_layout)

        # הוספת שלוש הלשוניות הקבועות וקביעת ברירת המחדל
        self.graph_tabs.addTab(self.temperature_tab, "Temperature")
        self.graph_tabs.addTab(self.rate_tab, "Heat Transfer Rate")
        self.graph_tabs.addTab(self.cumulative_tab, "Cumulative Heat Transfer")
        self.graph_tabs.setCurrentIndex(0)

        # יצירת כרטיס הבקרה בצד ימין עם גלילה אנכית פנימית בעת הצורך
        self.controls_card = QWidget()
        self.controls_card.setObjectName("graphControlsCard")
        self.controls_card.setFixedWidth(262)
        self.controls_card.setMinimumHeight(180)
        self.controls_card.setSizePolicy(
            QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding
        )

        self.controls_title = QLabel("Graph Controls")
        self.controls_title.setObjectName("cardTitle")
        self.controls_title.setFixedHeight(24)
        self.controls_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        controls_divider = QWidget()
        controls_divider.setObjectName("dividerLine")
        controls_divider.setFixedHeight(1)

        # יצירת רשימה לבחירת הסימולציה
        self.simulation_select_label = QLabel("Select Simulation")
        self.simulation_select_label.setObjectName("secondaryLabel")
        self.simulation_select_label.setFixedSize(214, 17)

        self.simulation_selector = QComboBox()
        self.simulation_selector.setFixedSize(214, 28)
        self.simulation_selector.currentIndexChanged.connect(
            self.simulation_changed
        )

        # יצירת רשימה לבחירת הגוף
        self.body_select_label = QLabel("Select Body")
        self.body_select_label.setObjectName("secondaryLabel")
        self.body_select_label.setFixedSize(214, 17)

        self.body_selector = QComboBox()
        self.body_selector.setFixedSize(214, 28)
        self.body_selector.addItems(["Body 1", "Body 2"])
        self.body_selector.setCurrentText("Body 1")

        # חיבור שינוי לשונית לעדכון זמינות בחירת הגוף
        self.graph_tabs.currentChanged.connect(self.tab_changed)

        # יצירת כפתור שרטוט
        self.draw_button = QPushButton("Draw")
        self.draw_button.setObjectName("drawButton")
        self.draw_button.setFixedSize(214, 32)
        self.draw_button.setEnabled(False)
        self.draw_button.clicked.connect(self.draw_graph)

        # יצירת כפתור ניקוי
        self.clear_button = QPushButton("Clear")
        self.clear_button.setObjectName("graphSecondaryButton")
        self.clear_button.setFixedSize(214, 32)
        self.clear_button.clicked.connect(self.clear_graph)

        # יצירת כפתור ייצוא נתונים
        self.export_button = QPushButton("Export Data")
        self.export_button.setObjectName("graphSecondaryButton")
        self.export_button.setFixedSize(214, 32)
        self.export_button.clicked.connect(self.open_export_window)

        # יצירת אזור המשוואה השולטת כיחידה עצמאית שניתן להסתיר במצב טבלה מורחבת
        self.equation_section = QWidget()
        equation_divider = QWidget()
        equation_divider.setObjectName("dividerLine")
        equation_divider.setFixedHeight(1)

        self.equation_heading = QLabel("Governing Equation")
        self.equation_heading.setObjectName("equationHeading")
        self.equation_heading.setFixedHeight(20)
        self.equation_heading.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.equation_card = QWidget()
        self.equation_card.setObjectName("equationCard")
        self.equation_card.setFixedWidth(214)

        self.equation_subheading1 = QLabel()
        self.equation_subheading1.setObjectName("equationSubheading")
        self.equation_subheading1.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # קנבס Matplotlib ייעודי להצגת המשוואה הראשונה באיכות גבוהה
        self.equation_figure1 = Figure()
        self.equation_canvas1 = FigureCanvasQTAgg(self.equation_figure1)
        self.equation_ax1 = self.equation_figure1.add_subplot(111)
        self.equation_canvas1.setFixedWidth(190)

        self.equation_mid_divider = QWidget()
        self.equation_mid_divider.setObjectName("dividerLine")
        self.equation_mid_divider.setFixedHeight(1)

        self.equation_subheading2 = QLabel()
        self.equation_subheading2.setObjectName("equationSubheading")
        self.equation_subheading2.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # קנבס Matplotlib ייעודי להצגת המשוואה השנייה במידת הצורך
        self.equation_figure2 = Figure()
        self.equation_canvas2 = FigureCanvasQTAgg(self.equation_figure2)
        self.equation_ax2 = self.equation_figure2.add_subplot(111)
        self.equation_canvas2.setFixedWidth(190)

        equation_inner_divider = QWidget()
        equation_inner_divider.setObjectName("dividerLine")
        equation_inner_divider.setFixedHeight(1)

        self.equation_explanation_label = QLabel()
        self.equation_explanation_label.setObjectName("equationExplanation")
        self.equation_explanation_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        )
        self.equation_explanation_label.setWordWrap(True)

        equation_card_layout = QVBoxLayout()
        equation_card_layout.setContentsMargins(10, 6, 10, 6)
        equation_card_layout.setSpacing(3)
        equation_card_layout.addWidget(self.equation_subheading1)
        equation_card_layout.addWidget(self.equation_canvas1)
        equation_card_layout.addWidget(self.equation_mid_divider)
        equation_card_layout.addWidget(self.equation_subheading2)
        equation_card_layout.addWidget(self.equation_canvas2)
        equation_card_layout.addWidget(equation_inner_divider)
        equation_card_layout.addWidget(self.equation_explanation_label)
        self.equation_card.setLayout(equation_card_layout)

        equation_section_layout = QVBoxLayout()
        equation_section_layout.setContentsMargins(0, 4, 0, 0)
        equation_section_layout.setSpacing(4)
        equation_section_layout.addWidget(equation_divider)
        equation_section_layout.addWidget(self.equation_heading)
        equation_section_layout.addWidget(self.equation_card)
        self.equation_section.setLayout(equation_section_layout)

        # סידור רכיבי הבקרה בתוך מכל נגלל אנכית בעת הצורך בלבד
        controls_content = QWidget()
        controls_content.setObjectName("controlsScrollContent")

        controls_layout = QVBoxLayout()
        controls_layout.setContentsMargins(14, 8, 14, 8)
        controls_layout.setSpacing(5)
        controls_layout.addWidget(self.controls_title)
        controls_layout.addWidget(controls_divider)
        controls_layout.addWidget(self.simulation_select_label)
        controls_layout.addWidget(self.simulation_selector)
        controls_layout.addWidget(self.body_select_label)
        controls_layout.addWidget(self.body_selector)
        controls_layout.addWidget(self.draw_button)
        controls_layout.addWidget(self.clear_button)
        controls_layout.addWidget(self.export_button)
        controls_layout.addWidget(self.equation_section)
        controls_layout.addStretch()
        controls_content.setLayout(controls_layout)

        self.controls_scroll_area = QScrollArea()
        self.controls_scroll_area.setObjectName("controlsScrollArea")
        self.controls_scroll_area.setWidgetResizable(True)
        self.controls_scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.controls_scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.controls_scroll_area.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.controls_scroll_area.setWidget(controls_content)

        controls_card_layout = QVBoxLayout()
        controls_card_layout.setContentsMargins(2, 2, 2, 2)
        controls_card_layout.addWidget(self.controls_scroll_area)
        self.controls_card.setLayout(controls_card_layout)

        # הצגת משוואת ברירת המחדל עבור לשונית הטמפרטורה
        self.update_equation_display(0)

        # סידור אזור הגרפים והבקרה במכל העליון הגמיש
        self.top_container = QWidget()
        self.top_container.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        top_content_layout = QHBoxLayout()
        top_content_layout.setContentsMargins(0, 0, 0, 0)
        top_content_layout.setSpacing(14)
        top_content_layout.addWidget(self.graph_tabs, 1)
        top_content_layout.addWidget(self.controls_card)
        self.top_container.setLayout(top_content_layout)

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
        self.toggle_table_button.setFixedHeight(26)
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

        # הגדרת טבלת הפרמטרים בגובה מחושב לכל 12 השורות עם גלילה בעת הצורך
        self.table_row_height = 22
        self.table_header_height = 28
        self.parameters_table = QTableWidget(12, 2)
        self.parameters_table.setObjectName("parametersTable")
        self.parameters_table.setHorizontalHeaderLabels(["Category", "Parameter"])
        self.parameters_table.setColumnWidth(0, 105)
        self.parameters_table.setColumnWidth(1, 275)
        self.parameters_table.setAlternatingRowColors(True)
        self.parameters_table.verticalHeader().setVisible(False)
        self.parameters_table.verticalHeader().setDefaultSectionSize(
            self.table_row_height
        )
        self.parameters_table.horizontalHeader().setFixedHeight(
            self.table_header_height
        )
        self.parameters_table.setMinimumHeight(100)
        self.parameters_table.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        self.parameters_table.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.parameters_table.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
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
        table_card_layout.setContentsMargins(14, 8, 14, 8)
        table_card_layout.setSpacing(6)
        table_card_layout.addLayout(table_header_layout)
        table_card_layout.addWidget(self.table_divider)
        table_card_layout.addWidget(self.parameters_table, 1)
        self.table_card.setLayout(table_card_layout)
        self.table_card.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum
        )

        # סידור כל הכרטיסים בחלון הראשי של הגרפים במרווחים קומפקטיים
        self.main_layout = QVBoxLayout()
        self.main_layout.setContentsMargins(12, 10, 12, 10)
        self.main_layout.setSpacing(8)
        self.main_layout.addWidget(self.header_card, 0)
        self.main_layout.addWidget(self.top_container, 1)
        self.main_layout.addWidget(self.table_card, 0)
        self.setLayout(self.main_layout)

        # עיצוב קומפקטי ואחיד לכל שלושת סרגלי הכלים לאחר הרכבת עץ החלון
        self.style_toolbar(self.toolbar)
        self.style_toolbar(self.rate_toolbar)
        self.style_toolbar(self.cumulative_toolbar)

        # התאמת גודל ומיקום החלון לשטח המסך הזמין (ללא שורת המשימות)
        self.fit_to_screen()

    # חישוב גודל התחלתי מתאים למסך הזמין ומרכוז החלון
    def fit_to_screen(self):
        screen = QApplication.primaryScreen()
        if screen is not None:
            available = screen.availableGeometry()
            min_width = min(760, max(560, available.width() - 40))
            min_height = min(500, max(420, available.height() - 40))
            self.setMinimumSize(min_width, min_height)

            width = min(1200, int(available.width() * 0.92))
            height = min(780, int(available.height() * 0.92))
            width = max(width, min_width)
            height = max(height, min_height)
            self.resize(width, height)

            x = available.x() + (available.width() - width) // 2
            y = available.y() + (available.height() - height) // 2
            self.move(x, y)
        else:
            self.setMinimumSize(760, 500)
            self.resize(1140, 750)

    # חישוב הגובה הנדרש להצגת כל 12 שורות הטבלה, הכותרת, המסגרת ופס הגלילה האופקי
    def calculate_required_table_height(self):
        total_rows_height = (
            self.parameters_table.rowCount() * self.table_row_height
        )
        frame_height = self.parameters_table.frameWidth() * 2 + 4

        # בדיקה האם נדרש פס גלילה אופקי לפי סכום רוחבי העמודות
        total_columns_width = 0
        for col in range(self.parameters_table.columnCount()):
            total_columns_width += self.parameters_table.columnWidth(col)

        available_table_width = max(100, self.width() - 56)
        hbar_height = 0
        if total_columns_width > available_table_width:
            hbar_height = (
                self.parameters_table.horizontalScrollBar().sizeHint().height()
            )

        return (
            self.table_header_height
            + total_rows_height
            + frame_height
            + hbar_height
        )

    # התאמת גובה כרטיס הטבלה המורחבת כך שכל 12 השורות יוצגו בגודל רגיל ללא הגדלת החלון
    def update_expanded_table_height(self):
        if not self.parameters_table.isVisible():
            return

        required_table_h = self.calculate_required_table_height()
        card_overhead = 56
        min_top_h = 278
        header_h = max(52, self.header_card.sizeHint().height())
        available_for_table_card = max(
            165, self.height() - header_h - 38 - min_top_h
        )
        target_card_h = min(
            required_table_h + card_overhead, available_for_table_card
        )
        self.table_card.setMaximumHeight(target_card_h)

    # שמירת פרופורציות הטבלה המורחבת בעת שינוי גודל החלון ידנית
    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.parameters_table.isVisible():
            self.update_expanded_table_height()

    # עיצוב קומפקטי ואחיד לסרגל הכלים של Matplotlib בכל לשוניות הגרפים
    def style_toolbar(self, toolbar):
        toolbar.setObjectName("graphToolbar")
        toolbar.style().unpolish(toolbar)
        toolbar.style().polish(toolbar)
        toolbar.setIconSize(QSize(16, 16))
        toolbar.setFixedHeight(29)
        toolbar.setContentsMargins(2, 1, 2, 1)
        if toolbar.layout() is not None:
            toolbar.layout().setContentsMargins(2, 1, 2, 1)
            toolbar.layout().setSpacing(3)
        for button in toolbar.findChildren(QToolButton):
            if button.objectName() != "qt_toolbar_ext_button":
                button.style().unpolish(button)
                button.style().polish(button)
                button.setIconSize(QSize(16, 16))
                button.setFixedSize(24, 24)

    # עיצוב אחיד לצירים, כותרות ורשת הגרף
    def style_axes(
        self, title, ax=None, figure=None, ylabel="Temperature (°C)"
    ):
        if ax is None:
            ax = self.ax
        if figure is None:
            figure = self.figure

        figure.set_facecolor("#FFFFFF")
        ax.set_facecolor("#FFFFFF")
        ax.set_title(
            title, color="#23364D", fontsize=13, fontweight="bold", pad=12
        )
        ax.set_xlabel("Time (s)", color="#23364D", fontsize=11)
        ax.set_ylabel(ylabel, color="#23364D", fontsize=11)
        ax.grid(True, linestyle="--", color="#E2E8F0")
        ax.tick_params(colors="#64748B", labelsize=10)

        # עיצוב גבולות הצירים בגוון עדין
        ax.spines["top"].set_color("#E2E8F0")
        ax.spines["right"].set_color("#E2E8F0")
        ax.spines["left"].set_color("#CBD5E1")
        ax.spines["bottom"].set_color("#CBD5E1")

    # עדכון זמינות בחירת הגוף ותצוגת המשוואה בעת מעבר בין לשוניות הגרפים
    def tab_changed(self, index):
        self.body_selector.setEnabled(index == 0)
        self.update_equation_display(index)

    # הצגת נוסחה מתמטית ממורכזת באמצעות Matplotlib MathText
    def render_equation(self, ax, figure, canvas, latex_text, fontsize, height):
        canvas.setFixedHeight(height)
        figure.set_facecolor("#F5F8FB")
        ax.clear()
        ax.set_facecolor("#F5F8FB")
        ax.axis("off")
        figure.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0)
        ax.text(
            0.5,
            0.5,
            latex_text,
            ha="center",
            va="center",
            fontsize=fontsize,
            color="#23364D",
            math_fontfamily="cm",
            transform=ax.transAxes,
        )
        canvas.draw()

    # עדכון תצוגת המשוואה השולטת לפי הלשונית הפעילה
    def update_equation_display(self, index):
        if index == 0:
            self.equation_subheading1.setText("Temperature Change")
            self.equation_subheading1.setVisible(True)
            self.render_equation(
                self.equation_ax1,
                self.equation_figure1,
                self.equation_canvas1,
                r"$\Delta T = \frac{\Delta Q}{m \cdot c}$",
                17,
                52,
            )

            self.equation_mid_divider.setVisible(False)
            self.equation_subheading2.setVisible(False)
            self.equation_canvas2.setVisible(True)
            self.render_equation(
                self.equation_ax2,
                self.equation_figure2,
                self.equation_canvas2,
                r"$T_{\mathrm{new}} = T + \Delta T$",
                15,
                32,
            )

            explanation = (
                "<p style='margin:0px 0px 3px 0px;'>"
                "<b style='color:#23364D;'>m</b> &mdash; Mass (kg)</p>"
                "<p style='margin:0px 0px 3px 0px;'>"
                "<b style='color:#23364D;'>c</b> &mdash; Specific heat capacity "
                "(J/(kg&middot;&deg;C))</p>"
                "<p style='margin:0px;'>"
                "<b style='color:#23364D;'>&Delta;Q</b> &mdash; Net heat added (J)</p>"
            )
        elif index == 1:
            self.equation_subheading1.setText("Heat Transfer Rate")
            self.equation_subheading1.setVisible(True)
            self.render_equation(
                self.equation_ax1,
                self.equation_figure1,
                self.equation_canvas1,
                r"$\dot{Q}_{1\to2} = \sigma(T_1 - T_2)$",
                15,
                46,
            )

            self.equation_mid_divider.setVisible(False)
            self.equation_subheading2.setVisible(False)
            self.equation_canvas2.setVisible(False)

            explanation = (
                "<p style='margin:0px 0px 3px 0px;'>"
                "<b style='color:#23364D;'>&sigma;</b> &mdash; Thermal conductance "
                "(W/&deg;C)</p>"
                "<p style='margin:0px 0px 4px 0px;'>"
                "<b style='color:#23364D;'>T<sub>1</sub>, T<sub>2</sub></b> "
                "&mdash; Temperature (&deg;C)</p>"
                "<p style='margin:0px 0px 2px 0px; color:#0D9488;'>"
                "Positive: Body 1 &rarr; Body 2</p>"
                "<p style='margin:0px;'>"
                "Negative: Body 2 &rarr; Body 1</p>"
            )
        else:
            self.equation_subheading1.setText("Continuous Model")
            self.equation_subheading1.setVisible(True)
            self.render_equation(
                self.equation_ax1,
                self.equation_figure1,
                self.equation_canvas1,
                r"$Q(t) = \int_0^t \dot{Q}(\tau)\,d\tau$",
                14,
                54,
            )

            self.equation_mid_divider.setVisible(True)
            self.equation_subheading2.setText("Numerical Model")
            self.equation_subheading2.setVisible(True)
            self.equation_canvas2.setVisible(True)
            self.render_equation(
                self.equation_ax2,
                self.equation_figure2,
                self.equation_canvas2,
                r"$Q_{i+1} = Q_i + \dot{Q}_i\Delta t_i$",
                14,
                34,
            )

            explanation = (
                "<p style='margin:0px 0px 3px 0px;'>"
                "<b style='color:#23364D;'>Q</b> &mdash; Net transferred energy (J)</p>"
                "<p style='margin:0px 0px 3px 0px;'>"
                "<b style='color:#23364D;'>Q&#775;</b> &mdash; Heat transfer rate (W)</p>"
                "<p style='margin:0px 0px 4px 0px;'>"
                "<b style='color:#23364D;'>&Delta;t</b> &mdash; Simulation time step (s)</p>"
                "<p style='margin:0px; color:#64748B;'>Displayed in kJ</p>"
            )

        self.equation_explanation_label.setText(explanation)
        self.equation_explanation_label.setMinimumHeight(
            self.equation_explanation_label.heightForWidth(190) + 4
        )

    # הפעלת השרטוט עבור הלשונית הפעילה בלבד
    def draw_graph(self):
        if self.main_window is None:
            return

        index = self.simulation_selector.currentIndex()
        if index < 0 or index >= len(self.main_window.simulation_history):
            return

        simulation = self.main_window.simulation_history[index]
        current_tab = self.graph_tabs.currentIndex()

        if current_tab == 0:
            self.draw_temperature_graph(simulation)
        elif current_tab == 1:
            self.draw_heat_transfer_rate_graph(simulation)
        elif current_tab == 2:
            self.draw_cumulative_heat_transfer_graph(simulation)

    # הוספת עקומת הגוף שנבחר לגרף הטמפרטורה ללא מחיקת עקומות קיימות
    def draw_temperature_graph(self, simulation):
        number = simulation["number"]
        material1 = simulation["material1"]
        material2 = simulation["material2"]
        selected_body = self.body_selector.currentText()

        # שרטוט הגוף שנבחר רק אם אינו מוצג כבר בגרף
        if selected_body == "Body 1":
            if self.body1_displayed:
                return
            self.ax.plot(
                simulation["time"],
                simulation["temperature1"],
                label=f"Body 1 ({material1})",
                color="#DC2626",
                linewidth=2.2,
            )
            self.body1_displayed = True
        elif selected_body == "Body 2":
            if self.body2_displayed:
                return
            self.ax.plot(
                simulation["time"],
                simulation["temperature2"],
                label=f"Body 2 ({material2})",
                color="#2871B8",
                linewidth=2.2,
            )
            self.body2_displayed = True

        # עדכון הכותרת, המקרא, גבולות הצירים והיסטוריית הניווט
        self.ax.set_title(
            f"Simulation {number} - Temperature vs. Time",
            color="#23364D",
            fontsize=13,
            fontweight="bold",
            pad=12,
        )
        self.ax.legend(
            facecolor="#FFFFFF",
            edgecolor="#CBD5E1",
            frameon=True,
            fontsize=10,
        )
        self.ax.relim()
        self.ax.autoscale()
        self.canvas.draw()
        self.toolbar.update()
        self.toolbar.push_current()

        # חישוב קצב מעבר החום בין הגופים
    def calculate_heat_transfer_rate(self, simulation):
        temperature1 = simulation["temperature1"]
        temperature2 = simulation["temperature2"]
        conductance = simulation["conductance"]

        rates = []

        for i in range(len(temperature1)):
            rate = conductance * (temperature1[i] - temperature2[i])
            rates.append(rate)

        return rates

    # הוספת עקומת קצב מעבר החום של הסימולציה הנבחרת להשוואה
    def draw_heat_transfer_rate_graph(self, simulation):
        number = simulation["number"]
        if number in self.rate_displayed_simulations:
            return

        rates = self.calculate_heat_transfer_rate(simulation)
        if len(rates) == 0:
            return

        # קביעת צבע וסגנון קו קבועים לפי מספר הסימולציה
        color_index = (number - 1) % len(self.simulation_colors)
        style_index = ((number - 1) // len(self.simulation_colors)) % len(
            self.simulation_linestyles
        )
        color = self.simulation_colors[color_index]
        linestyle = self.simulation_linestyles[style_index]

        self.rate_ax.plot(
            simulation["time"],
            rates,
            label=f"Simulation {number}",
            color=color,
            linestyle=linestyle,
            linewidth=2.2,
        )
        self.rate_displayed_simulations.append(number)

        # עדכון הכותרת הכללית, המקרא, גבולות הצירים והיסטוריית הניווט
        self.rate_ax.set_title(
            "Heat Transfer Rate vs. Time",
            color="#23364D",
            fontsize=13,
            fontweight="bold",
            pad=12,
        )
        self.rate_ax.legend(
            facecolor="#FFFFFF",
            edgecolor="#CBD5E1",
            frameon=True,
            fontsize=10,
        )
        self.rate_ax.margins(x=0.05, y=0.05)
        self.rate_ax.relim()
        self.rate_ax.autoscale()
        self.rate_canvas.draw()
        self.rate_toolbar.update()
        self.rate_toolbar.push_current()

        # חישוב אנרגיית החום המצטברת בין הגופים
    def calculate_cumulative_heat_transfer(self, simulation):
        time = simulation["time"]
        temperature1 = simulation["temperature1"]
        temperature2 = simulation["temperature2"]
        conductance = simulation["conductance"]

        if len(time) == 0:
            return []

        cumulative_kj = [0.0]
        total_energy_joules = 0.0

        # חישוב כמות החום שעברה בכל צעד זמן
        for i in range(1, len(time)):
            dt = time[i] - time[i - 1]
            rate = conductance * (temperature1[i - 1] - temperature2[i - 1])

            total_energy_joules += rate * dt
            cumulative_kj.append(total_energy_joules / 1000.0)

        return cumulative_kj

    # הוספת עקומת מעבר החום המצטבר של הסימולציה הנבחרת להשוואה
    def draw_cumulative_heat_transfer_graph(self, simulation):
        number = simulation["number"]
        if number in self.cumulative_displayed_simulations:
            return

        cumulative_kj = self.calculate_cumulative_heat_transfer(simulation)
        if len(cumulative_kj) == 0:
            return

        # קביעת צבע וסגנון קו קבועים לפי מספר הסימולציה
        color_index = (number - 1) % len(self.simulation_colors)
        style_index = ((number - 1) // len(self.simulation_colors)) % len(
            self.simulation_linestyles
        )
        color = self.simulation_colors[color_index]
        linestyle = self.simulation_linestyles[style_index]

        self.cumulative_ax.plot(
            simulation["time"],
            cumulative_kj,
            label=f"Simulation {number}",
            color=color,
            linestyle=linestyle,
            linewidth=2.2,
        )
        self.cumulative_displayed_simulations.append(number)

        # עדכון הכותרת הכללית, המקרא, גבולות הצירים והיסטוריית הניווט
        self.cumulative_ax.set_title(
            "Cumulative Heat Transfer vs. Time",
            color="#23364D",
            fontsize=13,
            fontweight="bold",
            pad=12,
        )
        self.cumulative_ax.legend(
            facecolor="#FFFFFF",
            edgecolor="#CBD5E1",
            frameon=True,
            fontsize=10,
        )
        self.cumulative_ax.margins(x=0.05, y=0.05)
        self.cumulative_ax.relim()
        self.cumulative_ax.autoscale()
        self.cumulative_canvas.draw()
        self.cumulative_toolbar.update()
        self.cumulative_toolbar.push_current()

    # ניקוי גרף הטמפרטורה ואיפוס המעקב וההיסטוריה שלו
    def clear_temperature_graph(self):
        self.body1_displayed = False
        self.body2_displayed = False
        self.ax.clear()
        self.style_axes("Temperature vs. Time")
        self.canvas.draw()
        self.toolbar.update()
        self.toolbar.push_current()

    # ניקוי גרף קצב מעבר החום ואיפוס המעקב וההיסטוריה שלו
    def clear_rate_graph(self):
        self.rate_displayed_simulations = []
        self.rate_ax.clear()
        self.style_axes(
            "Heat Transfer Rate vs. Time",
            self.rate_ax,
            self.rate_figure,
            "Heat Transfer Rate (W)",
        )
        self.rate_canvas.draw()
        self.rate_toolbar.update()
        self.rate_toolbar.push_current()

    # ניקוי גרף מעבר החום המצטבר ואיפוס המעקב וההיסטוריה שלו
    def clear_cumulative_graph(self):
        self.cumulative_displayed_simulations = []
        self.cumulative_ax.clear()
        self.style_axes(
            "Cumulative Heat Transfer vs. Time",
            self.cumulative_ax,
            self.cumulative_figure,
            "Transferred Energy (kJ)",
        )
        self.cumulative_canvas.draw()
        self.cumulative_toolbar.update()
        self.cumulative_toolbar.push_current()

    # ניקוי הגרף המוצג בלשונית הפעילה בלבד
    def clear_graph(self):
        current_tab = self.graph_tabs.currentIndex()
        if current_tab == 0:
            self.clear_temperature_graph()
        elif current_tab == 1:
            self.clear_rate_graph()
        elif current_tab == 2:
            self.clear_cumulative_graph()

    # ניקוי גרף הטמפרטורה בלבד בעת החלפת סימולציה ושמירת גרפי ההשוואה
    def simulation_changed(self):
        self.clear_temperature_graph()

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

            # בדיקת הספק חימום משתנה עבור כל גוף בנפרד עם תמיכה בסימולציות קודמות
            is_power1_variable = simulation.get("heating_power1_variable", False)
            is_power2_variable = simulation.get("heating_power2_variable", False)

            power1_text = (
                "Variable"
                if is_power1_variable
                else f"{simulation['heating_power1']:.2f}"
            )
            power2_text = (
                "Variable"
                if is_power2_variable
                else f"{simulation['heating_power2']:.2f}"
            )

            values = [
                f"{simulation['conductance']:.2f}",
                f"{simulation['duration']:.2f}",
                simulation["material1"],
                f"{simulation['initial_temp1']:.2f}",
                f"{simulation['mass1']:.2f}",
                f"{simulation['heat_capacity1']:.2f}",
                power1_text,
                simulation["material2"],
                f"{simulation['initial_temp2']:.2f}",
                f"{simulation['mass2']:.2f}",
                f"{simulation['heat_capacity2']:.2f}",
                power2_text,
            ]

            for row in range(len(values)):
                if row == 1 or row == 6:
                    target_name = (
                        "tableSeparatorValueVariable"
                        if row == 6 and is_power1_variable
                        else "tableSeparatorValue"
                    )
                    existing_label = self.parameters_table.cellWidget(
                        row, column
                    )
                    if existing_label is None:
                        value_label = QLabel(values[row])
                        value_label.setObjectName(target_name)
                        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                        self.parameters_table.setCellWidget(
                            row, column, value_label
                        )
                    else:
                        existing_label.setText(values[row])
                        if existing_label.objectName() != target_name:
                            existing_label.setObjectName(target_name)
                            existing_label.style().unpolish(existing_label)
                            existing_label.style().polish(existing_label)
                else:
                    item = QTableWidgetItem(values[row])
                    item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    if row == 11 and is_power2_variable:
                        item.setForeground(QColor("#B45309"))
                        font = item.font()
                        font.setWeight(QFont.Weight.DemiBold)
                        item.setFont(font)
                    self.parameters_table.setItem(row, column, item)

        # עדכון גובה הטבלה המורחבת אם נוספו עמודות הדורשות פס גלילה אופקי
        if self.parameters_table.isVisible():
            self.update_expanded_table_height()

    # מעבר בין מצב טבלה מקופלת (גרף מרבי + משוואה) למצב טבלה מורחבת (כל 12 השורות)
    def toggle_parameters_table(self):
        is_visible = not self.parameters_table.isVisible()
        self.parameters_table.setVisible(is_visible)
        self.table_divider.setVisible(is_visible)
        self.equation_section.setVisible(not is_visible)

        if is_visible:
            self.table_card.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
            )
            self.update_expanded_table_height()
            self.main_layout.setStretch(1, 1)
            self.main_layout.setStretch(2, 2)
            self.toggle_table_button.setText("Hide Simulation Parameters ▲")
        else:
            self.table_card.setMaximumHeight(16777215)
            self.table_card.setSizePolicy(
                QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum
            )
            self.main_layout.setStretch(1, 1)
            self.main_layout.setStretch(2, 0)
            self.toggle_table_button.setText("Show Simulation Parameters ▼")
            self.update_equation_display(self.graph_tabs.currentIndex())

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
