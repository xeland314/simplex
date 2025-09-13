from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QMenu, QPushButton, QHBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut, QGuiApplication


class ResultsTable(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        # Tabla principal
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # Configurar selección
        self.table.setSelectionBehavior(QTableWidget.SelectItems)  # o SelectRows
        self.table.setSelectionMode(QTableWidget.ExtendedSelection)

        # Shortcut Ctrl+C para copiar
        copy_shortcut = QShortcut(QKeySequence("Ctrl+C"), self.table)
        copy_shortcut.activated.connect(self.copy_selection_to_clipboard)

        # Menú contextual para clic derecho
        self.table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.open_context_menu)

        # Botón para copiar toda la tabla
        btn_layout = QHBoxLayout()
        copy_all_btn = QPushButton("Copiar toda la tabla")
        copy_all_btn.clicked.connect(self.copy_entire_table)
        btn_layout.addStretch()
        btn_layout.addWidget(copy_all_btn)
        layout.addLayout(btn_layout)

    # Copiar celdas seleccionadas con nombres de columna
    def copy_selection_to_clipboard(self):
        selection = self.table.selectedRanges()
        if not selection:
            return

        copied_text = ""

        for r in selection:
            # Agregar encabezados de columna
            headers = [self.table.horizontalHeaderItem(col).text() if self.table.horizontalHeaderItem(col) else ""
                       for col in range(r.leftColumn(), r.rightColumn() + 1)]
            copied_text += "\t".join(headers) + "\n"

            # Agregar valores
            for row in range(r.topRow(), r.bottomRow() + 1):
                row_data = []
                for col in range(r.leftColumn(), r.rightColumn() + 1):
                    item = self.table.item(row, col)
                    row_data.append(item.text() if item else "")
                copied_text += "\t".join(row_data) + "\n"

        QGuiApplication.clipboard().setText(copied_text)

    # Copiar toda la tabla con nombres de columna
    def copy_entire_table(self):
        row_count = self.table.rowCount()
        col_count = self.table.columnCount()
        copied_text = ""

        # Encabezados
        headers = [self.table.horizontalHeaderItem(col).text() if self.table.horizontalHeaderItem(col) else ""
                   for col in range(col_count)]
        copied_text += "\t".join(headers) + "\n"

        # Datos
        for row in range(row_count):
            row_data = []
            for col in range(col_count):
                item = self.table.item(row, col)
                row_data.append(item.text() if item else "")
            copied_text += "\t".join(row_data) + "\n"

        QGuiApplication.clipboard().setText(copied_text)

    # Menú contextual clic derecho
    def open_context_menu(self, position):
        menu = QMenu()
        copy_action = menu.addAction("Copiar selección")
        copy_all_action = menu.addAction("Copiar toda la tabla")

        action = menu.exec(self.table.viewport().mapToGlobal(position))
        if action == copy_action:
            self.copy_selection_to_clipboard()
        elif action == copy_all_action:
            self.copy_entire_table()
