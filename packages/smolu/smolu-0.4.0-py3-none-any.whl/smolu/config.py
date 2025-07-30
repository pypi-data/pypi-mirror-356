import os
import sys
import json
from dataclasses import dataclass

DEFAULT_SERVER_ADDRESS_PREFIX = "example.com/u/"
DEFAULT_SERVER_ROOT = "/srv/http/u"
DEFAULT_TEMPLATE = """
<!DOCTYPE HTML>
<html lang="en-US">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="0; url={url}">
    </head>
    <body>
        If you are not redirected automatically, follow this <a href='{url}'>link</a>.
    </body>
</html>
"""
DEFAULT_RANDOM_BYTE_LENGTH = 2
DEFAULT_TIMESTAMP_BYTE_LENGTH = 4

USER_CONFIG = os.path.expanduser("~/.config/smolu.json")
DEFAULT_STATE_DB = os.path.expanduser("~/.local/share/smolu.db")


@dataclass
class Config:
    server_address_prefix: str
    server_root: str
    template: str
    random_byte_length: int
    timestamp_byte_length: int
    gen_qr: bool
    state_db: str

    @classmethod
    def load(cls, config_path=USER_CONFIG) -> "Config":
        config = {}

        try:
            with open(config_path, "r") as f:
                config = json.load(f)
        except FileNotFoundError:
            pass
        except json.JSONDecodeError:
            with (
                open(config_path, "r") as fin,
                open(config_path + ".invalid", "w") as fout,
            ):
                fout.write(fin.read())

            print(
                f"Invalid config file {config_path}, overwriting with a default config instead.",
                file=sys.stderr,
            )
            print(
                f"The faulty file is preserved at {config_path}.invalid",
                file=sys.stderr,
            )

        return cls.from_dict(config)

    @classmethod
    def from_dict(cls, config):
        c = cls(
            config.get("server_address_prefix", DEFAULT_SERVER_ADDRESS_PREFIX),
            config.get("server_root", DEFAULT_SERVER_ROOT),
            config.get("template", DEFAULT_TEMPLATE),
            config.get("random_byte_length", DEFAULT_RANDOM_BYTE_LENGTH),
            config.get("timestamp_byte_length", DEFAULT_TIMESTAMP_BYTE_LENGTH),
            config.get("gen_qr", False),
            config.get("state_db", DEFAULT_STATE_DB),
        )

        c.fix()
        return c

    def as_dict(self):
        return {
            "server_address_prefix": self.server_address_prefix,
            "server_root": self.server_root,
            "template": self.template,
            "random_byte_length": self.random_byte_length,
            "timestamp_byte_length": self.timestamp_byte_length,
            "gen_qr": self.gen_qr,
            "state_db": self.state_db,
        }

    def __getitem__(self, name):
        return getattr(self, name)

    def __setitem__(self, name, value):
        setattr(self, name, value)
        self.fix()

    def save(self, config_path=USER_CONFIG) -> None:
        with open(config_path, "w") as f:
            json.dump(self.as_dict(), f)

    def fix(self) -> None:
        if not isinstance(self.random_byte_length, int):
            self.random_byte_length = int(self.random_byte_length)

        if not isinstance(self.timestamp_byte_length, int):
            self.timestamp_byte_length = int(self.timestamp_byte_length)

        self.server_root = os.path.expanduser(self.server_root)

        if not self.server_address_prefix.endswith("/"):
            self.server_address_prefix += "/"

    def print(self) -> None:
        print(json.dumps(self.as_dict(), indent=4))
