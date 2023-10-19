import sys
import os

from .log import ZephyrusLogger

logger = ZephyrusLogger(__name__)


class Monitor:
    def __init__(self, target, hash_alg, verbose, threads):
        self.target = target
        self.hash_alg = hash_alg
        self.verbose = verbose
        self.threads = threads

    def _parse_target(self, target):
        try:
            with open(target, "r") as f:
                targets = f.readlines()
        except OSError as e:
            logger.error(f"_parse_target caught: {e}")
            sys.exit(1)
        except Exception as e:
            logger.error(f"_parse_target caught: {e}")
            sys.exit(1)

        if not targets:
            logger.info("Target file is empty. There's nothing to monitor!")
            sys.exit(1)

    def run(self):
        self._parse_target(self.target)

        logger.info("Zephyrus initialized.")
