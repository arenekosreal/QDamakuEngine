import json
import random
from typing import Any
from PySide6.QtCore import QObject, QThread, QTimerEvent, Qt, Signal, Slot
from PySide6.QtWidgets import QFrame, QGraphicsDropShadowEffect, QMenu, QVBoxLayout, QWidget
from PySide6.QtGui import QMouseEvent, QContextMenuEvent
from PySide6.QtNetwork import QHostAddress, QLocalServer, QTcpServer, QTcpSocket
from qdamakuengine.config import get_config
from qdamakuengine.damaku import Damaku
from qdamakuengine.log import info, error, debug


_object_names: dict[str, str] = {
    "main": "main"
}


class _DamakuDistributionSmoothly(QObject):
    damakuupdated = Signal(str, str)
    add = Signal(str, str)
    start = Signal()
    started = Signal()
    stop = Signal()
    stopped = Signal()

    def __init__(self) -> None:
        super().__init__()
        self._damaku_send_wait_secs = get_config().damaku.damaku_send_wait_secs
        self._damakus: list[tuple[str, str]] = []
        self.start.connect(self._start)
        self.stop.connect(self._stop)
        self.add.connect(self._add)
        self._timer_id = 0

    @Slot(str, str)
    def _add(self, damaku: str, sender: str):
        self._damakus.append((damaku, sender))

    @Slot()
    def _start(self):
        self._timer_id = self.startTimer(int(1000*self._damaku_send_wait_secs))
        self.started.emit()

    @Slot()
    def _stop(self):
        self.killTimer(self._timer_id)
        self.stopped.emit()

    def timerEvent(self, event: QTimerEvent) -> None:
        if event.timerId() == self._timer_id and len(self._damakus) > 0:
            self.damakuupdated.emit(
                *self._damakus.pop(0)
            )
        return super().timerEvent(event)


class _FramelessWindowWidget(QWidget):
    """The frameless window widget with optimizations
    """

    def __init__(self):
        super().__init__(f=Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

    def mousePressEvent(self, event: QMouseEvent):
        """Let frameless window can also be dragged.
        """
        if self.isEnabled() and self.isVisible() and event.button() == Qt.MouseButton.LeftButton:
            self.windowHandle().startSystemMove()
        return super().mousePressEvent(event)


class App(_FramelessWindowWidget):
    """The main window
    """

    def __init__(self):
        super().__init__()
        self._config = get_config()
        if not self._config.ui.fullscreen:
            self.resize(self._config.ui.width, self._config.ui.height)
        self.container = QFrame(self)
        self.container.setFrameShape(QFrame.Shape.StyledPanel)
        self.container.setObjectName(_object_names["main"])
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setColor(Qt.GlobalColor.black)
        shadow.setBlurRadius(self._config.ui.shadow_radius)
        shadow.setOffset(0)
        self.container.setGraphicsEffect(shadow)
        layout = QVBoxLayout(self)
        layout.addWidget(self.container)
        layout.setContentsMargins(
            self._config.ui.shadow_radius,
            self._config.ui.shadow_radius,
            self._config.ui.shadow_radius,
            self._config.ui.shadow_radius
        )
        self.setLayout(layout)

        self.dthread = QThread(self)
        self.djob = _DamakuDistributionSmoothly()
        self.dthread.started.connect(self.djob.start.emit)
        self.djob.damakuupdated.connect(self.play_damaku)
        self.djob.moveToThread(self.dthread)

        if self._config.network.address.startswith("local://"):
            self.socket = QLocalServer(self)
        elif self._config.network.address.startswith("tcp://"):
            self.socket = QTcpServer(self)
        else:
            raise RuntimeError(
                "Unable to listen to socket, please check your config.")

    @Slot(str, str)
    def play_damaku(self, text: str, sender: str):
        move_damaku = random.choices(
            [True, False],
            [self._config.damaku.moving_weight, self._config.damaku.static_weight],
            k=1
        )[0]
        return Damaku("damaku-from-%s" % sender, text, self.container, move_damaku).play()

    @Slot()
    def handle(self):
        @Slot()
        def read():
            _success = 0
            _err_failed_to_deserialize = -1
            _err_no_damaku = -2
            _err_format_error = -3
            response: dict[str, str | int] = {
                "result": _success,
                "message": "Success to record damaku."
            }
            try:
                data = client.readAll().data().decode()
            except:
                error("Failed to decode client %s's data" % client)
                response["result"] = _err_failed_to_deserialize
                response["message"] = "Failed to deserialize data."
                client.write(json.dumps(response).encode())
            else:
                debug("Received string: %s" % data)
                try:
                    result: dict[str, Any] | list[Any] = json.loads(data)
                except:
                    error("Failed to deserialize data string")
                    response["result"] = _err_failed_to_deserialize
                    response["message"] = "Failed to deserialize data."
                    client.write(json.dumps(response).encode())
                else:
                    if isinstance(result, dict):
                        damaku = result.get("text")
                        if isinstance(damaku, str):
                            if isinstance(client, QTcpSocket):
                                sender = client.localAddress().toString()
                            else:
                                sender = "localhost"
                            self.djob.add.emit(damaku, sender)
                        else:
                            info("No damaku in data")
                            response["result"] = _err_no_damaku
                            response["message"] = "No \"text\" section found."
                    else:
                        response["result"] = _err_format_error
                        response["message"] = "Data is not JSON dict."
                    client.write(json.dumps(response).encode())
        client = self.socket.nextPendingConnection()
        client.readyRead.connect(read)

    def show(self) -> None:
        info("Starting distribution thread...")
        self.dthread.start()
        info("Starting socket server...")
        try:
            if isinstance(self.socket, QLocalServer):
                self.socket.listen(
                    self._config.network.address.removeprefix("local://"))
                address = self.socket.serverName()
            else:
                self.socket.listen(
                    QHostAddress(
                        self._config.network.address.removeprefix("tcp://")),
                    self._config.network.port
                )
                address = "tcp://%s:%s" % (
                    self.socket.serverAddress().toString(), self.socket.serverPort())

        except:
            error("Failed to listen socket.")
            raise
        else:
            self.socket.newConnection.connect(self.handle)
            info("Bind to %s successfully." % address)
        self.container.show()
        return self.showFullScreen() if self._config.ui.fullscreen else super().show()

    def close(self) -> bool:
        info("Closing socket...")
        self.socket.close()
        info("Closing distribution thread...")
        self.djob.stop.emit()
        self.dthread.quit()
        if not self.dthread.isFinished():
            info("Waiting distribution to be closed...")
            self.dthread.wait()
        info("Closing App...")
        return super().close()

    def contextMenuEvent(self, event: QContextMenuEvent) -> None:
        menu = QMenu(self)
        menu.addAction(self.tr("&Exit"), self.close)  # type: ignore
        menu.move(event.pos())
        menu.show()
        return super().contextMenuEvent(event)
