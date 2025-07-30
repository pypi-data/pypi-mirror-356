import os
from time import time
from random import randbytes
from base64 import urlsafe_b64encode
from subprocess import run

from .config import Config
from .state import State


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


def make_qr(config: Config, uid: str) -> str:
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


def make_redir(config: Config, target: str) -> tuple[str, str]:
    id = gen_id(config)
    path = os.path.join(config.server_root, id)
    while os.path.exists(path):
        id = gen_id(config)
        path = os.path.join(config.server_root, id)

    with open(path, "w") as f:
        f.write(config.template.format(url=target))

    with State(config) as state:
        state.record(id, target)

    return config.server_address_prefix + id, id
