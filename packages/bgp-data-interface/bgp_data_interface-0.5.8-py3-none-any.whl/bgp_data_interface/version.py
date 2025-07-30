import tomllib

with open("pyproject.toml", "rb") as file:
    data = tomllib.load(file)
    VERSION = data['project']['version']


class Version:

    def __init__(self) -> None:
        return

    def version(self) -> str:
        return VERSION
