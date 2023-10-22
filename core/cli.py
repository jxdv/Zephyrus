import argparse


def parse_cli():
    """Parse CLI arguments"""

    parser = argparse.ArgumentParser(
        prog="Zephyrus",
        description="Local-based File Integrity Monitor",
        epilog="Made with love by https://github.com/jxd1337"
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show Zephyrus version"
    )
    parser.add_argument(
        "--dir",
        help="Path to dir which contains file to be monitored"
    )
    parser.add_argument(
        "--seconds",
        type=int,
        default=21600,
        help="Interval to check integrity of monitored targets (6 hours by default)"
    )
    parser.add_argument(
        "--hash",
        choices=["sha256", "md5"],
        default="sha256",
        help="Hashing algorithm for calculating checksums (default is sha256)"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="Verbose logging"
    )
    parser.add_argument(
        "--threads",
        type=int,
        help="Number of threads to use"
    )
    parser.add_argument(
        "--ignore-prefix",
        nargs="+",
        dest="ignored_prefixes",
        help="Files with supplied prefixes will be ignored"
    )
    parser.add_argument(
        "--ignore-suffix",
        nargs="+",
        dest="ignored_suffixes",
        help="Files with supplied suffixes will be ignored"
    )
    args = parser.parse_args()

    return args
