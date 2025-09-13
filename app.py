import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon, QFontDatabase, QFont
from gui.main_window import MainWindow
from gui.views.emitting_stream import EmittingStream

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Set application icon
    app.setWindowIcon(QIcon("gui/assets/pixel-cat.png"))

    # Load custom font
    font_id = QFontDatabase.addApplicationFont("gui/assets/FiraCode-VariableFont_wght.ttf")
    if font_id != -1:
        font_families = QFontDatabase.applicationFontFamilies(font_id)
        if font_families:
            app.setFont(QFont(font_families[0]))

    window = MainWindow()
    
    # Redirect stdout and stderr
    sys.stdout = EmittingStream()
    sys.stderr = EmittingStream()
    sys.stdout.text_written.connect(window.console_log_widget.append_text)
    sys.stderr.text_written.connect(window.console_log_widget.append_text)

    window.show()
    sys.exit(app.exec())