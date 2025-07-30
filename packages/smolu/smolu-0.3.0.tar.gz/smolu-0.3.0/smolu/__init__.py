"""File based url shortening for individual use."""

import sys
import os
from time  import time
from random import randbytes
from base64 import urlsafe_b64encode
import json
from dataclasses import dataclass
from subprocess import run

__version__ = "0.3.0"
__author__ = "Théo Cavignac"

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


@dataclass
class Config:
    server_address_prefix: str
    server_root: str
    template: str
    random_byte_length: int
    timestamp_byte_length: int
    gen_qr: bool

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
        }

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


def gen_id(config: Config) -> str:
    t = round(time() * 1000)
    ts = t.to_bytes(8, "big")
    if config.timestamp_byte_length < 8:
        ts = ts[-config.timestamp_byte_length :]
    else:
        ts = b"\0" * (config.timestamp_byte_length - 8) + ts

    rd = randbytes(config.random_byte_length)
    id = urlsafe_b64encode(rd + ts).decode("utf-8")
    return id.rstrip("=")


def make_file(config: Config, target: str) -> tuple[str, str]:
    id = gen_id(config)
    path = os.path.join(config.server_root, id)
    while os.path.exists(path):
        id = gen_id(config)
        path = os.path.join(config.server_root, id)

    with open(path, "w") as f:
        f.write(config.template.format(url=target))

    return config.server_address_prefix + id, id


def gen_qr(config: Config, uid: str) -> str:
    path = os.path.join(config.server_root, uid + ".png")

    run(
        [
            "qrencode",
            "-l",
            "h",
            "-t",
            "PNG",
            "-o",
            path,
            "-",
        ],
        input=config.server_address_prefix + uid,
        text=True,
    )

    return path
