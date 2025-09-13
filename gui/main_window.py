from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QSplitter, QTableWidgetItem, QMessageBox, QFileDialog, QTabWidget
from PySide6.QtGui import QAction
from .views.input_widget import InputWidget
from .views.results_table import ResultsTable
from .views.plot_widget import PlotWidget
from .views.console_log_widget import ConsoleLogWidget
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
    
    def about(self):
        QMessageBox.about(self, "About Simplex Solver", "A simple application to solve linear programming problems.")
        
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
                            y = (b - c[0] * x) / c[1]
                            ax.plot(x, y, label=const.representation)
                ax.legend()
            
            self.plot_widget.canvas.draw()