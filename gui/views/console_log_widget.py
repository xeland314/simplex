from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit

class ConsoleLogWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.editor = QTextEdit()
        self.editor.setReadOnly(True)
        layout = QVBoxLayout(self)
        layout.addWidget(self.editor)

    def append_text(self, text):
        self.editor.moveCursor(self.editor.textCursor().End)
        self.editor.insertPlainText(text)
