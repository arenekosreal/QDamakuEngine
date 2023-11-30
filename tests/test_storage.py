import pytest
from os import environ
from qdamakuengine.storage import *


@pytest.mark.skipif(system() != "Linux", reason="This test is for Linux platform.")
def test_get_config_dir_linux(tmp_path: Path):
    environ["XDG_CONFIG_HOME"] = ""
    assert get_config_dir() == Path(expanduser("~"))/".config"/APPNAME
    environ["XDG_CONFIG_HOME"] = tmp_path.as_posix()
    assert get_config_dir() == tmp_path/APPNAME


@pytest.mark.skipif(system() != "Windows", reason="This test is for Windows platform.")
def test_get_config_dir_windows():
    assert get_config_dir() == Path(expanduser("~"))/"AppData"/"Local"/APPNAME


@pytest.mark.skipif(system() != "Darwin", reason="This test is for Darwin platform.")
def test_get_config_dir_darwin():
    assert get_config_dir() == Path(expanduser("~")) / \
        "Library"/"Preferences"/APPNAME


@pytest.mark.skipif(system() in ["Linux", "Windows", "Darwin"], reason="This test is for other platform.")
def test_get_config_dir_other():
    assert get_config_dir() == Path(".")/APPNAME


@pytest.mark.skipif(system() != "Linux", reason="This test is for Linux platform.")
def test_get_cache_dir_linux(tmp_path: Path):
    environ["XDG_CACHE_HOME"] = ""
    assert get_cache_dir() == Path(expanduser("~"))/".cache"/APPNAME
    environ["XDG_CACHE_HOME"] = tmp_path.as_posix()
    assert get_cache_dir() == tmp_path/APPNAME


@pytest.mark.skipif(system() != "Windows", reason="This test is for Windows platform.")
def test_get_cache_dir_windows():
    assert get_config_dir() == Path(expanduser("~"))/"AppData"/"Local"/APPNAME


@pytest.mark.skipif(system() != "Darwin", reason="This test is for Darwin platform.")
def test_get_cache_dir_darwin():
    assert get_cache_dir() == Path(expanduser("~")) / \
        "Library"/"Caches"/APPNAME


@pytest.mark.skipif(system() in ["Linux", "Windows", "Darwin"], reason="This test is for other platform.")
def test_get_cache_dir_other():
    assert get_cache_dir() == Path(".")/APPNAME


@pytest.mark.skipif(system() != "Linux", reason="This test is for Linux platform.")
def test_get_resource_dir_linux(tmp_path: Path):
    environ["XDG_DATA_HOME"] = ""
    assert get_resource_dir() == Path(expanduser("~"))/".local"/"share"/APPNAME
    environ["XDG_DATA_HOME"] = tmp_path.as_posix()
    assert get_resource_dir() == tmp_path/APPNAME


@pytest.mark.skipif(system() != "Windows", reason="This test is for Windows platform.")
def test_get_resource_dir_windows():
    assert get_resource_dir() == Path(expanduser("~"))/"AppData"/"Local"/APPNAME


@pytest.mark.skipif(system() != "Darwin", reason="This test is for Darwin platform.")
def test_get_resource_dir_darwin():
    assert get_resource_dir() == Path(expanduser("~")) / \
        "Library"/"Application Support"/APPNAME


@pytest.mark.skipif(system() in ["Linux", "Windows", "Darwin"], reason="This test is for other platform.")
def test_get_resource_dir_other():
    assert get_resource_dir() == Path(".")/APPNAME


def test_get_overlaid_resource_path_linux():
    with pytest.raises(FileNotFoundError):
        get_overlaid_resource_path("")