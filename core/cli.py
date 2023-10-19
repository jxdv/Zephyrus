import argparse


def parse_cli():
    """Parse command line arguments"""

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
        "--target",
        help="Path to file which contains newline-delimited targets"
    )
    parser.add_argument(
        "--hash",
        choices=["sha256", "md5"],
        help="Hashing algorithm for calculating checksums"
    )
    parser.add_argument(
        "--silent",
        action="store_true",
        default=False,
        help="Only log critical messages such as integrity change"
    )
    args = vars(parser.parse_args())

    return args
