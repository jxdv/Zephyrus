import sys
import os

from .target import Target
from .log import ZephyrusLogger
from .utils import zephyrus_prompt

logger = ZephyrusLogger(__name__)


class Monitor:
    def __init__(self, target, hash_alg, verbose, threads, ignored_prefixes, ignored_suffixes):
        self.target = target
        self.hash_alg = hash_alg
        self.verbose = verbose
        self.threads = threads
        self.ignored_prefixes = ignored_prefixes
        self.ignored_suffixes = ignored_suffixes
        self.targets = []

    def filter_check(self, file_path):
        if self.ignored_prefixes:
            return any(file_path.startswith(prefix) for prefix in self.ignored_prefixes)
        if self.ignored_suffixes:
            return any(file_path.endswith(suffix) for suffix in self.ignored_suffixes)
        return False

    def _parse_target(self, target):
        if not os.path.isdir(target):
            logger.info(f"{target} is not a directory!")
            sys.exit(1)

        for path, _, files in os.walk(target):
            for name in files:
                file_path = os.path.join(path, name)
                if not self.filter_check(name):
                    target = Target(file_path)
                    self.targets.append(target)

        if not self.targets:
            logger.info("Target directory is empty!")
            sys.exit(1)

    def run(self):
        self._parse_target(self.target)

        seconds = zephyrus_prompt("Interval for monitoring (in seconds):", choice_type="int")
