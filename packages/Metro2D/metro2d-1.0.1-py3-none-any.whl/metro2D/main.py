import sys
import os
import multiprocessing
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from multiprocessing import Process

# Import des modules à lancer
from PL.main import main as pl_main
from Raman2D.main import main as raman_main
from semapp.main import main as semapp_main
from wdxrf.main import main as wdxrf_main

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IMAGE_MAP = {
    "PL": os.path.join(BASE_DIR, "images", "pl.png"),
    "Raman2D": os.path.join(BASE_DIR, "images", "raman.png"),
    "SemApp": os.path.join(BASE_DIR, "images", "sem.png"),
    "WDXRF": os.path.join(BASE_DIR, "images", "wdxrf.png"),
}


class HoverButton(QPushButton):
    def __init__(self, label, key, image_label, *args, **kwargs):
        super().__init__(label, *args, **kwargs)
        self.key = key
        self.image_label = image_label
        self.setCursor(Qt.PointingHandCursor)
        self.setFixedHeight(40)
        self.setStyleSheet("""
            QPushButton {
                background-color: #fff;
                border: 1px solid #ccc;
                border-radius: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #e6f0ff;
                border: 1px solid #6699cc;
            }
        """)

    def enterEvent(self, event):
        image_path = IMAGE_MAP.get(self.key)
        if image_path:
            pixmap = QPixmap(image_path)
            if not pixmap.isNull():
                self.image_label.setPixmap(pixmap.scaled(600, 400, Qt.KeepAspectRatio))
            else:
                self.image_label.setText(f"Image introuvable\n{os.path.basename(image_path)}")
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.image_label.clear()
        super().leaveEvent(event)


class LauncherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lanceur d'applications avec aperçu")
        self.setGeometry(300, 100, 1000, 400)
        self.setStyleSheet("background-color: #f2f4f7;")

        layout = QHBoxLayout()
        left_panel = QVBoxLayout()
        left_panel.setContentsMargins(30, 30, 30, 30)
        left_panel.setSpacing(20)

        # Right preview frame
        self.preview_frame = QFrame()
        self.preview_frame.setFixedSize(600, 400)
        self.preview_frame.setStyleSheet("background-color: white; border: 1px solid #ccc;")
        
        self.image_label = QLabel(self.preview_frame)
        self.image_label.setGeometry(0, 0, 600, 400)
        self.image_label.setAlignment(Qt.AlignCenter)

        # Boutons + actions
        self.buttons = [
            ("PL2D", "PL", lambda: Process(target=pl_main).start()),
            ("Raman2D", "Raman2D", lambda: Process(target=raman_main).start()),
            ("SemApp", "SemApp", lambda: Process(target=semapp_main).start()),
            ("XRF2D", "WDXRF", lambda: Process(target=wdxrf_main).start()),
        ]

        for label, key, action in self.buttons:
            btn = HoverButton(label, key, self.image_label)
            btn.clicked.connect(action)
            left_panel.addWidget(btn)

        layout.addLayout(left_panel)
        layout.addWidget(self.preview_frame)
        self.setLayout(layout)


def main():
    multiprocessing.freeze_support()
    app = QApplication(sys.argv)
    window = LauncherApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
