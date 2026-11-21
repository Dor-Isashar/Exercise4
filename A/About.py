from pathlib import Path

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

PROJECT_ROOT = Path(__file__).resolve().parent


class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")
        self.setFixedSize(420, 620)
        self.setStyleSheet("background-color: #1e1e1e;")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(12)

        # Profile image
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setFixedSize(150, 180)
        self.image_label.setStyleSheet(
            "border: 1px solid #444444; background-color: #2d2d2d; color: #aaaaaa;"
        )
        pixmap = QPixmap(str(PROJECT_ROOT / "profile.jpg"))
        if not pixmap.isNull():
            self.image_label.setPixmap(pixmap.scaled(150, 180, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        layout.addWidget(self.image_label, alignment=Qt.AlignmentFlag.AlignCenter)

        # Name
        self.info_label = QLabel("Dor Isashar")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #ffffff;")
        layout.addWidget(self.info_label)

        # Bio
        bio_text = (
            "3rd-year Mechanical Engineering student with a unique "
            "multidisciplinary background. Combines strong academic "
            "foundations with hands-on experience in heavy machinery "
            "electrical systems and software development. Proficient "
            "in SolidWorks and Python, with a proven ability to bridge "
            "the gap between hardware and code. Passionate about solving "
            "complex physical problems, reverse engineering, and "
            "developing innovative electromechanical solutions."
        )
        self.bio_label = QLabel(bio_text)
        self.bio_label.setWordWrap(True)
        self.bio_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.bio_label.setStyleSheet("font-size: 13px; color: #cccccc; line-height: 1.4;")
        layout.addWidget(self.bio_label)

        layout.addSpacing(8)

        # LinkedIn link
        linkedin_url = "https://www.linkedin.com/in/dor-isashar-a2a2341b1/"
        self.link_label = QLabel(
            f'<a href="{linkedin_url}" style="color: #4da6ff; text-decoration: none;">LinkedIn Profile</a>'
        )
        self.link_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.link_label.setOpenExternalLinks(True)
        self.link_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(self.link_label)

        # GitHub link
        github_url = "https://github.com/Dor-Isashar/Exercise4"
        self.github_label = QLabel(
            f'<a href="{github_url}" style="color: #a6e3a1; text-decoration: none;">GitHub Repository</a>'
        )
        self.github_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.github_label.setOpenExternalLinks(True)
        self.github_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(self.github_label)
