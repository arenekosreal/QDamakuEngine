import json
import socket
from PySide6.QtCore import QThread
from PySide6.QtWidgets import QWidget
import pytest
from pytestqt.qtbot import QtBot
from qdamakuengine.app import App, _DamakuDistributionSmoothly  # type:ignore


def test_distribution(qtbot: QtBot):
    widget = QWidget()
    thread = QThread(widget)
    job = _DamakuDistributionSmoothly()
    thread.started.connect(job.start.emit)
    job.moveToThread(thread)
    thread.start()
    widget.show()
    qtbot.addWidget(widget)
    with qtbot.waitSignal(job.damakuupdated, timeout=10000):
        job.add.emit("Test-Damaku", "Pytest")
    job.stop.emit()
    thread.quit()
    if not thread.isFinished():
        thread.wait()


@pytest.mark.skip(reason="Need more work to know why s.recv hangs.")
def test_app(qtbot: QtBot):
    app = App()
    app.show()
    qtbot.addWidget(app)
    # app.close()
    with socket.socket() as s:
        s.connect(("127.0.0.1", 2333))
        s.sendall(json.dumps({"text": "Test-Damaku"}).encode())
        data = s.recv(1024).decode()
    assert json.loads(data)["result"] == 0
    app.dthread.quit()
