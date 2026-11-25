# רכיב מבער מונפש להמחשה חזותית של פעולת גוף החימום
import math

from PySide6.QtCore import QRectF, Qt, QTimer
from PySide6.QtGui import QBrush, QColor, QLinearGradient, QPainter, QPainterPath, QPen
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class BurnerCanvas(QWidget):
    # אתחול אזור הציור הווקטורי של המבער והלהבות
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(155, 68)
        self.heating_power = 0.0
        self.max_power = 1000.0
        self.is_active = False
        self.animation_time = 0.0

        # מיקומים אופקיים, פאזות ותדרים שונים לכל להבה ליצירת ריצוד טבעי
        self.flame_centers = [38.0, 57.5, 77.5, 97.5, 117.0]
        self.flame_phases = [0.0, 1.3, 2.7, 4.1, 5.4]
        self.flame_frequencies = [1.0, 1.24, 0.91, 1.33, 1.12]
        self.flame_height_factors = [0.92, 1.0, 1.04, 1.0, 0.92]

    # עדכון מצב הציור ובקשת רענון מסך
    def set_state(self, power, is_active, animation_time):
        self.heating_power = power
        self.is_active = is_active
        self.animation_time = animation_time
        self.update()

    # ציור המבער המתכתי והלהבות המונפשות באמצעות QPainter
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # ציור הלהבות רק כאשר החימום פעיל וההספק חיובי
        if self.is_active and self.heating_power > 0.0:
            self.draw_flames(painter)

        # ציור גוף המבער המתכתי והבסיס
        self.draw_burner(painter)
        painter.end()

    # ציור שלוש שכבות המבער המתכתי במרכז הרכיב
    def draw_burner(self, painter):
        # חלק עליון כהה של פיית המבער
        top_rect = QRectF(28.0, 44.0, 99.0, 6.0)
        top_grad = QLinearGradient(top_rect.left(), 0, top_rect.right(), 0)
        top_grad.setColorAt(0.0, QColor("#1E293B"))
        top_grad.setColorAt(0.5, QColor("#334155"))
        top_grad.setColorAt(1.0, QColor("#1E293B"))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(top_grad))
        painter.drawRoundedRect(top_rect, 3.0, 3.0)

        # גוף המבער האמצעי בגוון אפור מתכתי
        body_rect = QRectF(20.0, 49.0, 115.0, 10.0)
        body_grad = QLinearGradient(body_rect.left(), 0, body_rect.right(), 0)
        body_grad.setColorAt(0.0, QColor("#475569"))
        body_grad.setColorAt(0.5, QColor("#94A3B8"))
        body_grad.setColorAt(1.0, QColor("#475569"))
        painter.setPen(QPen(QColor("#334155"), 0.8))
        painter.setBrush(QBrush(body_grad))
        painter.drawRoundedRect(body_rect, 4.0, 4.0)

        # בסיס תחתון קומפקטי של המבער
        base_rect = QRectF(42.0, 58.5, 71.0, 7.5)
        base_grad = QLinearGradient(base_rect.left(), 0, base_rect.right(), 0)
        base_grad.setColorAt(0.0, QColor("#334155"))
        base_grad.setColorAt(0.5, QColor("#64748B"))
        base_grad.setColorAt(1.0, QColor("#334155"))
        painter.setPen(QPen(QColor("#1E293B"), 0.7))
        painter.setBrush(QBrush(base_grad))
        painter.drawRoundedRect(base_rect, 3.0, 3.0)

    # ציור הלהבות המונפשות לפי מיפוי לא-ליניארי רגיש במיוחד להספקים נמוכים
    def draw_flames(self, painter):
        normalized_power = self.heating_power / self.max_power
        if normalized_power < 0.0:
            normalized_power = 0.0
        elif normalized_power > 1.0:
            normalized_power = 1.0

        # מיפוי לא-ליניארי חזק להבלטת שינויים גם בהספקים נמוכים
        visual_power = normalized_power ** 0.35

        # טווח רחב ובולט בגובה, ברוחב, במשרעת הריצוד ובעוצמת ההארה
        min_height = 5.0
        max_height = 38.0
        base_height = min_height + (max_height - min_height) * visual_power
        base_width = 8.0 + 16.0 * visual_power
        flicker_amp = 0.06 + 0.14 * visual_power
        sway_amp = 0.6 + 2.4 * visual_power
        speed_factor = 6.5 + 5.0 * visual_power
        base_y = 45.5

        # הילה חמה עדינה מעל פיית המבער שמתחזקת עם ההספק
        glow_alpha = int(18 + 62 * visual_power)
        glow_height = 6.0 + 18.0 * visual_power
        glow_rect = QRectF(
            30.0, base_y - glow_height * 0.75, 95.0, glow_height
        )
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(QColor(249, 115, 22, glow_alpha)))
        painter.drawEllipse(glow_rect)

        # קביעת עוצמת שתי הלהבות החיצוניות כך שבהספק נמוך מוצגים פחות שיאים
        if self.heating_power < 15.0:
            outer_scale = 0.0
        elif self.heating_power < 45.0:
            outer_scale = 0.45 + 0.55 * ((self.heating_power - 15.0) / 30.0)
        else:
            outer_scale = 1.0

        # התאמת צבע ועוצמת הליבה לפי visual_power
        outer_color = QColor("#EA580C") if visual_power > 0.65 else QColor("#F97316")
        inner_color = QColor("#FDE047") if visual_power > 0.55 else QColor("#FACC15")
        core_color = QColor("#FFFBEB") if visual_power > 0.50 else QColor("#FEF9C3")
        core_ratio = 0.28 + 0.16 * visual_power

        for i in range(len(self.flame_centers)):
            is_outer = i == 0 or i == 4
            peak_scale = outer_scale if is_outer else 1.0
            if peak_scale <= 0.0:
                continue

            cx = self.flame_centers[i]
            t = self.animation_time * speed_factor * self.flame_frequencies[i]
            phase = self.flame_phases[i]

            # ריצוד עצמאי בגובה ובהטיית הקצה שמתחזק עם ההספק
            wave = math.sin(t + phase) + 0.35 * math.sin(2.1 * t + 1.7 * phase)
            flicker = 1.0 + flicker_amp * wave
            height = (
                base_height
                * self.flame_height_factors[i]
                * peak_scale
                * flicker
            )
            if height < 4.5:
                height = 4.5
            elif height > 42.5:
                height = 42.5

            sway = sway_amp * math.sin(1.35 * t + phase)
            width = (
                base_width
                * peak_scale
                * (0.93 + 0.07 * math.cos(t + phase))
            )

            # שכבה חיצונית כתומה
            self.draw_teardrop(
                painter, cx, base_y, width, height, sway, outer_color
            )
            # שכבה פנימית צהובה
            self.draw_teardrop(
                painter,
                cx,
                base_y,
                width * 0.68,
                height * 0.72,
                sway * 0.65,
                inner_color,
            )
            # ליבה בהירה וחמה בבסיס הלהבה
            self.draw_teardrop(
                painter,
                cx,
                base_y,
                width * (core_ratio + 0.06),
                height * core_ratio,
                sway * 0.3,
                core_color,
            )

    # יצירת נתיב וקטורי חלק בצורת טיפת להבה
    def draw_teardrop(self, painter, cx, base_y, width, height, sway, color):
        half_w = width / 2.0
        tip_x = cx + sway
        tip_y = base_y - height

        path = QPainterPath()
        path.moveTo(cx - half_w * 0.65, base_y)
        path.cubicTo(
            cx - half_w * 1.05,
            base_y - height * 0.42,
            tip_x - half_w * 0.35,
            base_y - height * 0.72,
            tip_x,
            tip_y,
        )
        path.cubicTo(
            tip_x + half_w * 0.35,
            base_y - height * 0.72,
            cx + half_w * 1.05,
            base_y - height * 0.42,
            cx + half_w * 0.65,
            base_y,
        )
        path.closeSubpath()

        painter.setBrush(QBrush(color))
        painter.drawPath(path)


