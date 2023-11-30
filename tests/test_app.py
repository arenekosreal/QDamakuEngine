from PySide6.QtCore import QThread
from PySide6.QtWidgets import QWidget
from pytestqt.qtbot import QtBot
from qdamakuengine.app import App, _DamakuDistributionSmoothly


def test_distribution(qtbot: QtBot):
    widget = QWidget()
    thread = QThread(widget)
    job = _DamakuDistributionSmoothly()
    thread.started.connect(job.start)
    job.moveToThread(thread)
    thread.start()
    widget.show()
    with qtbot.waitSignal(job.damakuupdated, timeout=10000):
        job.add("Test-Damaku", "Pytest")
    job.stop()
    qtbot.addWidget(widget)
    thread.quit()
    while not thread.isFinished():
        thread.wait()
