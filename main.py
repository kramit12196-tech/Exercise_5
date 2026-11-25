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
        self.setWindowTitle("Heat Transfer Simulation")
        self.resize(1040, 585)

        # יצירת הכותרת וכפתור אודות
        self.title_label = QLabel("Heat Transfer Simulation")
        self.about_button = QPushButton("About")
        self.about_button.setFixedSize(80, 30)
        self.about_button.clicked.connect(self.open_about)

        header_layout = QHBoxLayout()
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        header_layout.addWidget(self.about_button)

        # יצירת הגוף הראשון והסליידר שלו
        self.body1_title = QLabel("Body 1 (Custom)")
        self.body1_title.setFixedSize(135, 44)
        self.body1_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body1_title.setWordWrap(True)

        self.body1_visual = QLabel()
        self.body1_visual.setFixedSize(135, 114)
        self.body1_visual.setStyleSheet("background-color: red;")

        # יצירת חיווי גוף החימום מתחת לגוף הראשון
        self.body1_heater_indicator = QLabel("Heater OFF")
        self.body1_heater_indicator.setFixedSize(135, 24)
        self.body1_heater_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body1_heater_indicator.setStyleSheet(
            "background-color: lightgray; border: 1px solid gray;"
        )

        self.body1_slider_label = QLabel("Initial Temperature")
        self.body1_slider_label.setFixedSize(95, 44)
        self.body1_slider_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body1_slider_label.setWordWrap(True)

        self.body1_temperature_slider = QSlider(Qt.Orientation.Vertical)
        self.body1_temperature_slider.setFixedSize(20, 114)
        self.body1_temperature_slider.setRange(0, 200)
        self.body1_temperature_slider.setValue(200)

        # סידור תצוגת הגוף הראשון והסליידר
        body1_visual_layout = QVBoxLayout()
        body1_visual_layout.setSpacing(6)
        body1_visual_layout.addWidget(self.body1_title)
        body1_visual_layout.addWidget(self.body1_visual)
        body1_visual_layout.addWidget(self.body1_heater_indicator)

        body1_slider_row = QHBoxLayout()
        body1_slider_row.addStretch()
        body1_slider_row.addWidget(self.body1_temperature_slider)
        body1_slider_row.addStretch()

        body1_slider_layout = QVBoxLayout()
        body1_slider_layout.setSpacing(6)
        body1_slider_layout.addWidget(self.body1_slider_label)
        body1_slider_layout.addLayout(body1_slider_row)
        body1_slider_layout.addStretch()

        # יצירת פקד המוליכות והמחבר המרכזי
        self.conductance_label = QLabel("Thermal Conductance")
        self.conductance_label.setFixedSize(200, 44)
        self.conductance_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.conductance_input = QDoubleSpinBox()
        self.conductance_input.setFixedSize(135, 30)
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

        self.connector = QLabel()
        self.connector.setFixedSize(200, 22)
        self.connector.setStyleSheet("background-color: gray;")

        # סידור אזור המוליכות והמחבר בין שני הגופים
        center_upper_layout = QVBoxLayout()
        center_upper_layout.setSpacing(6)
        center_upper_layout.addWidget(self.conductance_label)
        center_upper_layout.addLayout(conductance_input_layout)
        center_upper_layout.addSpacing(10)
        center_upper_layout.addWidget(self.connector)
        center_upper_layout.addStretch()

        # יצירת הגוף השני והסליידר שלו
        self.body2_title = QLabel("Body 2 (Custom)")
        self.body2_title.setFixedSize(135, 44)
        self.body2_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body2_title.setWordWrap(True)

        self.body2_visual = QLabel()
        self.body2_visual.setFixedSize(135, 114)
        self.body2_visual.setStyleSheet("background-color: black;")

        # יצירת חיווי גוף החימום מתחת לגוף השני
        self.body2_heater_indicator = QLabel("Heater OFF")
        self.body2_heater_indicator.setFixedSize(135, 24)
        self.body2_heater_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body2_heater_indicator.setStyleSheet(
            "background-color: lightgray; border: 1px solid gray;"
        )

        self.body2_slider_label = QLabel("Initial Temperature")
        self.body2_slider_label.setFixedSize(95, 44)
        self.body2_slider_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body2_slider_label.setWordWrap(True)

        self.body2_temperature_slider = QSlider(Qt.Orientation.Vertical)
        self.body2_temperature_slider.setFixedSize(20, 114)
        self.body2_temperature_slider.setRange(0, 200)
        self.body2_temperature_slider.setValue(0)

        # סידור תצוגת הגוף השני והסליידר
        body2_visual_layout = QVBoxLayout()
        body2_visual_layout.setSpacing(6)
        body2_visual_layout.addWidget(self.body2_title)
        body2_visual_layout.addWidget(self.body2_visual)
        body2_visual_layout.addWidget(self.body2_heater_indicator)

        body2_slider_row = QHBoxLayout()
        body2_slider_row.addStretch()
        body2_slider_row.addWidget(self.body2_temperature_slider)
        body2_slider_row.addStretch()

        body2_slider_layout = QVBoxLayout()
        body2_slider_layout.setSpacing(6)
        body2_slider_layout.addWidget(self.body2_slider_label)
        body2_slider_layout.addLayout(body2_slider_row)
        body2_slider_layout.addStretch()

        # סידור שני הגופים והמחבר ביניהם בחלק העליון
        bodies_bridge_layout = QHBoxLayout()
        bodies_bridge_layout.setSpacing(0)
        bodies_bridge_layout.addLayout(body1_visual_layout)
        bodies_bridge_layout.addLayout(center_upper_layout)
        bodies_bridge_layout.addLayout(body2_visual_layout)

        upper_layout = QHBoxLayout()
        upper_layout.addStretch()
        upper_layout.addLayout(body1_slider_layout)
        upper_layout.addSpacing(20)
        upper_layout.addLayout(bodies_bridge_layout)
        upper_layout.addSpacing(20)
        upper_layout.addLayout(body2_slider_layout)
        upper_layout.addStretch()

        # יצירת כותרת ותוויות הנתונים של הגוף הראשון
        self.body1_parameters_title = QLabel("Body 1 (Custom) Parameters")
        self.body1_parameters_title.setFixedSize(323, 26)
        self.body1_parameters_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.body1_material_label = QLabel("Material")
        self.body1_temperature_label = QLabel("Temperature")
        self.body1_temperature_display = QLabel("200.00 °C")
        self.body1_mass_label = QLabel("Mass")
        self.body1_heat_capacity_label = QLabel("Specific Heat Capacity")

        self.body1_material_label.setFixedSize(155, 30)
        self.body1_material_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.body1_temperature_label.setFixedSize(155, 30)
        self.body1_temperature_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.body1_temperature_display.setFixedSize(160, 30)
        self.body1_temperature_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body1_temperature_display.setStyleSheet(
            "background-color: white; border: 1px solid gray;"
        )
        self.body1_mass_label.setFixedSize(155, 30)
        self.body1_mass_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.body1_heat_capacity_label.setFixedSize(155, 30)
        self.body1_heat_capacity_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )

        # יצירת פקדי הקלט ובחירת החומר של הגוף הראשון
        self.body1_material_selector = QComboBox()
        self.body1_material_selector.setFixedSize(160, 30)
        self.body1_material_selector.addItems(
            ["Custom", "Aluminum", "Copper", "Iron / Steel", "Brass", "Glass"]
        )
        self.body1_material_selector.setCurrentText("Custom")

        self.body1_mass_input = QDoubleSpinBox()
        self.body1_mass_input.setFixedSize(160, 30)
        self.body1_mass_input.setMinimum(0.01)
        self.body1_mass_input.setValue(10.0)
        self.body1_mass_input.setSuffix(" kg")
        self.body1_mass_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body1_mass_input.setButtonSymbols(
            QDoubleSpinBox.ButtonSymbols.NoButtons
        )

        self.body1_heat_capacity_input = QDoubleSpinBox()
        self.body1_heat_capacity_input.setFixedSize(160, 30)
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
        self.body1_heating_power_label.setFixedSize(155, 30)
        self.body1_heating_power_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )

        self.body1_heating_power_input = QDoubleSpinBox()
        self.body1_heating_power_input.setFixedSize(160, 30)
        self.body1_heating_power_input.setMinimum(0.0)
        self.body1_heating_power_input.setMaximum(1000.0)
        self.body1_heating_power_input.setValue(0.0)
        self.body1_heating_power_input.setSuffix(" W")
        self.body1_heating_power_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body1_heating_power_input.setButtonSymbols(
            QDoubleSpinBox.ButtonSymbols.NoButtons
        )

        # סידור שורות הנתונים של הגוף הראשון
        body1_material_layout = QHBoxLayout()
        body1_material_layout.setSpacing(8)
        body1_material_layout.addWidget(self.body1_material_label)
        body1_material_layout.addWidget(self.body1_material_selector)

        body1_temperature_layout = QHBoxLayout()
        body1_temperature_layout.setSpacing(8)
        body1_temperature_layout.addWidget(self.body1_temperature_label)
        body1_temperature_layout.addWidget(self.body1_temperature_display)

        body1_mass_layout = QHBoxLayout()
        body1_mass_layout.setSpacing(8)
        body1_mass_layout.addWidget(self.body1_mass_label)
        body1_mass_layout.addWidget(self.body1_mass_input)

        body1_heat_capacity_layout = QHBoxLayout()
        body1_heat_capacity_layout.setSpacing(8)
        body1_heat_capacity_layout.addWidget(self.body1_heat_capacity_label)
        body1_heat_capacity_layout.addWidget(self.body1_heat_capacity_input)

        body1_heating_power_layout = QHBoxLayout()
        body1_heating_power_layout.setSpacing(8)
        body1_heating_power_layout.addWidget(self.body1_heating_power_label)
        body1_heating_power_layout.addWidget(self.body1_heating_power_input)

        body1_layout = QVBoxLayout()
        body1_layout.setSpacing(10)
        body1_layout.addWidget(self.body1_parameters_title)
        body1_layout.addLayout(body1_material_layout)
        body1_layout.addLayout(body1_temperature_layout)
        body1_layout.addLayout(body1_mass_layout)
        body1_layout.addLayout(body1_heat_capacity_layout)
        body1_layout.addLayout(body1_heating_power_layout)
        body1_layout.addStretch()

        # יצירת תצוגת זמן הסימולציה ובחירת המהירות בשורה אחת
        self.simulation_time_title = QLabel("Simulation Time")
        self.simulation_time_title.setFixedSize(120, 30)
        self.simulation_time_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.simulation_time_display = QLabel("0.0 s")
        self.simulation_time_display.setFixedSize(120, 30)
        self.simulation_time_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.simulation_time_display.setStyleSheet(
            "background-color: white; border: 1px solid gray;"
        )

        simulation_time_layout = QVBoxLayout()
        simulation_time_layout.setSpacing(4)
        simulation_time_layout.addWidget(self.simulation_time_title)
        simulation_time_layout.addWidget(self.simulation_time_display)

        self.simulation_speed_title = QLabel("Simulation Speed")
        self.simulation_speed_title.setFixedSize(75, 30)
        self.simulation_speed_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.simulation_speed_title.setWordWrap(True)

        self.simulation_speed_selector = QComboBox()
        self.simulation_speed_selector.setFixedSize(70, 30)
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
        simulation_speed_layout.addLayout(simulation_speed_selector_row)

        time_speed_row_layout = QHBoxLayout()
        time_speed_row_layout.setSpacing(10)
        time_speed_row_layout.addStretch()
        time_speed_row_layout.addLayout(simulation_time_layout)
        time_speed_row_layout.addLayout(simulation_speed_layout)
        time_speed_row_layout.addStretch()

        # יצירת כפתורי השליטה המרכזיים מתחת לשורת הזמן והמהירות
        self.start_button = QPushButton("Start")
        self.start_button.setFixedSize(145, 38)
        self.start_button.setCheckable(True)
        self.start_button.toggled.connect(self.start_stop_button_method)

        start_row_layout = QHBoxLayout()
        start_row_layout.addStretch()
        start_row_layout.addWidget(self.start_button)
        start_row_layout.addStretch()

        self.graphs_button = QPushButton("Graphs")
        self.graphs_button.setFixedSize(145, 38)
        self.graphs_button.clicked.connect(self.open_graphs)

        graphs_row_layout = QHBoxLayout()
        graphs_row_layout.addStretch()
        graphs_row_layout.addWidget(self.graphs_button)
        graphs_row_layout.addStretch()

        self.reset_button = QPushButton("Reset Defaults")
        self.reset_button.setFixedSize(145, 38)
        self.reset_button.clicked.connect(self.reset_defaults)

        reset_row_layout = QHBoxLayout()
        reset_row_layout.addStretch()
        reset_row_layout.addWidget(self.reset_button)
        reset_row_layout.addStretch()

        # סידור האזור המרכזי
        center_layout = QVBoxLayout()
        center_layout.setSpacing(10)
        center_layout.addSpacing(4)
        center_layout.addLayout(time_speed_row_layout)
        center_layout.addSpacing(4)
        center_layout.addLayout(start_row_layout)
        center_layout.addLayout(graphs_row_layout)
        center_layout.addLayout(reset_row_layout)
        center_layout.addStretch()

        # יצירת כותרת ותוויות הנתונים של הגוף השני
        self.body2_parameters_title = QLabel("Body 2 (Custom) Parameters")
        self.body2_parameters_title.setFixedSize(323, 26)
        self.body2_parameters_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.body2_material_label = QLabel("Material")
        self.body2_temperature_label = QLabel("Temperature")
        self.body2_temperature_display = QLabel("0.00 °C")
        self.body2_mass_label = QLabel("Mass")
        self.body2_heat_capacity_label = QLabel("Specific Heat Capacity")

        self.body2_material_label.setFixedSize(155, 30)
        self.body2_material_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.body2_temperature_label.setFixedSize(155, 30)
        self.body2_temperature_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.body2_temperature_display.setFixedSize(160, 30)
        self.body2_temperature_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body2_temperature_display.setStyleSheet(
            "background-color: white; border: 1px solid gray;"
        )
        self.body2_mass_label.setFixedSize(155, 30)
        self.body2_mass_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.body2_heat_capacity_label.setFixedSize(155, 30)
        self.body2_heat_capacity_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )

        # יצירת פקדי הקלט ובחירת החומר של הגוף השני
        self.body2_material_selector = QComboBox()
        self.body2_material_selector.setFixedSize(160, 30)
        self.body2_material_selector.addItems(
            ["Custom", "Aluminum", "Copper", "Iron / Steel", "Brass", "Glass"]
        )
        self.body2_material_selector.setCurrentText("Custom")

        self.body2_mass_input = QDoubleSpinBox()
        self.body2_mass_input.setFixedSize(160, 30)
        self.body2_mass_input.setMinimum(0.01)
        self.body2_mass_input.setValue(10.0)
        self.body2_mass_input.setSuffix(" kg")
        self.body2_mass_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body2_mass_input.setButtonSymbols(
            QDoubleSpinBox.ButtonSymbols.NoButtons
        )

        self.body2_heat_capacity_input = QDoubleSpinBox()
        self.body2_heat_capacity_input.setFixedSize(160, 30)
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
        self.body2_heating_power_label.setFixedSize(155, 30)
        self.body2_heating_power_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )

        self.body2_heating_power_input = QDoubleSpinBox()
        self.body2_heating_power_input.setFixedSize(160, 30)
        self.body2_heating_power_input.setMinimum(0.0)
        self.body2_heating_power_input.setMaximum(1000.0)
        self.body2_heating_power_input.setValue(0.0)
        self.body2_heating_power_input.setSuffix(" W")
        self.body2_heating_power_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body2_heating_power_input.setButtonSymbols(
            QDoubleSpinBox.ButtonSymbols.NoButtons
        )

        # סידור שורות הנתונים של הגוף השני
        body2_material_layout = QHBoxLayout()
        body2_material_layout.setSpacing(8)
        body2_material_layout.addWidget(self.body2_material_label)
        body2_material_layout.addWidget(self.body2_material_selector)

        body2_temperature_layout = QHBoxLayout()
        body2_temperature_layout.setSpacing(8)
        body2_temperature_layout.addWidget(self.body2_temperature_label)
        body2_temperature_layout.addWidget(self.body2_temperature_display)

        body2_mass_layout = QHBoxLayout()
        body2_mass_layout.setSpacing(8)
        body2_mass_layout.addWidget(self.body2_mass_label)
        body2_mass_layout.addWidget(self.body2_mass_input)

        body2_heat_capacity_layout = QHBoxLayout()
        body2_heat_capacity_layout.setSpacing(8)
        body2_heat_capacity_layout.addWidget(self.body2_heat_capacity_label)
        body2_heat_capacity_layout.addWidget(self.body2_heat_capacity_input)

        body2_heating_power_layout = QHBoxLayout()
        body2_heating_power_layout.setSpacing(8)
        body2_heating_power_layout.addWidget(self.body2_heating_power_label)
        body2_heating_power_layout.addWidget(self.body2_heating_power_input)

        body2_layout = QVBoxLayout()
        body2_layout.setSpacing(10)
        body2_layout.addWidget(self.body2_parameters_title)
        body2_layout.addLayout(body2_material_layout)
        body2_layout.addLayout(body2_temperature_layout)
        body2_layout.addLayout(body2_mass_layout)
        body2_layout.addLayout(body2_heat_capacity_layout)
        body2_layout.addLayout(body2_heating_power_layout)
        body2_layout.addStretch()

        # סידור שלושת החלקים התחתונים בחלון
        lower_layout = QHBoxLayout()
        lower_layout.setSpacing(0)
        lower_layout.addStretch()
        lower_layout.addLayout(body1_layout)
        lower_layout.addSpacing(35)
        lower_layout.addLayout(center_layout)
        lower_layout.addSpacing(35)
        lower_layout.addLayout(body2_layout)
        lower_layout.addStretch()

        # סידור הפריסה הראשית של החלון
        main_layout = QVBoxLayout()
        main_layout.addLayout(header_layout)
        main_layout.addSpacing(10)
        main_layout.addLayout(upper_layout)
        main_layout.addSpacing(28)
        main_layout.addLayout(lower_layout)
        main_layout.addStretch()
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

    # עדכון חיווי גוף החימום של הגוף הראשון
    def body1_heating_power_changed(self, power):
        if power > 0:
            self.body1_heater_indicator.setText("Heater ON")
            self.body1_heater_indicator.setStyleSheet(
                "background-color: orange; border: 1px solid gray;"
            )
        else:
            self.body1_heater_indicator.setText("Heater OFF")
            self.body1_heater_indicator.setStyleSheet(
                "background-color: lightgray; border: 1px solid gray;"
            )

    # עדכון חיווי גוף החימום של הגוף השני
    def body2_heating_power_changed(self, power):
        if power > 0:
            self.body2_heater_indicator.setText("Heater ON")
            self.body2_heater_indicator.setStyleSheet(
                "background-color: orange; border: 1px solid gray;"
            )
        else:
            self.body2_heater_indicator.setText("Heater OFF")
            self.body2_heater_indicator.setStyleSheet(
                "background-color: lightgray; border: 1px solid gray;"
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
            "QDoubleSpinBox { border: 2px solid red; background-color: white; color: black; border-radius: 3px; padding: 0px 2px; } "
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
        self.body1_temperature_display.setText(f"{temperature:.2f} °C")
        red = int(temperature / 200 * 255)
        if red > 255:   # הגבלת ערך הצבע לטווח RGB
            red = 255

        self.body1_visual.setStyleSheet(f"background-color: rgb({red}, 0, 0);")

    # עדכון הטמפרטורה והצבע של הגוף הימני
    def right_temperature_changed(self, temperature):
        self.body2_temperature = temperature
        self.body2_temperature_display.setText(f"{temperature:.2f} °C")
        red = int(temperature / 200 * 255)
        if red > 255:   # הגבלת ערך הצבע לטווח RGB
                    red = 255

        self.body2_visual.setStyleSheet(f"background-color: rgb({red}, 0, 0);")

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

        else:  # עצירת הסימולציה
            self.timer.stop()
            self.start_button.setText("Start")
            
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

        # איפוס זמן ומהירות הסימולציה
        self.elapsed_time = 0.0
        self.simulation_time_title.setText("Simulation Time")
        self.simulation_time_display.setText("0.0 s")
        self.simulation_speed_selector.setCurrentText("1x")
        self.simulation_speed_changed("1x")

# הפעלת החלון הראשי
if __name__ == "__main__":
    app = QApplication()
    window = HeatTransfer()
    window.show()
    app.exec()
