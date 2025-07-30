import sys
import os
import multiprocessing
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFrame
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from multiprocessing import Process

from pathlib import Path

# Import des modules à lancer
from PL.main import main as pl_main
from Raman2D.main import main as raman_main
from semapp.main import main as semapp_main
from wdxrf.main import main as wdxrf_main

def load_image(name: str) -> QPixmap:
    # Le dossier `images` est au même niveau que ce fichier
    image_path = Path(__file__).parent / "images" / name
    return QPixmap(str(image_path))

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
        try:
            pixmap = load_image(f"{self.key.lower()}.png")
            if not pixmap.isNull():
                self.image_label.setPixmap(pixmap.scaled(600, 400, Qt.KeepAspectRatio))
            else:
                self.image_label.setText(f"Image vide : {self.key.lower()}.png")
        except FileNotFoundError:
            self.image_label.setText(f"Image introuvable : {self.key.lower()}.png")
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
            ("PL", "pl", lambda: Process(target=pl_main).start()),
            ("Raman", "raman", lambda: Process(target=raman_main).start()),
            ("SemApp", "sem", lambda: Process(target=semapp_main).start()),
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
