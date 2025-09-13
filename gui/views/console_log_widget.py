from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PySide6.QtGui import QTextCursor

class ConsoleLogWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.editor = QTextEdit()
        self.editor.setReadOnly(True)
        layout = QVBoxLayout(self)
        layout.addWidget(self.editor)

    def append_text(self, text):
        self.editor.moveCursor(QTextCursor.MoveToEnd)
        self.editor.insertPlainText(text)