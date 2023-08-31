#!/usr/bin/env python3

import sys
import platform
import configparser

from nixShield.monitor import Monitor


def main():
    if platform.system() != "Linux":
        print("Non-UNIX system detected! Please run on a UNIX-like system.")
        sys.exit(1)

    if sys.version_info < (3, 6):
        print("Python version 3.6 or newer required to run nixShield!")
        sys.exit(1)

    config = configparser.ConfigParser()
    config.read("config/config.ini")
    monitor = Monitor(config)
    monitor.start()


if __name__ == "__main__":
    main()
