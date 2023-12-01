import json
import tomllib
import magic
from os.path import isfile
from pathlib import Path
from typing import Any, Self, overload
from abc import ABC, abstractmethod


class DeserializableObject(ABC):
    @classmethod
    @abstractmethod
    def from_dict(cls, **data: Any) -> Self:
        pass

    def __eq__(self, __value: object) -> bool:
        return __value.__dict__ == self.__dict__ if hasattr(__value, "__dict__") else False


class BaseConfig(DeserializableObject):
    @classmethod
    def from_dict(cls, **data: Any) -> Self:
        instance = cls()
        for key in dir(instance):
            item = getattr(instance, key)
            if key in data.keys():
                value = data[key]
                if type(value) == type(item):
                    setattr(instance, key,
                            value)
                elif isinstance(value, dict) and isinstance(item, DeserializableObject):
                    setattr(instance, key,
                            type(item).from_dict(**value))
        return instance


class UIConfig(BaseConfig):
    fullscreen = False
    shadow_radius = 4
    width = 800
    height = 600


class DamakuConfig(BaseConfig):
    damaku_speed = 5
    damaku_size_min = 20
    damaku_size_max = 30
    moving_weight = 0.8
    static_weight = 0.2
    static_damaku_time_ratio = 0.2
    damaku_send_wait_secs = 0.1


class NetworkConfig(BaseConfig):
    address = "tcp://127.0.0.1"
    port = 2333


class Config(BaseConfig):
    debug = False
    network = NetworkConfig()
    ui = UIConfig()
    damaku = DamakuConfig()


class InvalidConfigurationException(Exception):
    pass


class _Cache:
    config: Config = Config()


@overload
def get_config(path: Path) -> Config:
    pass


@overload
def get_config(path: str) -> Config:
    pass


@overload
def get_config() -> Config:
    pass


def get_config(path: Path | str | None = None) -> Config:
    """Get config instance from config file

    Args:
        path (Path|str|None): The config path, defaults to None for current config

    Raises:
        InvalidConfigurationException: When configuration file is failed to deserialize.

    Returns:
        Config: the configuration instance
    """
    if not path:
        return _Cache.config
    data = None
    if isinstance(path, str):
        if isfile(path):
            with open(path, "r", encoding="utf-8") as reader:
                data_string = reader.read()
            try:
                match magic.from_file(path, mime=True):  # type: ignore
                    # Hope toml has its mime type
                    case "text/plain":
                        if path.endswith(".toml"):
                            data = tomllib.loads(data_string)
                    case "application/json":
                        data = json.loads(data_string)
                    case _:
                        pass
            except:
                raise InvalidConfigurationException(
                    "Configuration file is failed to deserialize.")
    else:
        if path.is_file():
            try:
                match magic.from_file(path, mime=True):  # type: ignore
                    case "text/plain":
                        if path.name.endswith(".toml"):
                            data = tomllib.loads(
                                path.read_text(encoding="utf-8"))
                    case "application/json":
                        data = json.loads(path.read_text(encoding="utf-8"))
                    case _:
                        pass
            except:
                raise InvalidConfigurationException(
                    "Configuration file is failed to deserialize.")
    if isinstance(data, dict):
        instance = Config.from_dict(**data)
        _Cache.config = instance
        return instance
    return _Cache.config
