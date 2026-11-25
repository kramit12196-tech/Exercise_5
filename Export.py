# יצירת חלון ייצוא הנתונים עם PySide6
import os

from openpyxl import Workbook
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ExportWindow(QWidget):
    # אתחול חלון ייצוא הנתונים
    def __init__(self, main_window=None, graph_window=None):
        super().__init__()
        self.main_window = main_window
        self.graph_window = graph_window
        self.simulation_checkboxes = []
        self.setupUI()

    # בניית ממשק המשתמש
    def setupUI(self):
        self.setWindowTitle("Export Simulation Data")
        self.setMinimumWidth(450)

        # יצירת כותרת ותיבת בחירה לאופן הייצוא
        self.mode_label = QLabel("Export Mode")

        self.export_mode_selector = QComboBox()
        self.export_mode_selector.addItems(
            ["Export Current Simulation", "Export Multiple Simulations"]
        )
        self.export_mode_selector.setCurrentIndex(0)
        self.export_mode_selector.currentIndexChanged.connect(
            self.update_mode_visibility
        )

        # יצירת אזור בחירת סימולציות מרובות
        self.multiple_section = QWidget()
        multiple_layout = QVBoxLayout()
        multiple_layout.setContentsMargins(0, 8, 0, 8)
        multiple_layout.setSpacing(6)

        self.select_simulations_title = QLabel("Select Simulations")

        self.select_all_checkbox = QCheckBox("Select All")
        self.select_all_checkbox.clicked.connect(self.toggle_select_all)

        self.checkboxes_layout = QVBoxLayout()
        self.checkboxes_layout.setSpacing(6)

        multiple_layout.addWidget(self.select_simulations_title)
        multiple_layout.addWidget(self.select_all_checkbox)
        multiple_layout.addLayout(self.checkboxes_layout)
        self.multiple_section.setLayout(multiple_layout)
        self.multiple_section.setVisible(False)

        # יצירת כפתורי הפעולה בתחתית החלון
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.setFixedSize(110, 34)
        self.cancel_button.clicked.connect(self.close)

        self.export_button = QPushButton("Export")
        self.export_button.setFixedSize(110, 34)
        self.export_button.setEnabled(False)
        self.export_button.clicked.connect(self.export_data)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addWidget(self.export_button)

        # סידור הרכיבים בחלון
        main_layout = QVBoxLayout()
        main_layout.setSpacing(12)
        main_layout.addWidget(self.mode_label)
        main_layout.addWidget(self.export_mode_selector)
        main_layout.addWidget(self.multiple_section)
        main_layout.addStretch()
        main_layout.addLayout(buttons_layout)
        self.setLayout(main_layout)

    # רענון אפשרויות הייצוא ורשימת הסימולציות בפתיחת החלון
    def refresh_options(self):
        # ניקוי תיבות סימון קודמות
        for checkbox in self.simulation_checkboxes:
            checkbox.setParent(None)
        self.simulation_checkboxes = []
        self.select_all_checkbox.setChecked(False)

        # בדיקה שקיימת גישה לחלון הראשי ולחלון הגרפים
        if self.main_window is None or self.graph_window is None:
            self.export_mode_selector.setItemText(0, "Export Current Simulation")
            self.export_mode_selector.setCurrentIndex(0)
            self.update_mode_visibility()
            return

        simulations = self.main_window.simulation_history
        current_index = self.graph_window.simulation_selector.currentIndex()

        # עדכון טקסט האפשרות הראשונה לפי הסימולציה הנבחרת בגרף
        if current_index >= 0 and current_index < len(simulations):
            current_number = simulations[current_index]["number"]
            self.export_mode_selector.setItemText(
                0, f"Export Current Simulation (Simulation {current_number})"
            )
        else:
            self.export_mode_selector.setItemText(0, "Export Current Simulation")

        # יצירת תיבת סימון עבור כל סימולציה שהסתיימה
        for simulation in simulations:
            number = simulation["number"]
            checkbox = QCheckBox(f"Simulation {number}")
            checkbox.setChecked(False)
            checkbox.toggled.connect(self.update_export_button_state)
            self.checkboxes_layout.addWidget(checkbox)
            self.simulation_checkboxes.append(checkbox)

        # בחירת ברירת המחדל ועדכון מצב התצוגה והכפתור
        self.export_mode_selector.setCurrentIndex(0)
        self.update_mode_visibility()

    # הצגה או הסתרה של אזור בחירת הסימולציות המרובות
    def update_mode_visibility(self):
        is_multiple = self.export_mode_selector.currentIndex() == 1
        self.multiple_section.setVisible(is_multiple)
        self.adjustSize()
        self.update_export_button_state()

    # סימון או ביטול סימון של כל הסימולציות
    def toggle_select_all(self):
        checked = self.select_all_checkbox.isChecked()
        for checkbox in self.simulation_checkboxes:
            checkbox.setChecked(checked)
        self.update_export_button_state()

    # עדכון זמינות כפתור הייצוא ותיבת בחר הכל
    def update_export_button_state(self):
        # בדיקה אם קיימות סימולציות זמינות
        if self.main_window is None or len(self.main_window.simulation_history) == 0:
            self.export_button.setEnabled(False)
            self.select_all_checkbox.setChecked(False)
            return

        # במצב ייצוא סימולציה נוכחית
        if self.export_mode_selector.currentIndex() == 0:
            current_index = -1
            if self.graph_window is not None:
                current_index = self.graph_window.simulation_selector.currentIndex()
            self.export_button.setEnabled(current_index >= 0)
            return

        # במצב ייצוא מספר סימולציות
        checked_count = 0
        for checkbox in self.simulation_checkboxes:
            if checkbox.isChecked():
                checked_count += 1

        self.export_button.setEnabled(checked_count > 0)
        all_checked = (
            len(self.simulation_checkboxes) > 0
            and checked_count == len(self.simulation_checkboxes)
        )
        self.select_all_checkbox.setChecked(all_checked)

    # הפעלת הייצוא לפי האפשרות שנבחרה
    def export_data(self):
        if self.main_window is None or self.graph_window is None:
            return

        # ניסיון ייצוא והצגת שגיאה במידת הצורך
        try:
            if self.export_mode_selector.currentIndex() == 0:
                exported = self.export_current_csv()
            else:
                exported = self.export_multiple_excel()

            if exported:
                self.close()
        except Exception as error:
            QMessageBox.critical(self, "Export Error", str(error))

    # ייצוא הסימולציה הנוכחית לקובץ CSV
    def export_current_csv(self):
        index = self.graph_window.simulation_selector.currentIndex()
        simulations = self.main_window.simulation_history

        if index < 0 or index >= len(simulations):
            return False

        # שליפת נתוני הסימולציה השמורים
        simulation = simulations[index]
        number = simulation["number"]
        time = simulation["time"]
        temperature1 = simulation["temperature1"]
        temperature2 = simulation["temperature2"]

        # פתיחת חלון שמירה לבחירת תיקייה ושם קובץ
        default_name = f"Simulation_{number}.csv"
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save Simulation Data",
            default_name,
            "CSV Files (*.csv)",
        )

        if file_name == "":
            return False

        # וידוא סיומת .csv לקובץ שנבחר
        if not file_name.lower().endswith(".csv"):
            file_name += ".csv"

        # כתיבת הנתונים לקובץ CSV
        with open(file_name, "w") as f:
            f.write(
                "Time (s),Body 1 Temperature (deg C),Body 2 Temperature (deg C)\n"
            )
            for i in range(len(time)):
                f.write(f"{time[i]},{temperature1[i]},{temperature2[i]}\n")

        # פתיחת הקובץ באופן אוטומטי
        os.startfile(file_name)
        return True

    # ייצוא הסימולציות שנבחרו לקובץ Excel יחיד
    def export_multiple_excel(self):
        simulations = self.main_window.simulation_history

        # איסוף הסימולציות שסומנו לפי סדר עולה
        selected_simulations = []
        for i in range(len(self.simulation_checkboxes)):
            if self.simulation_checkboxes[i].isChecked():
                selected_simulations.append(simulations[i])

        if len(selected_simulations) == 0:
            return False

        # פתיחת חלון שמירה לבחירת תיקייה ושם קובץ
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save Simulation Data",
            "Heat_Transfer_Simulations.xlsx",
            "Excel Files (*.xlsx)",
        )

        if file_name == "":
            return False

        # וידוא סיומת .xlsx לקובץ שנבחר
        if not file_name.lower().endswith(".xlsx"):
            file_name += ".xlsx"

        # יצירת חוברת עבודה והסרת גיליון ברירת המחדל הריק
        wb = Workbook()
        wb.remove(wb.active)

        # יצירת גיליון נפרד לכל סימולציה שנבחרה
        for simulation in selected_simulations:
            number = simulation["number"]
            time = simulation["time"]
            temperature1 = simulation["temperature1"]
            temperature2 = simulation["temperature2"]

            ws = wb.create_sheet(title=f"Simulation {number}")
            ws.append(
                [
                    "Time (s)",
                    "Body 1 Temperature (deg C)",
                    "Body 2 Temperature (deg C)",
                ]
            )

            # כתיבת כל צעדי הזמן כערכים מספריים
            for j in range(len(time)):
                ws.append([time[j], temperature1[j], temperature2[j]])

            # התאמת רוחב העמודות לקריאה נוחה
            ws.column_dimensions["A"].width = 14
            ws.column_dimensions["B"].width = 28
            ws.column_dimensions["C"].width = 28

        # שמירת חוברת העבודה ופתיחתה באקסל
        wb.save(file_name)
        os.startfile(file_name)
        return True


# הפעלת חלון הייצוא לבדיקה ישירה
if __name__ == "__main__":
    app = QApplication()
    window = ExportWindow()
    window.show()
    app.exec()
