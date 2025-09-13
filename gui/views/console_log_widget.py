from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton
from PySide6.QtGui import QTextCursor
import re

class ConsoleLogWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.editor = QTextEdit()
        self.editor.setReadOnly(True)
        self.clear_button = QPushButton("Clear Console")
        self.clear_button.clicked.connect(self.editor.clear)
        layout.addWidget(self.editor)
        layout.addWidget(self.clear_button)

    def append_text(self, text):
        # Strip ANSI escape codes
        ansi_escape = re.compile(r'\x1b\[[0-9;]*[a-zA-Z]')
        clean_text = ansi_escape.sub('', text)
        self.editor.moveCursor(QTextCursor.MoveOperation.End)
        self.editor.insertPlainText(clean_text)
