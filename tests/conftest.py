import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

import pytest
from PySide6.QtWidgets import QApplication, QMessageBox

from rword.core.document import Document
from rword.ui.editor import Editor
from rword.ui.main_window import MainWindow


@pytest.fixture(scope="session")
def qapp():
    app = QApplication.instance() or QApplication([])
    yield app


@pytest.fixture
def editor(qapp):
    widget = Editor()
    yield widget
    widget.deleteLater()


@pytest.fixture
def main_window(qapp, tmp_path, monkeypatch):
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setattr(
        QMessageBox,
        "question",
        staticmethod(lambda *args, **kwargs: QMessageBox.StandardButton.Discard),
    )
    monkeypatch.setattr(
        QMessageBox,
        "critical",
        staticmethod(lambda *args, **kwargs: QMessageBox.StandardButton.Ok),
    )
    monkeypatch.setattr(
        QMessageBox,
        "information",
        staticmethod(lambda *args, **kwargs: QMessageBox.StandardButton.Ok),
    )
    window = MainWindow()
    yield window
    window.close()


@pytest.fixture
def document():
    return Document()
