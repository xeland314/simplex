from PySide6.QtCore import QThread, Signal
from dsl import DSL

class SolverThread(QThread):
    finished = Signal(object)

    def __init__(self, problem_str):
        super().__init__()
        self.problem_str = problem_str

    def run(self):
        try:
            dsl = DSL(self.problem_str)
            simplex = dsl.to_simplex()
            simplex.solve_problem()
            simplex.show_results()
            self.finished.emit(simplex)
        except Exception as e:
            self.finished.emit(e)
