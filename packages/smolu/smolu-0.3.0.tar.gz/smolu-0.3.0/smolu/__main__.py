"""File based url shortening for individual use."""

import os
from argparse import ArgumentParser
import sys

from . import Config, make_file, gen_qr


def main() -> None:
    parser = ArgumentParser()

    parser.add_argument("target", nargs="?", default=None, help="target url")
    parser.add_argument(
        "--configure", "-c", action="store_true", help="configure the generator"
    )
    parser.add_argument(
        "--template", "-t", action="store_true", help="read the new template from stdin"
    )

    opts = parser.parse_args()

    config = Config.load()

    if opts.configure:
        print("Configure wizard:")
        config.server_address_prefix = ask(
            "URL prefix",
            config.server_address_prefix,
        )
        config.server_root = ask(
            "Server root", config.server_root, lambda x: os.path.isdir(x)
        )

        config.random_byte_length = ask(
            "Random byte length",
            config.random_byte_length,
            lambda x: x.isdigit() and int(x) >= 0,
        )

        config.timestamp_byte_length = ask(
            "Timestamp byte length",
            config.timestamp_byte_length,
            lambda x: x.isdigit() and int(x) >= 0,
        )

        gq = ask(
            "Generate QR code",
            "yes" if config.gen_qr else "no",
            lambda x: x.lower() in ("true", "false", "yes", "no", "y", "n"),
        )

        if gq.lower() in ("true", "yes", "y"):
            config.gen_qr = True
        elif gq.lower() in ("false", "no", "n"):
            config.gen_qr = False

        config.fix()
        config.save()

        print("Current configuration:")
        config.print()

    elif opts.template:
        config.template = sys.stdin.read()
        config.save()

    elif opts.target is None:
        parser.print_help()
        sys.exit(1)

    else:
        url, uid = make_file(config, opts.target)
        if config.gen_qr:
            gen_qr(config, uid)

        print(url)



def ask(question: str, default, validator=lambda _: True):
    while True:
        print(question + "?")
        print(f"Default: {default}")
        answer = input("> ")
        if not answer:
            return default

        if validator(answer):
            return answer


if __name__ == "__main__":
    main()
