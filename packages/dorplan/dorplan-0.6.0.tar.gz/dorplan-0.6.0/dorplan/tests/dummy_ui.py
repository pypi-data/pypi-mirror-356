from unittest.mock import MagicMock


class DummyUi:
    def __init__(self):
        # Mock all UI elements used in DorPlan
        self.actionOpen_from = MagicMock()
        self.actionSave = MagicMock()
        self.actionSave_As = MagicMock()
        self.actionExit = MagicMock()
        self.chooseFile = MagicMock()
        self.loadTest = MagicMock()
        self.checkSolution = MagicMock()
        self.exportSolution = MagicMock()
        self.exportSolution_to = MagicMock()
        self.generateReport = MagicMock()
        self.generateSolution = MagicMock()
        self.openReport = MagicMock()
        self.max_time = MagicMock()
        self.log_level = MagicMock()
        self.solver = MagicMock()
        self.tabWidget = MagicMock()
        self.instCheck = MagicMock()
        self.solCheck = MagicMock()
        self.reuse_sol = MagicMock()
        self.solution_log = MagicMock()
        self.stopExecution = MagicMock()
        self.solution_report = MagicMock()
        self.objectiveLineEdit = MagicMock()
        self.errorsLineEdit = MagicMock()

    def setupUi(self, MainWindow):
        pass
