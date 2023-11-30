from PySide6.QtWidgets import QWidget
from pytestqt.qtbot import QtBot
from qdamakuengine.damaku import Damaku


def test_damaku(qtbot: QtBot):
    widget = QWidget()
    damaku = Damaku("pytest-qt-damaku", "Test-Damaku-By-pytest-qt", widget)
    qtbot.addWidget(widget)
    damaku.play()