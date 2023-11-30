import pytest
import json
import tomli_w
from qdamakuengine.config import *


dict_map: dict[str, bool | str | int | dict[str, bool | str | int]] = {
    "debug": True
}

target = Config()
target.debug = True


def test_config_from_json_complex():
    dict_map = {
        "debug": True,
        "network": {
            "address": "0.0.0.0",
            "port": 1024
        }
    }
    target = Config()
    target.debug = True
    network = target.network
    network.address = "0.0.0.0"
    network.port = 1024
    target.network = network
    assert Config.from_dict(**dict_map) == target


def test_config_from_json():
    assert Config.from_dict(**dict_map) == target


def test_get_config_invalid_file(tmp_path: Path):
    with (tmp_path/"invalid-toml.toml").open("w", encoding="utf-8") as writer:
        writer.write("Invalid test file")
    with pytest.raises(InvalidConfigurationException):
        get_config(tmp_path/"invalid-toml.toml")


def test_get_config_no_file(tmp_path: Path):
    assert get_config(tmp_path/"nosuchfile.txt") == Config()


def test_get_config_no_args():
    assert get_config() == Config()


def test_get_config_json(tmp_path: Path):
    with (tmp_path/"test-config.json").open("w", encoding="utf-8") as writer:
        writer.write(json.dumps(dict_map))
    assert get_config(tmp_path/"test-config.json") == target
    assert get_config(str(tmp_path/"test-config.json")) == target


def test_get_config_toml(tmp_path: Path):
    with (tmp_path/"test-config.toml").open("w", encoding="utf-8") as writer:
        writer.write(tomli_w.dumps(dict_map))
    assert get_config(tmp_path/"test-config.toml") == target
    assert get_config(str(tmp_path/"test-config.toml")) == target


def test___eq__():
    class TestConfig(Config):
        pass
    assert Config() == TestConfig()