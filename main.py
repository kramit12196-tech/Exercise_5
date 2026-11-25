# יצירת ממשק המשתמש עם רכיבי PySide6
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QDoubleSpinBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSlider,
    QVBoxLayout,
    QWidget,
)

from About import AboutWindow


class HeatTransfer(QWidget):
    # אתחול החלון הראשי
    def __init__(self):
        super().__init__()
        self.about_window = AboutWindow()
        self.setupUI()

    # בניית ממשק המשתמש
    def setupUI(self):
        self.setWindowTitle("Heat Transfer Simulation")
        self.resize(980, 470)

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
        self.body1_title = QLabel("Body 1")
        self.body1_title.setFixedSize(135, 36)
        self.body1_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.body1_visual = QLabel()
        self.body1_visual.setFixedSize(135, 114)
        self.body1_visual.setStyleSheet("background-color: red;")

        self.body1_slider_label = QLabel("Initial Temperature")
        self.body1_slider_label.setFixedSize(95, 36)
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

        body1_slider_row = QHBoxLayout()
        body1_slider_row.addStretch()
        body1_slider_row.addWidget(self.body1_temperature_slider)
        body1_slider_row.addStretch()

        body1_slider_layout = QVBoxLayout()
        body1_slider_layout.setSpacing(6)
        body1_slider_layout.addWidget(self.body1_slider_label)
        body1_slider_layout.addLayout(body1_slider_row)

        # יצירת פקד המוליכות והמחבר המרכזי
        self.conductance_label = QLabel("Thermal Conductance")
        self.conductance_label.setFixedSize(200, 36)
        self.conductance_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.conductance_input = QDoubleSpinBox()
        self.conductance_input.setFixedSize(95, 30)
        self.conductance_input.setMinimum(0.01)
        self.conductance_input.setValue(1.00)
        self.conductance_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.conductance_input.setButtonSymbols(
            QDoubleSpinBox.ButtonSymbols.NoButtons
        )

        self.conductance_unit = QLabel("W/°C")
        self.conductance_unit.setFixedSize(45, 30)

        conductance_input_layout = QHBoxLayout()
        conductance_input_layout.setSpacing(6)
        conductance_input_layout.addStretch()
        conductance_input_layout.addWidget(self.conductance_input)
        conductance_input_layout.addWidget(self.conductance_unit)
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
        self.body2_title = QLabel("Body 2")
        self.body2_title.setFixedSize(135, 36)
        self.body2_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.body2_visual = QLabel()
        self.body2_visual.setFixedSize(135, 114)
        self.body2_visual.setStyleSheet("background-color: black;")

        self.body2_slider_label = QLabel("Initial Temperature")
        self.body2_slider_label.setFixedSize(95, 36)
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

        body2_slider_row = QHBoxLayout()
        body2_slider_row.addStretch()
        body2_slider_row.addWidget(self.body2_temperature_slider)
        body2_slider_row.addStretch()

        body2_slider_layout = QVBoxLayout()
        body2_slider_layout.setSpacing(6)
        body2_slider_layout.addWidget(self.body2_slider_label)
        body2_slider_layout.addLayout(body2_slider_row)

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
        self.body1_parameters_title = QLabel("Body 1 Parameters")
        self.body1_parameters_title.setFixedSize(331, 26)
        self.body1_parameters_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.body1_temperature_label = QLabel("Temperature")
        self.body1_temperature_display = QLabel("200")
        self.body1_temperature_unit = QLabel("°C")
        self.body1_mass_label = QLabel("Mass")
        self.body1_mass_unit = QLabel("kg")
        self.body1_heat_capacity_label = QLabel("Specific Heat Capacity")
        self.body1_heat_capacity_unit = QLabel("J/(kg·°C)")

        self.body1_temperature_label.setFixedSize(155, 30)
        self.body1_temperature_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.body1_temperature_display.setFixedSize(85, 30)
        self.body1_temperature_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body1_temperature_display.setStyleSheet(
            "background-color: white; border: 1px solid gray;"
        )
        self.body1_temperature_unit.setFixedSize(75, 30)
        self.body1_mass_label.setFixedSize(155, 30)
        self.body1_mass_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.body1_mass_unit.setFixedSize(75, 30)
        self.body1_heat_capacity_label.setFixedSize(155, 30)
        self.body1_heat_capacity_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.body1_heat_capacity_unit.setFixedSize(75, 30)

        # יצירת פקדי הקלט של הגוף הראשון
        self.body1_mass_input = QDoubleSpinBox()
        self.body1_mass_input.setFixedSize(85, 30)
        self.body1_mass_input.setMinimum(0.01)
        self.body1_mass_input.setValue(10.0)
        self.body1_mass_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body1_mass_input.setButtonSymbols(
            QDoubleSpinBox.ButtonSymbols.NoButtons
        )

        self.body1_heat_capacity_input = QDoubleSpinBox()
        self.body1_heat_capacity_input.setFixedSize(85, 30)
        self.body1_heat_capacity_input.setMinimum(0.01)
        self.body1_heat_capacity_input.setValue(0.40)
        self.body1_heat_capacity_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body1_heat_capacity_input.setButtonSymbols(
            QDoubleSpinBox.ButtonSymbols.NoButtons
        )

        # סידור שורות הנתונים של הגוף הראשון
        body1_temperature_layout = QHBoxLayout()
        body1_temperature_layout.setSpacing(8)
        body1_temperature_layout.addWidget(self.body1_temperature_label)
        body1_temperature_layout.addWidget(self.body1_temperature_display)
        body1_temperature_layout.addWidget(self.body1_temperature_unit)

        body1_mass_layout = QHBoxLayout()
        body1_mass_layout.setSpacing(8)
        body1_mass_layout.addWidget(self.body1_mass_label)
        body1_mass_layout.addWidget(self.body1_mass_input)
        body1_mass_layout.addWidget(self.body1_mass_unit)

        body1_heat_capacity_layout = QHBoxLayout()
        body1_heat_capacity_layout.setSpacing(8)
        body1_heat_capacity_layout.addWidget(self.body1_heat_capacity_label)
        body1_heat_capacity_layout.addWidget(self.body1_heat_capacity_input)
        body1_heat_capacity_layout.addWidget(self.body1_heat_capacity_unit)

        body1_layout = QVBoxLayout()
        body1_layout.setSpacing(10)
        body1_layout.addWidget(self.body1_parameters_title)
        body1_layout.addLayout(body1_temperature_layout)
        body1_layout.addLayout(body1_mass_layout)
        body1_layout.addLayout(body1_heat_capacity_layout)
        body1_layout.addStretch()

        # יצירת הכפתורים המרכזיים בחלק התחתון
        self.start_button = QPushButton("Start")
        self.start_button.setFixedSize(145, 38)
        self.start_button.setCheckable(True)
        self.graphs_button = QPushButton("Graphs")
        self.graphs_button.setFixedSize(145, 38)

        center_layout = QVBoxLayout()
        center_layout.setSpacing(14)
        center_layout.addSpacing(36)
        center_layout.addWidget(self.start_button)
        center_layout.addWidget(self.graphs_button)
        center_layout.addStretch()

        # יצירת כותרת ותוויות הנתונים של הגוף השני
        self.body2_parameters_title = QLabel("Body 2 Parameters")
        self.body2_parameters_title.setFixedSize(331, 26)
        self.body2_parameters_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.body2_temperature_label = QLabel("Temperature")
        self.body2_temperature_display = QLabel("0")
        self.body2_temperature_unit = QLabel("°C")
        self.body2_mass_label = QLabel("Mass")
        self.body2_mass_unit = QLabel("kg")
        self.body2_heat_capacity_label = QLabel("Specific Heat Capacity")
        self.body2_heat_capacity_unit = QLabel("J/(kg·°C)")

        self.body2_temperature_label.setFixedSize(155, 30)
        self.body2_temperature_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.body2_temperature_display.setFixedSize(85, 30)
        self.body2_temperature_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body2_temperature_display.setStyleSheet(
            "background-color: white; border: 1px solid gray;"
        )
        self.body2_temperature_unit.setFixedSize(75, 30)
        self.body2_mass_label.setFixedSize(155, 30)
        self.body2_mass_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.body2_mass_unit.setFixedSize(75, 30)
        self.body2_heat_capacity_label.setFixedSize(155, 30)
        self.body2_heat_capacity_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.body2_heat_capacity_unit.setFixedSize(75, 30)

        # יצירת פקדי הקלט של הגוף השני
        self.body2_mass_input = QDoubleSpinBox()
        self.body2_mass_input.setFixedSize(85, 30)
        self.body2_mass_input.setMinimum(0.01)
        self.body2_mass_input.setValue(10.0)
        self.body2_mass_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body2_mass_input.setButtonSymbols(
            QDoubleSpinBox.ButtonSymbols.NoButtons
        )

        self.body2_heat_capacity_input = QDoubleSpinBox()
        self.body2_heat_capacity_input.setFixedSize(85, 30)
        self.body2_heat_capacity_input.setMinimum(0.01)
        self.body2_heat_capacity_input.setValue(0.40)
        self.body2_heat_capacity_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.body2_heat_capacity_input.setButtonSymbols(
            QDoubleSpinBox.ButtonSymbols.NoButtons
        )

        # סידור שורות הנתונים של הגוף השני
        body2_temperature_layout = QHBoxLayout()
        body2_temperature_layout.setSpacing(8)
        body2_temperature_layout.addWidget(self.body2_temperature_label)
        body2_temperature_layout.addWidget(self.body2_temperature_display)
        body2_temperature_layout.addWidget(self.body2_temperature_unit)

        body2_mass_layout = QHBoxLayout()
        body2_mass_layout.setSpacing(8)
        body2_mass_layout.addWidget(self.body2_mass_label)
        body2_mass_layout.addWidget(self.body2_mass_input)
        body2_mass_layout.addWidget(self.body2_mass_unit)

        body2_heat_capacity_layout = QHBoxLayout()
        body2_heat_capacity_layout.setSpacing(8)
        body2_heat_capacity_layout.addWidget(self.body2_heat_capacity_label)
        body2_heat_capacity_layout.addWidget(self.body2_heat_capacity_input)
        body2_heat_capacity_layout.addWidget(self.body2_heat_capacity_unit)

        body2_layout = QVBoxLayout()
        body2_layout.setSpacing(10)
        body2_layout.addWidget(self.body2_parameters_title)
        body2_layout.addLayout(body2_temperature_layout)
        body2_layout.addLayout(body2_mass_layout)
        body2_layout.addLayout(body2_heat_capacity_layout)
        body2_layout.addStretch()

        # סידור שלושת החלקים התחתונים בחלון
        lower_layout = QHBoxLayout()
        lower_layout.setSpacing(0)
        lower_layout.addStretch()
        lower_layout.addLayout(body1_layout)
        lower_layout.addSpacing(40)
        lower_layout.addLayout(center_layout)
        lower_layout.addSpacing(40)
        lower_layout.addLayout(body2_layout)
        lower_layout.addStretch()

        # סידור הפריסה הראשית של החלון
        main_layout = QVBoxLayout()
        main_layout.addLayout(header_layout)
        main_layout.addSpacing(10)
        main_layout.addLayout(upper_layout)
        main_layout.addSpacing(45)
        main_layout.addLayout(lower_layout)
        main_layout.addStretch()
        self.setLayout(main_layout)

    # פתיחת חלון אודות
    def open_about(self):
        self.about_window.show()


# הפעלת החלון הראשי
if __name__ == "__main__":
    app = QApplication()
    window = HeatTransfer()
    window.show()
    app.exec()