class HeaterWidget(QWidget):
    # אתחול רכיב גוף החימום המונפש, תווית המצב וטיימר האנימציה העצמאי
    def __init__(self, max_power=1000.0):
        super().__init__()
        self.heating_power = 0.0
        self.max_power = max_power
        self.is_running = False
        self.animation_time = 0.0

        # טיימר אנימציה עצמאי (25 מילישניות) שאינו תלוי במהירות הסימולציה
        self.animation_interval = 25
        self.animation_timer = QTimer(self)
        self.animation_timer.setInterval(self.animation_interval)
        self.animation_timer.timeout.connect(self.update_animation_frame)

        self.setupUI()
        self.update_status_display()

    # בניית מבנה הרכיב: מבער וקטורי למעלה ותווית מצב קומפקטית מתחתיו
    def setupUI(self):
        self.setFixedSize(155, 88)

        self.burner_canvas = BurnerCanvas(self)
        self.burner_canvas.max_power = self.max_power

        self.status_label = QLabel("Heater OFF")
        self.status_label.setObjectName("heaterStatusLabel")
        self.status_label.setFixedSize(155, 18)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        layout.addWidget(self.burner_canvas)
        layout.addWidget(self.status_label)
        self.setLayout(layout)

    # עדכון הספק החימום המוגדר והתאמת האנימציה והתווית
    def set_heating_power(self, power):
        self.heating_power = max(0.0, float(power))

        if self.is_running and self.heating_power > 0.0:
            if not self.animation_timer.isActive():
                self.animation_timer.start(self.animation_interval)
        else:
            self.animation_timer.stop()

        self.update_status_display()

    # הפעלת אנימציית הלהבות רק אם קיים הספק חימום חיובי
    def start_animation(self):
        self.is_running = True
        if self.heating_power > 0.0:
            if not self.animation_timer.isActive():
                self.animation_timer.start(self.animation_interval)
        else:
            self.animation_timer.stop()

        self.update_status_display()

    # עצירת אנימציית הלהבות ושמירת ההספק המוגדר
    def stop_animation(self):
        self.is_running = False
        self.animation_timer.stop()
        self.update_status_display()

    # איפוס מלא של רכיב החימום למצב כבוי
    def reset_animation(self):
        self.is_running = False
        self.heating_power = 0.0
        self.animation_time = 0.0
        self.animation_timer.stop()
        self.update_status_display()

    # קידום פריים אחד של אנימציית הלהבות
    def update_animation_frame(self):
        if not self.is_running or self.heating_power <= 0.0:
            self.animation_timer.stop()
            self.burner_canvas.set_state(0.0, False, self.animation_time)
            return

        self.animation_time += self.animation_interval / 1000.0
        self.burner_canvas.set_state(
            self.heating_power, True, self.animation_time
        )

    # עדכון טקסט ועיצוב תווית מצב גוף החימום ומצב הציור
    def update_status_display(self):
        is_heating = self.is_running and self.heating_power > 0.0
        self.burner_canvas.set_state(
            self.heating_power, is_heating, self.animation_time
        )

        if self.heating_power <= 0.0:
            self.status_label.setText("Heater OFF")
            self.status_label.setStyleSheet(
                "color: #64748B; background-color: transparent; font-size: 12px; font-weight: 600;"
            )
        elif self.is_running:
            self.status_label.setText(f"Heating {self.heating_power:.1f} W")
            self.status_label.setStyleSheet(
                "color: #B45309; background-color: transparent; font-size: 12px; font-weight: bold;"
            )
        else:
            self.status_label.setText(f"Heater Set: {self.heating_power:.1f} W")
            self.status_label.setStyleSheet(
                "color: #92400E; background-color: transparent; font-size: 12px; font-weight: 600;"
            )
