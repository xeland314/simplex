from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout
from PySide6.QtGui import QKeySequence, QShortcut

class InputWidget(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)

        # Editor de texto
        self.editor = QTextEdit()
        self.editor.setUndoRedoEnabled(True)  # habilita undo/redo

        # Botón Solve
        self.solve_button = QPushButton("Solve")

        # Opcional: botones undo/redo
        btn_layout = QHBoxLayout()
        self.undo_btn = QPushButton("Undo")
        self.redo_btn = QPushButton("Redo")
        btn_layout.addWidget(self.undo_btn)
        btn_layout.addWidget(self.redo_btn)
        btn_layout.addStretch()

        layout.addWidget(self.editor)
        layout.addLayout(btn_layout)
        layout.addWidget(self.solve_button)

        # Conectar botones a las acciones
        self.undo_btn.clicked.connect(self.editor.undo)
        self.redo_btn.clicked.connect(self.editor.redo)

        # Atajos de teclado explícitos (ya funcionan por defecto)
        QShortcut(QKeySequence("Ctrl+Z"), self.editor, self.editor.undo)
        QShortcut(QKeySequence("Ctrl+Y"), self.editor, self.editor.redo)
