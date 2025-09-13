import sys
from PySide6.QtWidgets import QApplication
from gui.main_window import MainWindow
from gui.views.emitting_stream import EmittingStream

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    
    # Redirect stdout and stderr
    sys.stdout = EmittingStream()
    sys.stderr = EmittingStream()
    sys.stdout.text_written.connect(window.console_log_widget.append_text)
    sys.stderr.text_written.connect(window.console_log_widget.append_text)

    window.show()
    sys.exit(app.exec())