import unittest
import os
import sys
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dorplan.tests.data.graph_coloring import GraphColoring
from dorplan.app import DorPlan
from dorplan.tests.dummy_ui import DummyUi


class AppTest(unittest.TestCase):
    @patch("dorplan.app.QtWidgets.QApplication")
    @patch("dorplan.app.QtWidgets.QMainWindow")
    def test_open_app(self, mock_mainwindow, mock_qapp):
        # Patch QApplication and QMainWindow to prevent GUI from launching
        mock_qapp.return_value = MagicMock()
        mock_mainwindow.return_value = MagicMock()
        # Patch exec to prevent event loop
        with patch("dorplan.app.QtWidgets.QApplication.exec", return_value=None):
            app = DorPlan(GraphColoring, {}, ui=DummyUi)
            self.assertIsInstance(app, DorPlan)

    @patch("dorplan.app.QtWidgets.QApplication")
    @patch("dorplan.app.QtWidgets.QMainWindow")
    def test_update_options(self, mock_mainwindow, mock_qapp):
        mock_qapp.return_value = MagicMock()
        mock_mainwindow.return_value = MagicMock()
        dummy_ui = DummyUi()
        dummy_ui.max_time.text.return_value = "120"
        dummy_ui.log_level.currentIndex.return_value = 1
        dummy_ui.solver.currentText.return_value = "solver1"
        with patch("dorplan.app.QtWidgets.QApplication.exec", return_value=None):
            app = DorPlan(GraphColoring, {}, ui=lambda: dummy_ui)
            app.ui = dummy_ui
            app.options = {}
            result = app.update_options()
            self.assertEqual(app.options["timeLimit"], 120)
            self.assertTrue(app.options["debug"])
            self.assertEqual(app.options["solver"], "solver1")
            self.assertEqual(result, 1)

    @patch("dorplan.app.QtWidgets.QApplication")
    @patch("dorplan.app.QtWidgets.QMainWindow")
    def test_update_ui_no_instance(self, mock_mainwindow, mock_qapp):
        mock_qapp.return_value = MagicMock()
        mock_mainwindow.return_value = MagicMock()
        dummy_ui = DummyUi()
        with patch("dorplan.app.QtWidgets.QApplication.exec", return_value=None):
            app = DorPlan(GraphColoring, {}, ui=lambda: dummy_ui)
            # app.ui = dummy_ui
            app.instance = None
            app.solution = None
            result = app.update_ui()
            dummy_ui.instCheck.setText.assert_called_with("No instance loaded")
            dummy_ui.instCheck.setStyleSheet.assert_called()
            dummy_ui.solCheck.setText.assert_called_with("No solution loaded")
            dummy_ui.solCheck.setStyleSheet.assert_called()
            dummy_ui.reuse_sol.setEnabled.assert_called_with(False)
            dummy_ui.reuse_sol.setChecked.assert_called_with(False)
            self.assertEqual(result, 1)

    @patch("dorplan.app.QtWidgets.QApplication")
    @patch("dorplan.app.QtWidgets.QMainWindow")
    def test_load_test_loads_instance_and_solution(self, mock_mainwindow, mock_qapp):
        mock_qapp.return_value = MagicMock()
        mock_mainwindow.return_value = MagicMock()
        dummy_ui = DummyUi()
        with patch("dorplan.app.QtWidgets.QApplication.exec", return_value=None):
            app = DorPlan(GraphColoring, {}, ui=lambda: dummy_ui)
            app.instance = None
            app.solution = None
            app.load_test()
            self.assertIsNotNone(app.instance)
            # Some test cases may not have a solution, so just check attribute exists
            self.assertTrue(hasattr(app, "solution"))

    @patch("dorplan.app.QtWidgets.QApplication")
    @patch("dorplan.app.QtWidgets.QMainWindow")
    def test_generate_solution_runs_and_updates_ui(self, mock_mainwindow, mock_qapp):
        mock_qapp.return_value = MagicMock()
        mock_mainwindow.return_value = MagicMock()
        dummy_ui = DummyUi()
        dummy_ui.reuse_sol.isChecked.return_value = False
        dummy_ui.solution_log = MagicMock()
        dummy_ui.generateSolution = MagicMock()
        dummy_ui.stopExecution = MagicMock()
        dummy_ui.solver.currentText.return_value = "default"
        dummy_ui.max_time.text.return_value = "60"
        dummy_ui.log_level.currentIndex.return_value = 0
        dummy_ui.solver.addItems = MagicMock()
        dummy_ui.tabWidget = MagicMock()
        with patch("dorplan.app.QtWidgets.QApplication.exec", return_value=None):
            app = DorPlan(GraphColoring, {}, ui=lambda: dummy_ui)
            app.options = {"solver": "default", "timeLimit": 60, "debug": False}
            app.load_test()
            # Patch OptimWorker to avoid threading and side effects
            with (
                patch("dorplan.app.OptimWorker") as MockWorker,
                patch("dorplan.app.LogTailer"),
            ):
                mock_worker_instance = MagicMock()
                MockWorker.return_value = mock_worker_instance
                # Patch signals to avoid errors
                mock_worker_instance.started.connect = MagicMock()
                mock_worker_instance.finished.connect = MagicMock()
                mock_worker_instance.error.connect = MagicMock()
                mock_worker_instance.setObjectName = MagicMock()
                mock_worker_instance.start = MagicMock()
                dummy_ui.stopExecution.clicked.connect = MagicMock()
                dummy_ui.generateSolution.setEnabled = MagicMock()
                dummy_ui.stopExecution.setEnabled = MagicMock()
                result = app.generate_solution()
                self.assertEqual(result, 1)
                mock_worker_instance.start.assert_called_once()
                dummy_ui.generateSolution.setEnabled.assert_called_with(False)
                dummy_ui.stopExecution.setEnabled.assert_called_with(True)

    # Add more tests for other methods as needed, mocking file dialogs, etc.
    def test_solve(self):
        app = GraphColoring()
        data = app.test_cases[0]
        for solver_name in ["pulp", "ortools"]:
            experiment = app.solvers[solver_name](
                app.instance.from_dict(data["instance"])
            )
            experiment.solve({})
            experiment.check_solution()
            experiment.get_objective()


if __name__ == "__main__":
    unittest.main()
