from sys import path
path.append('./src/bgp_data_interface')

import tomllib
from version import Version


def test_version() -> None:

    version = Version().version()
    assert version is not None
    assert isinstance(version, str)
    assert version == _get_version()


def _get_version() -> str:
    with open("pyproject.toml", "rb") as file:
        data = tomllib.load(file)
        return data['project']['version']
