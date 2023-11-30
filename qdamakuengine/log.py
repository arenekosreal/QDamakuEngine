import logging
import sys

from qdamakuengine import APPID, APPNAME
from qdamakuengine.storage import get_cache_dir


_LOGFILE = get_cache_dir()/(APPNAME+".log")
_LOG_STRING_FORMAT = "%(asctime)s-%(levelname)s-%(message)s"
_LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

_LOGFILE.parent.mkdir(exist_ok=True)
_logger = logging.getLogger(APPID)
_console = logging.StreamHandler(sys.stdout)
_file = logging.FileHandler(_LOGFILE, mode="w", encoding="utf-8")
_formatter = logging.Formatter(_LOG_STRING_FORMAT, _LOG_DATE_FORMAT)
_console.setFormatter(_formatter)
_file.setFormatter(_formatter)
_logger.addHandler(_console)
_logger.addHandler(_file)


def set_level(debug: bool = False):
    """Set level to logger and handlers

    Args:
        debug (bool): If is debug mode
    """
    _logger.setLevel(logging.DEBUG if debug else logging.INFO)
    _console.setLevel(logging.DEBUG if debug else logging.INFO)
    _file.setLevel(logging.DEBUG if debug else logging.INFO)


info = _logger.info
debug = _logger.debug
error = _logger.error
warn = _logger.warn