from qdamakuengine.log import *


def test_set_level():
    set_level(False)
    set_level(True)
    set_level()


def test_info():
    info("qdamakuengine.tests.test_log:info")


def test_error():
    error("qdamakuengine.tests.test_log:error")


def test_debug():
    set_level(True)
    debug("qdamakuengine.tests.test_log:debug")