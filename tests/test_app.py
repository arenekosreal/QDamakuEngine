import pytest
from pytestqt.qtbot import QtBot
from qdamakuengine.app import App
from qdamakuengine.config import get_config


@pytest.mark.skip
def test_app(qtbot: QtBot):
    app = App()
    app.show()
    qtbot.addWidget(app)
    config = get_config()