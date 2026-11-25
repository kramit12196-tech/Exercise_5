# יצירת ממשק המשתמש עם רכיבי PySide6
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import (
    QApplication,
    QComboBox,
    QDoubleSpinBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from About import AboutWindow
from Graph import GraphWindow
from Body import Body
from HeatFlow import HeatFlowWidget
from Heater import HeaterWidget

class HeatTransfer(QWidget):
    # אתחול החלון הראשי
    def __init__(self):
        super().__init__()
        self.about_window = AboutWindow()
        self.graph_window = GraphWindow(self)
        
        self.dt = 0.1  # הגדרת פרק הזמן בין עדכוני הטמפרטורה
        self.elapsed_time = 0.0
        self.temperature_tolerance = 0.1
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timer_method)

        self.body1_temperature = 200.0
        self.body2_temperature = 0.0

        # הגדרת קיבולי החום הסגוליים של החומרים הקבועים
        self.materials = {
            "Aluminum": 900.0,
            "Copper": 387.0,
            "Iron / Steel": 452.0,
            "Brass": 380.0,
            "Glass": 840.0,
        }
        
        # הגדרת מרווחי הטיימר במילישניות לפי מהירות הסימולציה
        self.speed_intervals = {
            "1x": 100,
            "2x": 50,
            "5x": 20,
            "10x": 10,
            "20x": 5,
            "50x": 2,
            "100x": 1,
        }
        self.timer_interval = 100
        self.timer.setInterval(self.timer_interval)
        
        self.setupUI()

        # יצירת רשימות לשמירת נתוני הסימולציה
        self.time_history = []
        self.body1_temp_history = []
        self.body2_temp_history = []
        self.simulation_history = []

    # בניית ממשק המשתמש
    def setupUI(self):
        self.setObjectName("mainWindow")
        self.setWindowTitle("Heat Transfer Simulation")
        self.resize(1110, 750)

        # יצירת כרטיס הכותרת העליון וכפתור אודות
        self.header_card = QWidget()
        self.header_card.setObjectName("headerCard")

        self.title_label = QLabel("Heat Transfer Simulation")
        self.title_label.setObjectName("headerTitle")

        self.subtitle_label = QLabel("Thermal Analysis Tool")
        self.subtitle_label.setObjectName("headerSubtitle")

        header_text_layout = QVBoxLayout()
        header_text_layout.setContentsMargins(0, 0, 0, 0)
        header_text_layout.setSpacing(2)
        header_text_layout.addWidget(self.title_label)
        header_text_layout.addWidget(self.subtitle_label)

        self.about_button = QPushButton("About")
        self.about_button.setObjectName("aboutButton")
        self.about_button.setFixedSize(84, 34)
        self.about_button.clicked.connect(self.open_about)

        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(18, 14, 18, 14)
        header_layout.addLayout(header_text_layout)
        header_layout.addStretch()
        header_layout.addWidget(self.about_button)
        self.header_card.setLayout(header_layout)

        # יצירת כרטיס המערכת התרמית העליון
        self.thermal_card = QWidget()
        self.thermal_card.setObjectName("thermalCard")

        self.thermal_section_title = QLabel("Thermal System")
        self.thermal_section_title.setObjectName("sectionTitle")

        self.status_label = QLabel("Ready")
        self.status_label.setObjectName("statusLabel")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        thermal_header_layout = QHBoxLayout()
        thermal_header_layout.addWidget(self.thermal_section_title)
        thermal_header_layout.addStretch()
        thermal_header_layout.addWidget(self.status_label)

        thermal_divider = QWidget()
        thermal_divider.setObjectName("dividerLine")
        thermal_divider.setFixedHeight(1)

        # יצירת הגוף הראשון והסליידר שלו
        self.body1_title = QLabel("Body 1 (Custom)")
        self.body1_title.setObjectName("bodyTitle")
        self.body1_title.setFixedSize(155, 40)
        self.body1_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body1_title.setWordWrap(True)

        self.body1_visual = QLabel("200.00 °C")
        self.body1_visual.setObjectName("bodyVisual")
        self.body1_visual.setFixedSize(155, 120)
        self.body1_visual.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body1_visual.setStyleSheet(
            "background-color: rgb(255, 0, 0); color: #FFFFFF; font-size: 21px; font-weight: bold; border-radius: 6px;"
        )

        # יצירת מבער חימום מונפש מתחת לגוף הראשון
        self.body1_heater = HeaterWidget()

        self.body1_slider_label = QLabel("Initial Temperature")
        self.body1_slider_label.setObjectName("secondaryLabel")
        self.body1_slider_label.setFixedSize(105, 40)
        self.body1_slider_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body1_slider_label.setWordWrap(True)

        self.body1_temperature_slider = QSlider(Qt.Orientation.Vertical)
        self.body1_temperature_slider.setFixedSize(24, 120)
        self.body1_temperature_slider.setRange(0, 200)
        self.body1_temperature_slider.setValue(200)

        # סידור תצוגת הגוף הראשון, המבער והסליידר
        body1_visual_layout = QVBoxLayout()
        body1_visual_layout.setSpacing(4)
        body1_visual_layout.addWidget(self.body1_title)
        body1_visual_layout.addWidget(self.body1_visual)
        body1_visual_layout.addWidget(self.body1_heater)
        body1_visual_layout.addStretch()

        body1_slider_row = QHBoxLayout()
        body1_slider_row.addStretch()
        body1_slider_row.addWidget(self.body1_temperature_slider)
        body1_slider_row.addStretch()

        body1_slider_layout = QVBoxLayout()
        body1_slider_layout.setSpacing(6)
        body1_slider_layout.addWidget(self.body1_slider_label)
        body1_slider_layout.addLayout(body1_slider_row)
        body1_slider_layout.addStretch()

        # יצירת פקד המוליכות והמוט המחבר המונפש
        self.conductance_label = QLabel("Thermal Conductance")
        self.conductance_label.setObjectName("secondaryLabel")
        self.conductance_label.setFixedSize(200, 22)
        self.conductance_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.conductance_input = QDoubleSpinBox()
        self.conductance_input.setFixedSize(140, 34)
        self.conductance_input.setMinimum(0.01)
        self.conductance_input.setValue(1.00)
        self.conductance_input.setSuffix(" W/°C")
        self.conductance_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.conductance_input.setButtonSymbols(
            QDoubleSpinBox.ButtonSymbols.NoButtons
        )

        conductance_input_layout = QHBoxLayout()
        conductance_input_layout.setSpacing(6)
        conductance_input_layout.addStretch()
        conductance_input_layout.addWidget(self.conductance_input)
        conductance_input_layout.addStretch()

        self.connector = HeatFlowWidget()

        # יצירת תצוגת קצב מעבר החום ועוצמתו מתחת למוט המחבר
        self.heat_rate_title = QLabel("Heat Transfer Rate")
        self.heat_rate_title.setObjectName("heatRateTitle")
        self.heat_rate_title.setFixedSize(200, 16)
        self.heat_rate_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.heat_rate_value = QLabel("0.00 W")
        self.heat_rate_value.setObjectName("heatRateValue")
        self.heat_rate_value.setFixedSize(200, 24)
        self.heat_rate_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.heat_rate_strength = QLabel("Simulation Stopped")
        self.heat_rate_strength.setObjectName("heatRateStrength")
        self.heat_rate_strength.setFixedSize(200, 18)
        self.heat_rate_strength.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # סידור אזור המוליכות, המוט המונפש ותצוגת קצב מעבר החום בין הגופים
        center_upper_layout = QVBoxLayout()
        center_upper_layout.setSpacing(4)
        center_upper_layout.addSpacing(8)
        center_upper_layout.addWidget(self.conductance_label)
        center_upper_layout.addLayout(conductance_input_layout)
        center_upper_layout.addSpacing(18)
        center_upper_layout.addWidget(self.connector)
        center_upper_layout.addSpacing(10)
        center_upper_layout.addWidget(self.heat_rate_title)
        center_upper_layout.addWidget(self.heat_rate_value)
        center_upper_layout.addWidget(self.heat_rate_strength)
        center_upper_layout.addStretch()

        # יצירת הגוף השני והסליידר שלו
        self.body2_title = QLabel("Body 2 (Custom)")
        self.body2_title.setObjectName("bodyTitle")
        self.body2_title.setFixedSize(155, 40)
        self.body2_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body2_title.setWordWrap(True)

        self.body2_visual = QLabel("0.00 °C")
        self.body2_visual.setObjectName("bodyVisual")
        self.body2_visual.setFixedSize(155, 120)
        self.body2_visual.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body2_visual.setStyleSheet(
            "background-color: rgb(0, 0, 0); color: #FFFFFF; font-size: 21px; font-weight: bold; border-radius: 6px;"
        )

        # יצירת מבער חימום מונפש מתחת לגוף השני
        self.body2_heater = HeaterWidget()

        self.body2_slider_label = QLabel("Initial Temperature")
        self.body2_slider_label.setObjectName("secondaryLabel")
        self.body2_slider_label.setFixedSize(105, 40)
        self.body2_slider_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body2_slider_label.setWordWrap(True)

        self.body2_temperature_slider = QSlider(Qt.Orientation.Vertical)
        self.body2_temperature_slider.setFixedSize(24, 120)
        self.body2_temperature_slider.setRange(0, 200)
        self.body2_temperature_slider.setValue(0)

        # סידור תצוגת הגוף השני, המבער והסליידר
        body2_visual_layout = QVBoxLayout()
        body2_visual_layout.setSpacing(4)
        body2_visual_layout.addWidget(self.body2_title)
        body2_visual_layout.addWidget(self.body2_visual)
        body2_visual_layout.addWidget(self.body2_heater)
        body2_visual_layout.addStretch()

        body2_slider_row = QHBoxLayout()
        body2_slider_row.addStretch()
        body2_slider_row.addWidget(self.body2_temperature_slider)
        body2_slider_row.addStretch()

        body2_slider_layout = QVBoxLayout()
        body2_slider_layout.setSpacing(6)
        body2_slider_layout.addWidget(self.body2_slider_label)
        body2_slider_layout.addLayout(body2_slider_row)
        body2_slider_layout.addStretch()

        # סידור שני הגופים והמחבר ביניהם בתוך כרטיס המערכת התרמית
        bodies_bridge_layout = QHBoxLayout()
        bodies_bridge_layout.setSpacing(0)
        bodies_bridge_layout.addLayout(body1_visual_layout)
        bodies_bridge_layout.addLayout(center_upper_layout)
        bodies_bridge_layout.addLayout(body2_visual_layout)

        upper_layout = QHBoxLayout()
        upper_layout.addStretch()
        upper_layout.addLayout(body1_slider_layout)
        upper_layout.addSpacing(24)
        upper_layout.addLayout(bodies_bridge_layout)
        upper_layout.addSpacing(24)
        upper_layout.addLayout(body2_slider_layout)
        upper_layout.addStretch()

        thermal_card_layout = QVBoxLayout()
        thermal_card_layout.setContentsMargins(16, 12, 16, 16)
        thermal_card_layout.setSpacing(10)
        thermal_card_layout.addLayout(thermal_header_layout)
        thermal_card_layout.addWidget(thermal_divider)
        thermal_card_layout.addLayout(upper_layout)
        self.thermal_card.setLayout(thermal_card_layout)

        # יצירת כרטיס הפרמטרים של הגוף הראשון
        self.body1_card = QWidget()
        self.body1_card.setObjectName("body1Card")
        self.body1_card.setFixedWidth(362)

        self.body1_parameters_title = QLabel("Body 1 (Custom) Parameters")
        self.body1_parameters_title.setObjectName("cardTitle")
        self.body1_parameters_title.setFixedHeight(28)
        self.body1_parameters_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        body1_divider = QWidget()
        body1_divider.setObjectName("dividerLine")
        body1_divider.setFixedHeight(1)

        self.body1_material_label = QLabel("Material")
        self.body1_material_label.setObjectName("paramLabel")
        self.body1_temperature_label = QLabel("Temperature")
        self.body1_temperature_label.setObjectName("paramLabel")
        self.body1_temperature_display = QLabel("200.00 °C")
        self.body1_temperature_display.setObjectName("tempDisplay")
        self.body1_mass_label = QLabel("Mass")
        self.body1_mass_label.setObjectName("paramLabel")
        self.body1_heat_capacity_label = QLabel("Specific Heat Capacity")
        self.body1_heat_capacity_label.setObjectName("paramLabel")

        self.body1_material_label.setFixedSize(155, 34)
        self.body1_material_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.body1_temperature_label.setFixedSize(155, 34)
        self.body1_temperature_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.body1_temperature_display.setFixedSize(132, 34)
        self.body1_temperature_display.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # יצירת מחוון מגמת הטמפרטורה של הגוף הראשון
        self.body1_temperature_trend = QLabel("–")
        self.body1_temperature_trend.setObjectName("tempTrend")
        self.body1_temperature_trend.setFixedSize(24, 34)
        self.body1_temperature_trend.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body1_mass_label.setFixedSize(155, 34)
        self.body1_mass_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.body1_heat_capacity_label.setFixedSize(155, 34)
        self.body1_heat_capacity_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )

        # יצירת פקדי הקלט ובחירת החומר של הגוף הראשון
        self.body1_material_selector = QComboBox()
        self.body1_material_selector.setFixedSize(160, 34)
        self.body1_material_selector.addItems(
            ["Custom", "Aluminum", "Copper", "Iron / Steel", "Brass", "Glass"]
        )
        self.body1_material_selector.setCurrentText("Custom")

        self.body1_mass_input = QDoubleSpinBox()
        self.body1_mass_input.setFixedSize(160, 34)
        self.body1_mass_input.setMinimum(0.01)
        self.body1_mass_input.setValue(10.0)
        self.body1_mass_input.setSuffix(" kg")
        self.body1_mass_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body1_mass_input.setButtonSymbols(
            QDoubleSpinBox.ButtonSymbols.NoButtons
        )

        self.body1_heat_capacity_input = QDoubleSpinBox()
        self.body1_heat_capacity_input.setFixedSize(160, 34)
        self.body1_heat_capacity_input.setMinimum(0.0)
        self.body1_heat_capacity_input.setMaximum(10000.0)
        self.body1_heat_capacity_input.setValue(0.40)
        self.body1_heat_capacity_input.setSuffix(" J/(kg·°C)")
        self.body1_heat_capacity_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body1_heat_capacity_input.setButtonSymbols(
            QDoubleSpinBox.ButtonSymbols.NoButtons
        )

        # יצירת פקד הספק החימום של הגוף הראשון
        self.body1_heating_power_label = QLabel("Heating Power")
        self.body1_heating_power_label.setObjectName("paramLabel")
        self.body1_heating_power_label.setFixedSize(155, 34)
        self.body1_heating_power_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )

        self.body1_heating_power_input = QDoubleSpinBox()
        self.body1_heating_power_input.setFixedSize(160, 34)
        self.body1_heating_power_input.setMinimum(0.0)
        self.body1_heating_power_input.setMaximum(1000.0)
        self.body1_heating_power_input.setValue(0.0)
        self.body1_heating_power_input.setSuffix(" W")
        self.body1_heating_power_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body1_heating_power_input.setButtonSymbols(
            QDoubleSpinBox.ButtonSymbols.NoButtons
        )

        # סידור שורות הנתונים של הגוף הראשון בתוך הכרטיס
        body1_material_layout = QHBoxLayout()
        body1_material_layout.setSpacing(10)
        body1_material_layout.addWidget(self.body1_material_label)
        body1_material_layout.addWidget(self.body1_material_selector)

        body1_temp_value_layout = QHBoxLayout()
        body1_temp_value_layout.setContentsMargins(0, 0, 0, 0)
        body1_temp_value_layout.setSpacing(4)
        body1_temp_value_layout.addWidget(self.body1_temperature_display)
        body1_temp_value_layout.addWidget(self.body1_temperature_trend)

        body1_temperature_layout = QHBoxLayout()
        body1_temperature_layout.setSpacing(10)
        body1_temperature_layout.addWidget(self.body1_temperature_label)
        body1_temperature_layout.addLayout(body1_temp_value_layout)

        body1_mass_layout = QHBoxLayout()
        body1_mass_layout.setSpacing(10)
        body1_mass_layout.addWidget(self.body1_mass_label)
        body1_mass_layout.addWidget(self.body1_mass_input)

        body1_heat_capacity_layout = QHBoxLayout()
        body1_heat_capacity_layout.setSpacing(10)
        body1_heat_capacity_layout.addWidget(self.body1_heat_capacity_label)
        body1_heat_capacity_layout.addWidget(self.body1_heat_capacity_input)

        body1_heating_power_layout = QHBoxLayout()
        body1_heating_power_layout.setSpacing(10)
        body1_heating_power_layout.addWidget(self.body1_heating_power_label)
        body1_heating_power_layout.addWidget(self.body1_heating_power_input)

        body1_layout = QVBoxLayout()
        body1_layout.setContentsMargins(16, 14, 16, 16)
        body1_layout.setSpacing(10)
        body1_layout.addWidget(self.body1_parameters_title)
        body1_layout.addWidget(body1_divider)
        body1_layout.addLayout(body1_material_layout)
        body1_layout.addLayout(body1_temperature_layout)
        body1_layout.addLayout(body1_mass_layout)
        body1_layout.addLayout(body1_heat_capacity_layout)
        body1_layout.addLayout(body1_heating_power_layout)
        body1_layout.addStretch()
        self.body1_card.setLayout(body1_layout)

        # יצירת כרטיס השליטה המרכזי
        self.controls_card = QWidget()
        self.controls_card.setObjectName("controlsCard")

        self.controls_title = QLabel("Simulation Controls")
        self.controls_title.setObjectName("cardTitle")
        self.controls_title.setFixedHeight(28)
        self.controls_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        controls_divider = QWidget()
        controls_divider.setObjectName("dividerLine")
        controls_divider.setFixedHeight(1)

        # יצירת תצוגת זמן הסימולציה ובחירת המהירות בשורה אחת
        self.simulation_time_title = QLabel("Simulation Time")
        self.simulation_time_title.setObjectName("secondaryLabel")
        self.simulation_time_title.setFixedSize(145, 22)
        self.simulation_time_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.simulation_time_display = QLabel("0.0 s")
        self.simulation_time_display.setObjectName("timeDisplay")
        self.simulation_time_display.setFixedSize(145, 42)
        self.simulation_time_display.setAlignment(Qt.AlignmentFlag.AlignCenter)

        simulation_time_layout = QVBoxLayout()
        simulation_time_layout.setSpacing(4)
        simulation_time_layout.addWidget(self.simulation_time_title)
        simulation_time_layout.addWidget(self.simulation_time_display)

        self.simulation_speed_title = QLabel("Speed")
        self.simulation_speed_title.setObjectName("secondaryLabel")
        self.simulation_speed_title.setFixedSize(75, 22)
        self.simulation_speed_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.simulation_speed_selector = QComboBox()
        self.simulation_speed_selector.setFixedSize(72, 36)
        self.simulation_speed_selector.addItems(
            ["1x", "2x", "5x", "10x", "20x", "50x", "100x"]
        )
        self.simulation_speed_selector.setCurrentText("1x")
        self.simulation_speed_selector.currentTextChanged.connect(
            self.simulation_speed_changed
        )

        simulation_speed_selector_row = QHBoxLayout()
        simulation_speed_selector_row.addStretch()
        simulation_speed_selector_row.addWidget(self.simulation_speed_selector)
        simulation_speed_selector_row.addStretch()

        simulation_speed_layout = QVBoxLayout()
        simulation_speed_layout.setSpacing(4)
        simulation_speed_layout.addWidget(self.simulation_speed_title)
        simulation_speed_layout.addSpacing(3)
        simulation_speed_layout.addLayout(simulation_speed_selector_row)
        simulation_speed_layout.addSpacing(3)

        time_speed_row_layout = QHBoxLayout()
        time_speed_row_layout.setSpacing(12)
        time_speed_row_layout.addStretch()
        time_speed_row_layout.addLayout(simulation_time_layout)
        time_speed_row_layout.addLayout(simulation_speed_layout)
        time_speed_row_layout.addStretch()

        # יצירת כפתורי השליטה המרכזיים מתחת לשורת הזמן והמהירות
        self.start_button = QPushButton("Start")
        self.start_button.setObjectName("startButton")
        self.start_button.setFixedSize(220, 40)
        self.start_button.setCheckable(True)
        self.start_button.toggled.connect(self.start_stop_button_method)

        start_row_layout = QHBoxLayout()
        start_row_layout.addStretch()
        start_row_layout.addWidget(self.start_button)
        start_row_layout.addStretch()

        self.graphs_button = QPushButton("Graphs")
        self.graphs_button.setObjectName("secondaryButton")
        self.graphs_button.setFixedSize(220, 40)
        self.graphs_button.clicked.connect(self.open_graphs)

        graphs_row_layout = QHBoxLayout()
        graphs_row_layout.addStretch()
        graphs_row_layout.addWidget(self.graphs_button)
        graphs_row_layout.addStretch()

        self.reset_button = QPushButton("Reset Defaults")
        self.reset_button.setObjectName("secondaryButton")
        self.reset_button.setFixedSize(220, 40)
        self.reset_button.clicked.connect(self.reset_defaults)

        reset_row_layout = QHBoxLayout()
        reset_row_layout.addStretch()
        reset_row_layout.addWidget(self.reset_button)
        reset_row_layout.addStretch()

        # סידור האזור המרכזי בתוך כרטיס הבקרה
        center_layout = QVBoxLayout()
        center_layout.setContentsMargins(16, 14, 16, 16)
        center_layout.setSpacing(10)
        center_layout.addWidget(self.controls_title)
        center_layout.addWidget(controls_divider)
        center_layout.addSpacing(4)
        center_layout.addLayout(time_speed_row_layout)
        center_layout.addSpacing(8)
        center_layout.addLayout(start_row_layout)
        center_layout.addLayout(graphs_row_layout)
        center_layout.addLayout(reset_row_layout)
        center_layout.addStretch()
        self.controls_card.setLayout(center_layout)

        # יצירת כרטיס הפרמטרים של הגוף השני
        self.body2_card = QWidget()
        self.body2_card.setObjectName("body2Card")
        self.body2_card.setFixedWidth(362)

        self.body2_parameters_title = QLabel("Body 2 (Custom) Parameters")
        self.body2_parameters_title.setObjectName("cardTitle")
        self.body2_parameters_title.setFixedHeight(28)
        self.body2_parameters_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        body2_divider = QWidget()
        body2_divider.setObjectName("dividerLine")
        body2_divider.setFixedHeight(1)

        self.body2_material_label = QLabel("Material")
        self.body2_material_label.setObjectName("paramLabel")
        self.body2_temperature_label = QLabel("Temperature")
        self.body2_temperature_label.setObjectName("paramLabel")
        self.body2_temperature_display = QLabel("0.00 °C")
        self.body2_temperature_display.setObjectName("tempDisplay")
        self.body2_mass_label = QLabel("Mass")
        self.body2_mass_label.setObjectName("paramLabel")
        self.body2_heat_capacity_label = QLabel("Specific Heat Capacity")
        self.body2_heat_capacity_label.setObjectName("paramLabel")

        self.body2_material_label.setFixedSize(155, 34)
        self.body2_material_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.body2_temperature_label.setFixedSize(155, 34)
        self.body2_temperature_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.body2_temperature_display.setFixedSize(132, 34)
        self.body2_temperature_display.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # יצירת מחוון מגמת הטמפרטורה של הגוף השני
        self.body2_temperature_trend = QLabel("–")
        self.body2_temperature_trend.setObjectName("tempTrend")
        self.body2_temperature_trend.setFixedSize(24, 34)
        self.body2_temperature_trend.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body2_mass_label.setFixedSize(155, 34)
        self.body2_mass_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.body2_heat_capacity_label.setFixedSize(155, 34)
        self.body2_heat_capacity_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )

        # יצירת פקדי הקלט ובחירת החומר של הגוף השני
        self.body2_material_selector = QComboBox()
        self.body2_material_selector.setFixedSize(160, 34)
        self.body2_material_selector.addItems(
            ["Custom", "Aluminum", "Copper", "Iron / Steel", "Brass", "Glass"]
        )
        self.body2_material_selector.setCurrentText("Custom")

        self.body2_mass_input = QDoubleSpinBox()
        self.body2_mass_input.setFixedSize(160, 34)
        self.body2_mass_input.setMinimum(0.01)
        self.body2_mass_input.setValue(10.0)
        self.body2_mass_input.setSuffix(" kg")
        self.body2_mass_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body2_mass_input.setButtonSymbols(
            QDoubleSpinBox.ButtonSymbols.NoButtons
        )

        self.body2_heat_capacity_input = QDoubleSpinBox()
        self.body2_heat_capacity_input.setFixedSize(160, 34)
        self.body2_heat_capacity_input.setMinimum(0.0)
        self.body2_heat_capacity_input.setMaximum(10000.0)
        self.body2_heat_capacity_input.setValue(0.40)
        self.body2_heat_capacity_input.setSuffix(" J/(kg·°C)")
        self.body2_heat_capacity_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body2_heat_capacity_input.setButtonSymbols(
            QDoubleSpinBox.ButtonSymbols.NoButtons
        )

        # יצירת פקד הספק החימום של הגוף השני
        self.body2_heating_power_label = QLabel("Heating Power")
        self.body2_heating_power_label.setObjectName("paramLabel")
        self.body2_heating_power_label.setFixedSize(155, 34)
        self.body2_heating_power_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )

        self.body2_heating_power_input = QDoubleSpinBox()
        self.body2_heating_power_input.setFixedSize(160, 34)
        self.body2_heating_power_input.setMinimum(0.0)
        self.body2_heating_power_input.setMaximum(1000.0)
        self.body2_heating_power_input.setValue(0.0)
        self.body2_heating_power_input.setSuffix(" W")
        self.body2_heating_power_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body2_heating_power_input.setButtonSymbols(
            QDoubleSpinBox.ButtonSymbols.NoButtons
        )

        # סידור שורות הנתונים של הגוף השני בתוך הכרטיס
        body2_material_layout = QHBoxLayout()
        body2_material_layout.setSpacing(10)
        body2_material_layout.addWidget(self.body2_material_label)
        body2_material_layout.addWidget(self.body2_material_selector)

        body2_temp_value_layout = QHBoxLayout()
        body2_temp_value_layout.setContentsMargins(0, 0, 0, 0)
        body2_temp_value_layout.setSpacing(4)
        body2_temp_value_layout.addWidget(self.body2_temperature_display)
        body2_temp_value_layout.addWidget(self.body2_temperature_trend)

        body2_temperature_layout = QHBoxLayout()
        body2_temperature_layout.setSpacing(10)
        body2_temperature_layout.addWidget(self.body2_temperature_label)
        body2_temperature_layout.addLayout(body2_temp_value_layout)

        body2_mass_layout = QHBoxLayout()
        body2_mass_layout.setSpacing(10)
        body2_mass_layout.addWidget(self.body2_mass_label)
        body2_mass_layout.addWidget(self.body2_mass_input)

        body2_heat_capacity_layout = QHBoxLayout()
        body2_heat_capacity_layout.setSpacing(10)
        body2_heat_capacity_layout.addWidget(self.body2_heat_capacity_label)
        body2_heat_capacity_layout.addWidget(self.body2_heat_capacity_input)

        body2_heating_power_layout = QHBoxLayout()
        body2_heating_power_layout.setSpacing(10)
        body2_heating_power_layout.addWidget(self.body2_heating_power_label)
        body2_heating_power_layout.addWidget(self.body2_heating_power_input)

        body2_layout = QVBoxLayout()
        body2_layout.setContentsMargins(16, 14, 16, 16)
        body2_layout.setSpacing(10)
        body2_layout.addWidget(self.body2_parameters_title)
        body2_layout.addWidget(body2_divider)
        body2_layout.addLayout(body2_material_layout)
        body2_layout.addLayout(body2_temperature_layout)
        body2_layout.addLayout(body2_mass_layout)
        body2_layout.addLayout(body2_heat_capacity_layout)
        body2_layout.addLayout(body2_heating_power_layout)
        body2_layout.addStretch()
        self.body2_card.setLayout(body2_layout)

        # סידור שלושת הכרטיסים התחתונים בחלון
        lower_layout = QHBoxLayout()
        lower_layout.setSpacing(14)
        lower_layout.addWidget(self.body1_card)
        lower_layout.addWidget(self.controls_card, 1)
        lower_layout.addWidget(self.body2_card)

        # סידור הפריסה הראשית של החלון
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(14)
        main_layout.addWidget(self.header_card)
        main_layout.addWidget(self.thermal_card)
        main_layout.addLayout(lower_layout)
        self.setLayout(main_layout)

        # חיבור הסליידרים למתודות עדכון הטמפרטורה
        self.body1_temperature_slider.valueChanged.connect(self.left_temperature_changed)
        self.body2_temperature_slider.valueChanged.connect(self.right_temperature_changed)

        # חיבור בחירת החומרים לעדכון קיבול החום הסגולי
        self.body1_material_selector.currentTextChanged.connect(self.body1_material_changed)
        self.body2_material_selector.currentTextChanged.connect(self.body2_material_changed)

        # חיבור שדות קיבול החום הסגולי לבדיקת תקינות כפתור ההפעלה
        self.body1_heat_capacity_input.valueChanged.connect(self.update_start_button_state)
        self.body2_heat_capacity_input.valueChanged.connect(self.update_start_button_state)

        # חיבור שדות הספק החימום לעדכון חיווי גופי החימום
        self.body1_heating_power_input.valueChanged.connect(self.body1_heating_power_changed)
        self.body2_heating_power_input.valueChanged.connect(self.body2_heating_power_changed)

    # עדכון מהירות הסימולציה באמצעות שינוי מרווח הטיימר
    def simulation_speed_changed(self, speed):
        self.timer_interval = self.speed_intervals[speed]
        if self.timer.isActive():
            self.timer.setInterval(self.timer_interval)

    # עדכון הספק החימום המוגדר ברכיב המבער של הגוף הראשון
    def body1_heating_power_changed(self, power):
        self.body1_heater.set_heating_power(power)

    # עדכון הספק החימום המוגדר ברכיב המבער של הגוף השני
    def body2_heating_power_changed(self, power):
        self.body2_heater.set_heating_power(power)

    # עדכון תצוגת קצב מעבר החום, קטגוריית העוצמה ורכיב האנימציה
    def update_heat_flow_display(self, q_rate, is_running):
        self.connector.set_heat_flow(q_rate)

        if not is_running:
            self.heat_rate_value.setText("0.00 W")
            self.heat_rate_strength.setText("Simulation Stopped")
            self.heat_rate_strength.setStyleSheet(
                "color: #64748B; font-size: 11px; font-weight: 600;"
            )
            return

        magnitude = abs(q_rate)
        strength_text = self.connector.get_strength_text()
        self.heat_rate_value.setText(f"{magnitude:.2f} W")
        self.heat_rate_strength.setText(strength_text)

        if magnitude < 0.5:
            color = "#64748B"
        elif magnitude < 25.0:
            color = "#0D9488"
        elif magnitude < 100.0:
            color = "#D97706"
        else:
            color = "#B45309"

        self.heat_rate_strength.setStyleSheet(
            f"color: {color}; font-size: 11px; font-weight: 600;"
        )

    # עדכון הכותרות וקיבול החום הסגולי של הגוף הראשון לפי החומר שנבחר
    def body1_material_changed(self, material):
        self.body1_title.setText(f"Body 1 ({material})")
        self.body1_parameters_title.setText(f"Body 1 ({material}) Parameters")

        if material == "Custom":
            self.body1_heat_capacity_input.setReadOnly(False)
            self.body1_heat_capacity_input.setEnabled(True)
            self.body1_heat_capacity_input.setValue(0.0)
        else:
            self.body1_heat_capacity_input.setValue(self.materials[material])
            self.body1_heat_capacity_input.setEnabled(False)

        self.update_start_button_state()

    # עדכון הכותרות וקיבול החום הסגולי של הגוף השני לפי החומר שנבחר
    def body2_material_changed(self, material):
        self.body2_title.setText(f"Body 2 ({material})")
        self.body2_parameters_title.setText(f"Body 2 ({material}) Parameters")

        if material == "Custom":
            self.body2_heat_capacity_input.setReadOnly(False)
            self.body2_heat_capacity_input.setEnabled(True)
            self.body2_heat_capacity_input.setValue(0.0)
        else:
            self.body2_heat_capacity_input.setValue(self.materials[material])
            self.body2_heat_capacity_input.setEnabled(False)

        self.update_start_button_state()

    # עדכון זמינות כפתור ההפעלה ומסגרת תקינות לקיבול החום הסגולי
    def update_start_button_state(self):
        valid_c1 = self.body1_heat_capacity_input.value() > 0
        valid_c2 = self.body2_heat_capacity_input.value() > 0

        # סגנון מסגרת אדומה השומר על הצגת הערך והעריכה ב-QDoubleSpinBox
        invalid_style = (
            "QDoubleSpinBox { border: 2px solid #DC2626; background-color: #FFFFFF; color: #23364D; border-radius: 6px; padding: 0px 4px; font-size: 13px; } "
            "QDoubleSpinBox::up-button, QDoubleSpinBox::down-button { subcontrol-origin: border; width: 0px; border: none; }"
        )

        # הצגת מסגרת אדומה כאשר נבחר Custom והערך אינו תקין
        if self.body1_material_selector.currentText() == "Custom" and not valid_c1:
            self.body1_heat_capacity_input.setStyleSheet(invalid_style)
        else:
            self.body1_heat_capacity_input.setStyleSheet("")

        if self.body2_material_selector.currentText() == "Custom" and not valid_c2:
            self.body2_heat_capacity_input.setStyleSheet(invalid_style)
        else:
            self.body2_heat_capacity_input.setStyleSheet("")

        if self.start_button.isChecked():
            self.start_button.setEnabled(True)
            return

        self.start_button.setEnabled(valid_c1 and valid_c2)

    # עדכון הטמפרטורה והצבע של הגוף השמאלי
    def left_temperature_changed(self, temperature):
        self.body1_temperature = temperature
        temp_text = f"{temperature:.2f} °C"
        self.body1_temperature_display.setText(temp_text)
        self.body1_visual.setText(temp_text)
        red = int(temperature / 200 * 255)
        if red > 255:   # הגבלת ערך הצבע לטווח RGB
            red = 255

        self.body1_visual.setStyleSheet(
            f"background-color: rgb({red}, 0, 0); color: #FFFFFF; font-size: 21px; font-weight: bold; border-radius: 6px;"
        )

    # עדכון הטמפרטורה והצבע של הגוף הימני
    def right_temperature_changed(self, temperature):
        self.body2_temperature = temperature
        temp_text = f"{temperature:.2f} °C"
        self.body2_temperature_display.setText(temp_text)
        self.body2_visual.setText(temp_text)
        red = int(temperature / 200 * 255)
        if red > 255:   # הגבלת ערך הצבע לטווח RGB
            red = 255

        self.body2_visual.setStyleSheet(
            f"background-color: rgb({red}, 0, 0); color: #FFFFFF; font-size: 21px; font-weight: bold; border-radius: 6px;"
        )

        # הפעלה ועצירה של הסימולציה
    def start_stop_button_method(self):

        if self.start_button.isChecked(): # הפעלת הסימולציה
            self.elapsed_time = 0.0
            self.simulation_time_title.setText("Simulation Time")
            self.simulation_time_display.setText("0.0 s")
            
            self.body1 = Body(self.body1_mass_input.value(), self.body1_heat_capacity_input.value(), self.body1_temperature)
            self.body2 = Body(self.body2_mass_input.value(), self.body2_heat_capacity_input.value(), self.body2_temperature)

            self.conductance = self.conductance_input.value()
            
            # שמירת הספקי החימום בתחילת הסימולציה
            self.heating_power1 = self.body1_heating_power_input.value()
            self.heating_power2 = self.body2_heating_power_input.value()

            # שמירת שמות החומרים שנבחרו בתחילת הסימולציה
            self.body1_material = self.body1_material_selector.currentText()
            self.body2_material = self.body2_material_selector.currentText()

            self.start_button.setText("Stop")
            self.status_label.setText("Running")
            self.status_label.setStyleSheet(
                "color: #2871B8; background-color: #DBEAFE; border: 1px solid #93C5FD; border-radius: 10px; padding: 2px 10px; font-size: 12px; font-weight: 600;"
            )

            # אתחול רשימות הנתונים לניסוי חדש
            self.time_history = []
            self.body1_temp_history = []
            self.body2_temp_history = []

            # שמירת נתוני ההתחלה של הסימולציה
            self.time_history.append(0.0)
            self.body1_temp_history.append(self.body1.temperature)
            self.body2_temp_history.append(self.body2.temperature)

            # נעילת פקדי הקלט בזמן הרצת הסימולציה
            self.body1_material_selector.setEnabled(False)
            self.body2_material_selector.setEnabled(False)

            self.body1_temperature_slider.setEnabled(False)
            self.body2_temperature_slider.setEnabled(False)

            self.body1_mass_input.setEnabled(False)
            self.body2_mass_input.setEnabled(False)

            self.body1_heat_capacity_input.setEnabled(False)
            self.body2_heat_capacity_input.setEnabled(False)

            self.body1_heating_power_input.setEnabled(False)
            self.body2_heating_power_input.setEnabled(False)

            self.conductance_input.setEnabled(False)

            # חישוב קיבול החום הכולל של כל גוף
            c1 = self.body1.mass * self.body1.heat_capacity
            c2 = self.body2.mass * self.body2.heat_capacity
            
            max_dt = (c1 * c2) / (self.conductance * (c1 + c2)) # חישוב צעד הזמן המרבי
            
            self.dt = 0.1 # התאמת צעד הזמן לנתוני הסימולציה
            
            if self.dt > max_dt:
                self.dt = max_dt

            self.timer.start(self.timer_interval)

            # חישוב קצב מעבר החום ההתחלתי והפעלת האנימציה
            q_rate = self.conductance * (
                self.body1.temperature - self.body2.temperature
            )
            self.update_heat_flow_display(q_rate, True)
            self.connector.start_animation()
            self.body1_heater.start_animation()
            self.body2_heater.start_animation()

        else:  # עצירת הסימולציה
            self.timer.stop()
            self.reset_temperature_trends()
            self.connector.stop_animation()
            self.body1_heater.stop_animation()
            self.body2_heater.stop_animation()
            self.update_heat_flow_display(0.0, False)
            self.start_button.setText("Start")
            self.status_label.setText("Stopped")
            self.status_label.setStyleSheet(
                "color: #DC2626; background-color: #FEE2E2; border: 1px solid #FCA5A5; border-radius: 10px; padding: 2px 10px; font-size: 12px; font-weight: 600;"
            )
            
            if len(self.time_history) > 0:
                self.save_simulation()

            # שחרור פקדי הקלט לאחר עצירת הסימולציה
            self.body1_material_selector.setEnabled(True)
            self.body2_material_selector.setEnabled(True)

            self.body1_temperature_slider.setEnabled(True)
            self.body2_temperature_slider.setEnabled(True)

            self.body1_mass_input.setEnabled(True)
            self.body2_mass_input.setEnabled(True)

            if self.body1_material_selector.currentText() == "Custom":
                self.body1_heat_capacity_input.setEnabled(True)

            if self.body2_material_selector.currentText() == "Custom":
                self.body2_heat_capacity_input.setEnabled(True)

            self.body1_heating_power_input.setEnabled(True)
            self.body2_heating_power_input.setEnabled(True)

            self.conductance_input.setEnabled(True)
            self.update_start_button_state()

    # עדכון חץ מגמת הטמפרטורה של גוף לפי השינוי הלא מעוגל בצעד הנוכחי
    def update_temperature_trend(self, trend_label, previous_temp, new_temp):
        diff = new_temp - previous_temp
        if diff > 1e-9:
            trend_label.setText("↑")
            trend_label.setStyleSheet(
                "color: #DC2626; font-size: 19px; font-weight: bold;"
            )
        elif diff < -1e-9:
            trend_label.setText("↓")
            trend_label.setStyleSheet(
                "color: #2871B8; font-size: 19px; font-weight: bold;"
            )
        else:
            trend_label.setText("–")
            trend_label.setStyleSheet(
                "color: #94A3B8; font-size: 19px; font-weight: bold;"
            )

    # איפוס שני מחווני מגמת הטמפרטורה לקו אפור ניטרלי
    def reset_temperature_trends(self):
        self.body1_temperature_trend.setText("–")
        self.body1_temperature_trend.setStyleSheet(
            "color: #94A3B8; font-size: 19px; font-weight: bold;"
        )
        self.body2_temperature_trend.setText("–")
        self.body2_temperature_trend.setStyleSheet(
            "color: #94A3B8; font-size: 19px; font-weight: bold;"
        )

    def timer_method(self):
        t1 = self.body1.temperature
        t2 = self.body2.temperature

        # חישוב קצב מעבר החום כולל גופי החימום
        i1 = self.conductance * (t2 - t1) + self.heating_power1
        i2 = self.conductance * (t1 - t2) + self.heating_power2

        q1 = i1 * self.dt
        q2 = i2 * self.dt

        new_t1 = self.body1.add_heat(q1)
        new_t2 = self.body2.add_heat(q2)

        # עדכון מחווני מגמת הטמפרטורה לפי השינוי הלא מעוגל של כל גוף
        self.update_temperature_trend(self.body1_temperature_trend, t1, new_t1)
        self.update_temperature_trend(self.body2_temperature_trend, t2, new_t2)

        # חישוב קצב מעבר החום המוליך (ללא עיגול) ועדכון תצוגת האנימציה
        q_rate = self.conductance * (new_t1 - new_t2)
        self.update_heat_flow_display(q_rate, True)

        self.body1_temperature_slider.setValue(int(new_t1))
        self.body2_temperature_slider.setValue(int(new_t2))

        self.left_temperature_changed(new_t1)
        self.right_temperature_changed(new_t2)

        self.elapsed_time += self.dt
        self.simulation_time_display.setText(f"{self.elapsed_time:.1f} s")

         # שמירת נתוני צעד הזמן הנוכחי
        self.time_history.append(self.elapsed_time)
        self.body1_temp_history.append(new_t1)
        self.body2_temp_history.append(new_t2)

        temperature_difference = new_t1 - new_t2

        # עצירה אוטומטית כאשר גופי החימום כבויים
        if self.heating_power1 == 0 and self.heating_power2 == 0:

            if temperature_difference <= self.temperature_tolerance and temperature_difference >= -self.temperature_tolerance:

                self.start_button.setChecked(False)
                self.simulation_time_title.setText("Equilibrium Time")
                self.status_label.setText("Equilibrium Reached")
                self.status_label.setStyleSheet(
                    "color: #16A34A; background-color: #DCFCE7; border: 1px solid #86EFAC; border-radius: 10px; padding: 2px 10px; font-size: 12px; font-weight: 600;"
                )

    # פתיחת חלון אודות
    def open_about(self):
        self.about_window.show()

    # פתיחת חלון הגרפים
    def open_graphs(self):
        self.graph_window.refresh_simulations()
        self.graph_window.show()

        # שמירת נתוני הסימולציה שהסתיימה
    def save_simulation(self):
        simulation_number = len(self.simulation_history) + 1   # הגדרת מספר הסימולציה

        # שמירת הפרמטרים ותוצאות הסימולציה
        simulation = {
            "number": simulation_number,
            "conductance": self.conductance,

            "material1": self.body1_material,
            "material2": self.body2_material,

            "mass1": self.body1.mass,
            "mass2": self.body2.mass,

            "heat_capacity1": self.body1.heat_capacity,
            "heat_capacity2": self.body2.heat_capacity,

            "heating_power1": self.heating_power1,
            "heating_power2": self.heating_power2,

            "initial_temp1": self.body1_temp_history[0],
            "initial_temp2": self.body2_temp_history[0],

            "duration": self.elapsed_time,

            "time": self.time_history[:],
            "temperature1": self.body1_temp_history[:],
            "temperature2": self.body2_temp_history[:]
        }

        # הוספת הסימולציה להיסטוריה
        self.simulation_history.append(simulation)
        self.graph_window.refresh_simulations()

    # איפוס נתוני הסימולציה לערכי ברירת המחדל
    def reset_defaults(self):

        self.start_button.setChecked(False)  # עצירת הסימולציה

        # איפוס הטמפרטורות
        self.body1_temperature_slider.setValue(200)
        self.body2_temperature_slider.setValue(0)

        # איפוס המסות
        self.body1_mass_input.setValue(10.0)
        self.body2_mass_input.setValue(10.0)

        # איפוס בחירת החומרים והכותרות לברירת המחדל
        self.body1_material_selector.setCurrentText("Custom")
        self.body2_material_selector.setCurrentText("Custom")
        self.body1_material_changed("Custom")
        self.body2_material_changed("Custom")

        # איפוס קיבולי החום הסגוליים
        self.body1_heat_capacity_input.setEnabled(True)
        self.body2_heat_capacity_input.setEnabled(True)
        self.body1_heat_capacity_input.setValue(0.40)
        self.body2_heat_capacity_input.setValue(0.40)
        self.update_start_button_state()

        # איפוס הספקי החימום וחיווי גופי החימום
        self.body1_heating_power_input.setValue(0.0)
        self.body2_heating_power_input.setValue(0.0)
        self.body1_heating_power_changed(0.0)
        self.body2_heating_power_changed(0.0)

        # איפוס מקדם מעבר החום
        self.conductance_input.setValue(1.0)

        # עדכון תצוגת הטמפרטורות והצבעים
        self.left_temperature_changed(200)
        self.right_temperature_changed(0)

        # איפוס זמן, מצב ומהירות הסימולציה
        self.elapsed_time = 0.0
        self.simulation_time_title.setText("Simulation Time")
        self.simulation_time_display.setText("0.0 s")
        self.simulation_speed_selector.setCurrentText("1x")
        self.simulation_speed_changed("1x")
        self.status_label.setText("Ready")
        self.status_label.setStyleSheet("")
        self.reset_temperature_trends()
        self.connector.reset_animation()
        self.body1_heater.reset_animation()
        self.body2_heater.reset_animation()
        self.update_heat_flow_display(0.0, False)

    # עצירת טיימרי האנימציה בעת סגירת החלון הראשי
    def closeEvent(self, event):
        self.connector.stop_animation()
        self.body1_heater.stop_animation()
        self.body2_heater.stop_animation()
        super().closeEvent(event)

# הפעלת החלון הראשי וטעינת קובץ העיצוב
if __name__ == "__main__":
    app = QApplication()
    with open("style.qss", encoding="utf-8") as f:
        app.setStyleSheet(f.read())
    window = HeatTransfer()
    window.show()
    app.exec()
