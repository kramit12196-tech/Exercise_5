# רכיב אנימציה להצגת כיוון ועוצמת מעבר החום בתוך המוט המחבר
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QLabel, QWidget


class HeatFlowWidget(QWidget):
    # אתחול רכיב המוט המחבר ומנגנון האנימציה העצמאי
    def __init__(self):
        super().__init__()
        self.rod_width = 200
        self.rod_height = 26
        self.arrow_width = 24
        self.arrow_height = 24
        self.track_length = float(self.rod_width + self.arrow_width)

        # משתני מצב פנימיים של האנימציה
        self.q_rate = 0.0
        self.direction = 0
        self.arrow_count = 0
        self.arrow_speed = 0.0
        self.phase = 0.0
        self.is_running = False

        # יצירת טיימר אנימציה עצמאי (20 מילישניות ~ 50 פריימים לשנייה)
        self.animation_interval = 20
        self.animation_timer = QTimer(self)
        self.animation_timer.setInterval(self.animation_interval)
        self.animation_timer.timeout.connect(self.update_animation_frame)

        self.setupUI()
        self.update_visual_state()

    # בניית רקע המוט המתכתי, החצים הניתנים לשימוש חוזר והקווים הניטרליים
    def setupUI(self):
        self.setFixedSize(self.rod_width, self.rod_height)

        # רקע המוט המתכתי המשמש גם כמסגרת חיתוך (clipping) לחצים
        self.rod_background = QLabel(self)
        self.rod_background.setObjectName("connectorRod")
        self.rod_background.setGeometry(0, 0, self.rod_width, self.rod_height)

        # תצוגת קווים אפורים ניטרליים כאשר האנימציה כבויה או מעבר החום זניח
        self.dash_label = QLabel("–   –   –", self.rod_background)
        self.dash_label.setGeometry(0, 0, self.rod_width, self.rod_height)
        self.dash_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.dash_label.setStyleSheet(
            "color: #64748B; background-color: transparent; font-size: 14px; font-weight: bold;"
        )

        # יצירת מאגר של 4 תוויות חצים קבועות למניעת ריצוד ויצירה חוזרת
        self.arrow_labels = []
        for _ in range(4):
            arrow = QLabel("→", self.rod_background)
            arrow.setFixedSize(self.arrow_width, self.arrow_height)
            arrow.setAlignment(Qt.AlignmentFlag.AlignCenter)
            arrow.setStyleSheet(
                "color: #B45309; background-color: transparent; font-size: 17px; font-weight: bold;"
            )
            arrow.setVisible(False)
            self.arrow_labels.append(arrow)

    # קבלת קצב מעבר החום המסומן ועדכון כיוון, כמות ומהירות החצים
    def set_heat_flow(self, q_rate):
        self.q_rate = q_rate
        magnitude = abs(q_rate)

        # סף חזותי לזרימה זניחה (אינו משפיע על תנאי שיווי המשקל הפיזיקלי)
        if magnitude < 0.5:
            self.direction = 0
            self.arrow_count = 0
            self.arrow_speed = 0.0
        else:
            if q_rate > 0:
                self.direction = 1
            else:
                self.direction = -1

            # חישוב מהירות חזותית רציפה בפיקסלים לשנייה לפי עוצמת מעבר החום
            self.arrow_speed = 8.0 + 252.0 * magnitude / (magnitude + 200.0)

            # קביעת מספר החצים לפי קטגוריית עוצמת מעבר החום
            if magnitude < 25.0:
                self.arrow_count = 2
            elif magnitude < 100.0:
                self.arrow_count = 3
            else:
                self.arrow_count = 4

        self.update_visual_state()

    # החזרת תיאור עוצמת מעבר החום בהתאם לקצב הנוכחי
    def get_strength_text(self):
        magnitude = abs(self.q_rate)
        if magnitude < 0.5:
            return "Negligible Heat Flow"
        if magnitude < 25.0:
            return "Weak Heat Flow"
        if magnitude < 100.0:
            return "Medium Heat Flow"
        return "Strong Heat Flow"

    # הפעלת אנימציית זרימת החום
    def start_animation(self):
        self.is_running = True
        self.update_visual_state()
        if not self.animation_timer.isActive():
            self.animation_timer.start(self.animation_interval)

    # עצירת אנימציית זרימת החום והחזרת תצוגה ניטרלית
    def stop_animation(self):
        self.is_running = False
        self.animation_timer.stop()
        self.update_visual_state()

    # איפוס מלא של מצב האנימציה ומיקום החצים
    def reset_animation(self):
        self.is_running = False
        self.animation_timer.stop()
        self.q_rate = 0.0
        self.direction = 0
        self.arrow_count = 0
        self.arrow_speed = 0.0
        self.phase = 0.0
        self.update_visual_state()

    # עדכון נראות וכיוון החצים או הקווים הניטרליים ללא איפוס הפאזה
    def update_visual_state(self):
        if not self.is_running or self.arrow_count == 0:
            self.dash_label.setVisible(True)
            for arrow in self.arrow_labels:
                arrow.setVisible(False)
            return

        self.dash_label.setVisible(False)
        arrow_symbol = "→" if self.direction > 0 else "←"

        for i in range(len(self.arrow_labels)):
            if i < self.arrow_count:
                self.arrow_labels[i].setText(arrow_symbol)
                self.arrow_labels[i].setVisible(True)
            else:
                self.arrow_labels[i].setVisible(False)

        self.position_arrows()

    # קידום רציף של מיקום החצים בכל פריים של טיימר האנימציה
    def update_animation_frame(self):
        if not self.is_running or self.arrow_count == 0:
            return

        # חישוב תזוזה שברית בפיקסלים לשמירה על תנועה חלקה גם במהירויות נמוכות
        dt_seconds = self.animation_interval / 1000.0
        step = self.arrow_speed * dt_seconds

        if self.direction > 0:
            self.phase = (self.phase + step) % self.track_length
        elif self.direction < 0:
            self.phase = (self.phase - step) % self.track_length

        self.position_arrows()

    # חישוב מיקום אופקי מרווח באופן שווה לכל חץ פעיל בתוך המוט
    def position_arrows(self):
        if self.arrow_count == 0:
            return

        spacing = self.track_length / self.arrow_count
        y_pos = (self.rod_height - self.arrow_height) // 2

        for i in range(self.arrow_count):
            x_float = ((self.phase + i * spacing) % self.track_length) - self.arrow_width
            self.arrow_labels[i].move(int(round(x_float)), y_pos)
