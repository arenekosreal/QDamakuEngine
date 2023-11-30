import sys
import argparse
from platform import system, release
from PySide6.QtCore import QTranslator, QLocale
from PySide6.QtWidgets import QApplication
from qdamakuengine.app import App
from qdamakuengine.config import get_config
from qdamakuengine.log import set_level
from qdamakuengine import APPNAME, APPVER, APPAUTHORDOMAIN, APPAUTHOR, APPID


def _apply_config():
    parser = argparse.ArgumentParser(
        description="Display damaku sent from remote")
    parser.add_argument(
        "--config", "-c",
        help="Specify where config file is. Default is ./config.toml",
        default="./config.toml")
    args, sys.argv = parser.parse_known_args()
    set_level(get_config(args.config).debug)


def start():
    """Start the program
    """
    _apply_config()
    QApplication.setApplicationDisplayName(APPNAME)
    QApplication.setApplicationName(APPNAME.lower())
    QApplication.setApplicationVersion(APPVER)
    QApplication.setOrganizationDomain(APPAUTHORDOMAIN)
    QApplication.setOrganizationName(APPAUTHOR)
    match system():
        case "Windows":
            try:
                rel = int(release())
            except:
                pass
            else:
                if rel >= 7:
                    # Setting taskbar icon on Windos 7 and later
                    import ctypes
                    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(  # type: ignore
                        APPID)
        case "Linux":
            # Wayland needs this
            QApplication.setDesktopFileName(APPID)
        case _:
            pass
    app = QApplication(sys.argv)
    window = App()
    window.show()
    translator = QTranslator(window)
    if translator.load(QLocale(), "qt"):
        app.installTranslator(translator)
    app.exec()


if __name__ == "__main__":
    start()
