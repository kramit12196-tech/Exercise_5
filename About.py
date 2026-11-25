from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QApplication, QHBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

class AboutWindow(QWidget):

    # אתחול חלון אודות
    def __init__(self):
        super().__init__()
        self.initUI()

    # בניית ממשק חלון אודות
    def initUI(self):

        #---------- הגדרות חלון אודות ----------
        self.setWindowTitle("About")
        self.setFixedSize(390, 680)
        self.setStyleSheet("background-color: #202734;")

        self.layout = QVBoxLayout()
        self.layout.setSpacing(6)
        self.layout.setContentsMargins(16, 12, 16, 12)
        #---------------------------------------

        #---------- תמונת המפתח ----------
        self.photo_label = QLabel()
        self.photo_label.setPixmap(QPixmap("profile.png").scaled(140, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.photo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.photo_label.setFixedHeight(150)

        self.layout.addWidget(self.photo_label)
        #----------------------------------

        #---------- פרטים אישיים ----------
        self.name_label = QLabel("Amit Kremer")
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_label.setStyleSheet("color: white; font-size: 23px; font-weight: bold;")
        self.name_label.setFixedHeight(35)

        self.role_label = QLabel("Mechanical Engineering Student | App Developer")
        self.role_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.role_label.setStyleSheet("color: #AFC8E6; font-size: 12px;")
        self.role_label.setFixedHeight(25)

        self.layout.addWidget(self.name_label)
        self.layout.addWidget(self.role_label)
        #-----------------------------------

        #---------- כרטיס פרטי הקשר ----------
        self.contact_card = QWidget()
        self.contact_card.setFixedHeight(105)
        self.contact_card.setStyleSheet("background-color: #2B394D; border-radius: 10px;")

        self.contact_layout = QVBoxLayout()
        self.contact_layout.setSpacing(6)
        self.contact_layout.setContentsMargins(12, 8, 12, 8)

        self.contact_title = QLabel("Contact Information")
        self.contact_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.contact_title.setStyleSheet("color: white; font-size: 13px; font-weight: bold; background: transparent;")
        self.contact_layout.addWidget(self.contact_title)

        self.email_icon = QLabel("✉")
        self.email_icon.setFixedSize(22, 22)
        self.email_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.email_icon.setStyleSheet("color: white; background-color: #EA4335; font-size: 16px; border-radius: 3px;")

        self.email_label = QLabel('<a href="mailto:kramit12196@gmail.com" style="color: #85C6FF; text-decoration:none;">kramit12196@gmail.com</a>')
        self.email_label.setOpenExternalLinks(True)
        self.email_label.setStyleSheet("background: transparent; font-size: 13px")

        self.email_row = QHBoxLayout()
        self.email_row.addStretch()
        self.email_row.addWidget(self.email_icon)
        self.email_row.addWidget(self.email_label)
        self.email_row.addStretch()
        self.contact_layout.addLayout(self.email_row)

        self.linkedin_icon = QLabel("in")
        self.linkedin_icon.setFixedSize(22, 22)
        self.linkedin_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.linkedin_icon.setStyleSheet("color: white; background-color: #0A66C2; font-weight: bold; border-radius: 3px;")

        self.linkedin_label = QLabel('<a href="https://www.linkedin.com/in/amit-kremer-bb1756221/" style="color:#85C6FF;">LinkedIn Profile</a>')
        self.linkedin_label.setOpenExternalLinks(True)
        self.linkedin_label.setStyleSheet("background: transparent;")

        self.linkedin_row = QHBoxLayout()
        self.linkedin_row.addStretch()
        self.linkedin_row.addWidget(self.linkedin_icon)
        self.linkedin_row.addWidget(self.linkedin_label)
        self.linkedin_row.addStretch()
        self.contact_layout.addLayout(self.linkedin_row)

        self.contact_card.setLayout(self.contact_layout)
        self.layout.addWidget(self.contact_card)
        #-------------------------------------

        #---------- כרטיס פרויקטים ----------
        self.projects_card = QWidget()
        self.projects_card.setFixedHeight(265)
        self.projects_card.setStyleSheet("background-color: #2B394D; border-radius: 10px;")

        self.projects_layout = QVBoxLayout()
        self.projects_layout.setSpacing(4)
        self.projects_layout.setContentsMargins(12, 8, 12, 8)

        self.projects_title = QLabel("Developer Projects")
        self.projects_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.projects_title.setStyleSheet("color: white; font-size: 13px; font-weight: bold; background: transparent;")
        self.projects_layout.addWidget(self.projects_title)

        self.ex3_label = QLabel("Exercise 3: Bank Account Manager")
        self.ex3_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ex3_label.setStyleSheet("color: white; font-size: 12px; background: transparent;")
        self.projects_layout.addWidget(self.ex3_label)

        self.ex4_label = QLabel("Exercise 4.1: Grades Correction")
        self.ex4_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ex4_label.setStyleSheet("color: white; font-size: 12px; background: transparent;")
        self.projects_layout.addWidget(self.ex4_label)

        self.github41_icon = QLabel("GH")
        self.github41_icon.setFixedSize(22, 22)
        self.github41_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.github41_icon.setStyleSheet("color: white; background-color: #24292F; font-size: 10px; font-weight: bold; border-radius: 3px;")

        self.github41_label = QLabel('<a href="https://github.com/kramit12196-tech/-Exercise_4_1" style="color:#85C6FF;">GitHub - Exercise 4.1</a>')
        self.github41_label.setOpenExternalLinks(True)
        self.github41_label.setStyleSheet("background: transparent;")

        self.github41_row = QHBoxLayout()
        self.github41_row.addStretch()
        self.github41_row.addWidget(self.github41_icon)
        self.github41_row.addWidget(self.github41_label)
        self.github41_row.addStretch()
        self.projects_layout.addLayout(self.github41_row)

        self.ex42_label = QLabel("Exercise 4.2: Ice Cream Profits")
        self.ex42_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ex42_label.setStyleSheet("color: white; font-size: 12px; background: transparent;")
        self.projects_layout.addWidget(self.ex42_label)

        self.github42_icon = QLabel("GH")
        self.github42_icon.setFixedSize(22, 22)
        self.github42_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.github42_icon.setStyleSheet("color: white; background-color: #24292F; font-size: 10px; font-weight: bold; border-radius: 3px;")

        self.github42_label = QLabel('<a href="https://github.com/kramit12196-tech/Exercise_4_2" style="color:#85C6FF;">GitHub - Exercise 4.2</a>')
        self.github42_label.setOpenExternalLinks(True)
        self.github42_label.setStyleSheet("background: transparent;")

        self.github42_row = QHBoxLayout()
        self.github42_row.addStretch()
        self.github42_row.addWidget(self.github42_icon)
        self.github42_row.addWidget(self.github42_label)
        self.github42_row.addStretch()
        self.projects_layout.addLayout(self.github42_row)

        # הוספת פרויקט תרגיל 5
        self.ex5_label = QLabel("Exercise 5: Heat Transfer Simulation")
        self.ex5_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ex5_label.setStyleSheet("color: white; font-size: 12px; background: transparent;")
        self.projects_layout.addWidget(self.ex5_label)

        self.github5_icon = QLabel("GH")
        self.github5_icon.setFixedSize(22, 22)
        self.github5_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.github5_icon.setStyleSheet("color: white; background-color: #24292F; font-size: 10px; font-weight: bold; border-radius: 3px;")

        self.github5_label = QLabel('<a href="https://github.com/kramit12196-tech/Exercise_5" style="color:#85C6FF;">GitHub - Exercise 5</a>')
        self.github5_label.setOpenExternalLinks(True)
        self.github5_label.setStyleSheet("background: transparent;")

        self.github5_row = QHBoxLayout()
        self.github5_row.addStretch()
        self.github5_row.addWidget(self.github5_icon)
        self.github5_row.addWidget(self.github5_label)
        self.github5_row.addStretch()
        self.projects_layout.addLayout(self.github5_row)

        self.projects_card.setLayout(self.projects_layout)
        self.layout.addWidget(self.projects_card)
        #-------------------------------------

        #---------- פרטי פיתוח וסיום ----------
        self.footer_label = QLabel("Developed with Python & PySide6")
        self.footer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.footer_label.setStyleSheet("color: #9BAABC; font-size: 11px")

        self.layout.addWidget(self.footer_label)
        self.layout.addStretch()
        self.setLayout(self.layout)
        #--------------------------------------

if __name__ == "__main__":
    app = QApplication([])
    window = AboutWindow()
    window.show()
    app.exec()