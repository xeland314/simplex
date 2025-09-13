from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout
)
from PySide6.QtGui import QPixmap, QDesktopServices
from PySide6.QtCore import Qt, QUrl


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("About Simplex Solver")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout(self)

        # 🔹 Logo
        logo = QLabel()
        pixmap = QPixmap("gui/assets/pixel-cat.png").scaled(64, 64, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo.setPixmap(pixmap)
        logo.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo)

        # 🔹 Text
        info_label = QLabel(
            "<h3>Simplex Solver</h3>"
            "<p>A simple application to solve linear programming problems using the simplex method.</p>"
            "<p><b>Author:</b> Christopher Villamarín (xeland314)</p>"
            "<p><b>License:</b> MIT License</p>"
        )
        info_label.setWordWrap(True)
        layout.addWidget(info_label)

        # 🔹 Buttons
        buttons_layout = QHBoxLayout()

        btn_repo = QPushButton("GitHub")
        btn_repo.clicked.connect(lambda: QDesktopServices.openUrl(
            QUrl("https://github.com/xeland314/simplex")
        ))
        buttons_layout.addWidget(btn_repo)

        btn_license = QPushButton("License")
        btn_license.clicked.connect(lambda: QDesktopServices.openUrl(
            QUrl("https://github.com/xeland314/simplex/blob/main/LICENSE")
        ))
        buttons_layout.addWidget(btn_license)

        btn_donate = QPushButton("☕ Donate")
        btn_donate.clicked.connect(lambda: QDesktopServices.openUrl(
            QUrl("https://www.buymeacoffee.com/xeland314")
        ))
        buttons_layout.addWidget(btn_donate)

        layout.addLayout(buttons_layout)

        # 🔹 Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button, alignment=Qt.AlignCenter)
