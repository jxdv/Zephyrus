#!/usr/bin/env python3

import sys

from core import version
from core.cli import parse_cli
from core.monitor import Monitor
from core.utils import print_logo


def main():
    args = parse_cli()

    if args["version"]:
        print(f"Zephyrus version: {version}")
        sys.exit(0)

    if not args["target"]:
        print("Please specify a target file!")
        sys.exit(1)

    print_logo()

    monitor = Monitor(args["target"], args["hash"], args["silent"])


if __name__ == "__main__":
    main()
