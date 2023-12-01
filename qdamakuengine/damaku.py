import json
import random
from PySide6.QtCore import QAbstractAnimation, QPoint, QPropertyAnimation, QTimer, Slot
from PySide6.QtGui import QColor, QPalette, Qt
from PySide6.QtWidgets import QLabel, QWidget
from qdamakuengine.config import get_config
from qdamakuengine.log import debug


class Damaku(QLabel):
    """A Damaku object includes the text, color and animation for a damaku

    Use Damaku.play to see it.
    """

    def __init__(self, name: str, text: str, parent: QWidget, move_damaku: bool = True):
        """Initialize a Damaku object

        Args:
            name(str): The name
            text(str): The damaku text
            parent(QWidget): The parent widget, it should be the main window of program
            move_damaku(bool): Play move animation, default to True, set to False to make damaku appear directly.
        """
        super().__init__(
            text, parent,
            f=Qt.WindowType.FramelessWindowHint | Qt.WindowType.X11BypassWindowManagerHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.move_damaku = move_damaku
        self._config = get_config().damaku
        font = self.font()
        font.setPointSize(
            random.randint(
                self._config.damaku_size_min,
                self._config.damaku_size_max
            )
        )
        self.setFont(font)
        self.color = QColor(random.randint(0, 255), random.randint(0, 255),
                            random.randint(0, 255), random.randint(128, 255))
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.WindowText, self.color)
        self.setPalette(palette)
        self.adjustSize()
        self.setObjectName(name)

    def __str__(self) -> str:
        data = {
            "id": self.objectName(),
            "text": self.text(),
            "color": "rgba(%d, %d, %d, %d)" % (
                self.color.red(), self.color.green(), self.color.blue(), self.color.alpha())
        }
        return json.dumps(data)

    def play(self):
        # This should have problems under wayland...
        parent = self.parentWidget()
        parent.activateWindow()
        position_y = \
            random.randint(0, parent.height()-self.height())
        if self.move_damaku:
            position_x = parent.width()
            debug("Creating moving damaku at (%d,%d)" %
                  (position_x, position_y))
            animation = QPropertyAnimation(self)
            animation.setTargetObject(self)
            animation.setPropertyName("pos".encode())
            animation.setDuration(1000*self._config.damaku_speed)
            animation.setStartValue(QPoint(position_x, position_y))
            animation.setEndValue(
                QPoint(
                    -self.width(),
                    position_y
                )
            )
            animation.finished.connect(self.close)
            animation.start(
                QAbstractAnimation.DeletionPolicy.DeleteWhenStopped)
        else:
            position_x = round((parent.width()-self.width())/2)
            debug("Creating static damaku at (%d,%d)" %
                  (position_x, position_y))
            self.move(position_x, position_y)
            QTimer.singleShot(  # type: ignore
                round(1000*self._config.damaku_speed*self._config.static_damaku_time_ratio), self.close)
        self.show()

    @Slot()
    def close(self) -> bool:
        self.deleteLater()
        return super().close()
