"""File based url shortening for individual use."""

import os
from argparse import ArgumentParser
import sys

from .state import State
from .config import Config
from .gen import make_redir, make_qr


def main() -> None:
    parser = ArgumentParser(description="Manage shortened urls redirections")

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--add", "-a", help="a new target url to redir to")
    group.add_argument("--remove", "-r", help="remove a redirection by id or target")
    group.add_argument(
        "--list", "-l", action="store_true", help="list all generated urls"
    )
    group.add_argument(
        "--configure",
        "-c",
        metavar="KEY[=VALUE]",
        nargs="?",
        help="configure the generator",
    )

    opts = parser.parse_args()

    config = Config.load()

    if opts.list:
        with State(config) as state:
            for id, target in state.list():
                print(config.server_address_prefix + id, target)

    elif opts.add:
        url, uid = make_redir(config, opts.add)
        if config.gen_qr:
            make_qr(config, uid)

        print(url)

    elif opts.remove:
        with State(config) as state:
            id = state.find(opts.remove)
            if not id:
                print(f"No such redirection: {opts.remove}", file=sys.stderr)
                sys.exit(1)

            os.remove(os.path.join(config.server_root, id))
            if os.path.exists(os.path.join(config.server_root, id + ".png")):
                os.remove(os.path.join(config.server_root, id + ".png"))

            state.remove(id)

    elif opts.configure is True:
        edit_config(config)
        config.save()

        print("Current configuration:")
        config.print()

    elif opts.configure:
        if "=" in opts.configure:
            key, _, value = opts.configure.partition("=")
            config[key] = value

        else:
            key = opts.configure
            if key not in config.as_dict():
                print(f"Unknown key {key}", file=sys.stderr)
                sys.exit(1)

            if key == "template":
                if os.isatty(sys.stdin.fileno()):
                    print("Template (multiline, Ctrl-D to finish):")
                config.template = sys.stdin.read()
            else:
                config[key] = input("> ")

    else:
        parser.print_help()
        sys.exit(1)


def edit_config(config: Config):
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
