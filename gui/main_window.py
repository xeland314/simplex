from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QSplitter, QTableWidgetItem, QMessageBox, QFileDialog, QTabWidget
from PySide6.QtGui import QAction
from .views.input_widget import InputWidget
from .views.results_table import ResultsTable
from .views.plot_widget import PlotWidget
from .views.console_log_widget import ConsoleLogWidget
from .views.about_dialog import AboutDialog
from .solver_thread import SolverThread
import numpy as np

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simplex Solver")
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        splitter = QSplitter()
        layout.addWidget(splitter)
        
        self.input_widget = InputWidget()
        splitter.addWidget(self.input_widget)
        
        self.tabs = QTabWidget()
        self.results_table = ResultsTable()
        self.plot_widget = PlotWidget()
        self.console_log_widget = ConsoleLogWidget()
        self.tabs.addTab(self.results_table, "Results")
        self.tabs.addTab(self.plot_widget, "Plot")
        self.tabs.addTab(self.console_log_widget, "Console Log")
        splitter.addWidget(self.tabs)
        
        self.input_widget.solve_button.clicked.connect(self.solve)
        
        self._create_menus()
        
    def _create_menus(self):
        # File menu
        file_menu = self.menuBar().addMenu("&File")
        open_action = QAction("&Open", self)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        save_action = QAction("&Save", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        quit_action = QAction("&Quit", self)
        quit_action.triggered.connect(self.close)
        file_menu.addAction(quit_action)
        
        # Help menu
        help_menu = self.menuBar().addMenu("&Help")
        about_action = QAction("&About", self)
        about_action.triggered.connect(self.about)
        help_menu.addAction(about_action)
        
    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "LP Files (*.lp);;Text Files (*.txt)")
        if file_name:
            with open(file_name, 'r') as f:
                self.input_widget.editor.setPlainText(f.read())
    
    def save_file(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save File",
            "",
            "LP Files (*.lp)"
        )
        if file_name:
            # Ensure it has a .lp extension
            if not file_name.lower().endswith(".lp"):
                file_name += ".lp"
            try:
                with open(file_name, 'w') as f:
                    f.write(self.input_widget.editor.toPlainText())
                QMessageBox.information(self, "Saved", f"File saved to:\n{file_name}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file:\n{str(e)}")
    
    def about(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec()
        
    def solve(self):
        problem_str = self.input_widget.editor.toPlainText()
        self.solver_thread = SolverThread(problem_str)
        self.solver_thread.finished.connect(self.update_results)
        self.solver_thread.start()
        
    def update_results(self, result):
        if isinstance(result, Exception):
            QMessageBox.critical(self, "Error", str(result))
        else:
            self.results_table.table.setRowCount(len(result.optimal_values))
            self.results_table.table.setColumnCount(2)
            self.results_table.table.setHorizontalHeaderLabels(["Variable", "Value"])
            for i, (var, val) in enumerate(result.optimal_values):
                self.results_table.table.setItem(i, 0, QTableWidgetItem(var))
                self.results_table.table.setItem(i, 1, QTableWidgetItem(str(val)))
            
            self.plot_widget.figure.clear()
            ax = self.plot_widget.figure.add_subplot(111)
            
            if len(result.objective_function.variables) == 2:
                x = np.linspace(0, 20, 400)
                for const in result.constraints:
                    if len(const.variables) == 2:
                        c = const.coefficients
                        b = const.independent_term
                        if c[1] != 0:
                            y = (float(b) - float(c[0]) * x) / float(c[1])
                            ax.plot(x, y, label=const.representation)
                
                # Draw axes
                ax.axhline(0, color="black", linewidth=1)
                ax.axvline(0, color="black", linewidth=1)

                # Mark optimal point if defined
                opt_values = dict(result.optimal_values)
                if "x1" in opt_values and "x2" in opt_values:
                    x_opt = float(opt_values["x1"])
                    y_opt = float(opt_values["x2"])
                    ax.scatter(x_opt, y_opt, color="red", s=80, zorder=5, label="Optimal")
                    ax.text(x_opt, y_opt, f"({x_opt:.2f}, {y_opt:.2f})",
                            fontsize=9, ha="left", va="bottom", color="red")
                
                ax.legend()
                ax.grid(True, linestyle="--", alpha=0.6)
            
            self.plot_widget.canvas.draw()