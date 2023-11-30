from os import environ
from pathlib import Path
from platform import system
from os.path import expanduser
from importlib.resources import files, as_file
from qdamakuengine import APPNAME


_XDG_CONFIG_HOME = "XDG_CONFIG_HOME"
_XDG_CACHE_HOME = "XDG_CACHE_HOME"
_XDG_DATA_HOME = "XDG_DATA_HOME"
_LINUX_DATA_EXTRA_PATH = Path("/")/"share"/APPNAME.lower()


def get_config_dir() -> Path:
    """Get config directory of program

    Returns:
        Path: The path under config directory in pathlib.Path format
    """
    match system():
        case "Linux":
            xdg_config_home = environ.get(_XDG_CONFIG_HOME)
            return (Path(xdg_config_home) if xdg_config_home else Path(expanduser("~"))/".config")/APPNAME
        case "Windows":
            return Path(expanduser("~"))/"AppData"/"Local"/APPNAME
        case "Darwin":
            return Path(expanduser("~"))/"Library"/"Preferences"/APPNAME
        case _:
            return Path(".")/APPNAME


def get_cache_dir() -> Path:
    """Get cache directory of program

    Returns:
        Path: The path under cache directory in pathlib.Path format
    """
    match system():
        case "Linux":
            xdg_cache_home = environ.get(_XDG_CACHE_HOME)
            return (Path(xdg_cache_home) if xdg_cache_home else Path(expanduser("~"))/".cache")/APPNAME
        case "Windows":
            return Path(expanduser("~"))/"AppData"/"Local"/APPNAME
        case "Darwin":
            return Path(expanduser("~"))/"Library"/"Caches"/APPNAME
        case _:
            return Path(".")/APPNAME


def get_resource_dir() -> Path:
    """Get data directory of program

    Returns:
        Path: The path under resource directory in pathlib.Path format
    """
    match system():
        case "Linux":
            xdg_data_home = environ.get(_XDG_DATA_HOME)
            return (Path(xdg_data_home) if xdg_data_home else Path(expanduser("~"))/".local"/"share")/APPNAME
        case "Windows":
            return Path(expanduser("~"))/"AppData"/"Local"/APPNAME
        case "Darwin":
            return Path(expanduser("~"))/"Library"/"Application Support"/APPNAME
        case _:
            return Path(".")/APPNAME


def get_overlaid_resource_path(name: str) -> Path:
    """Get data path with a overlay mechanism

    Args:
        name(str): The resource filename, it must point to a file.
    Raises:
        FileNotFoundError: When no such file is found
    Returns:
        Path: the resource path in pathlib.Path format
    """
    # User level
    user_resource_dir = get_resource_dir()
    if (user_resource_dir/name).is_file():
        return user_resource_dir/name
    # System level(Linux specific)
    if (system() == "Linux") and (_LINUX_DATA_EXTRA_PATH/name).is_file():
        return _LINUX_DATA_EXTRA_PATH/name
    # Internal level
    if (files(__package__)/"resources"/name).is_file():
        with as_file(files(__package__)/"resources"/name) as path:
            return path
    # No such file
    raise FileNotFoundError("No such file: "+name)