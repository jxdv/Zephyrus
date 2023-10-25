#!/usr/bin/env python3

import sys
import os

from core import version
from core.cli import parse_cli
from core.monitor import Monitor
from core.utils import print_logo
from core.utils import get_random_interval


def main():
    if sys.version_info < (3, 6):
        print("Python >= 3.6 required to run!")
        sys.exit(1)

    args = parse_cli()

    if args.version:
        print(f"Zephyrus version: {version}")
        sys.exit(0)

    if not args.dir:
        print("Please specify a target file!")
        sys.exit(1)

    if args.random_interval and args.interval:
        print("Can't set both static interval and random interval!")
        sys.exit(1)

    if args.random_interval:
        args.interval = get_random_interval()

    if args.interval is not None and int(args.interval) < 60:
        print("interval has to be >= 60s")
        sys.exit(1)

    print_logo()

    monitor = Monitor(args.dir,
                      int(args.interval),
                      args.hash,
                      args.verbose,
                      args.ignored_prefixes,
                      args.ignored_suffixes
                      )
    monitor.menu()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted")
        try:
            sys.exit(130)
        except SystemExit:
            os._exit(130)
